# DD-2026-008 · Rate limiting por token na API pública

| | |
|---|---|
| **Documento** | DD-2026-008 |
| **Estado** | Rascunho |
| **Autores** | cassiobotaro |
| **Revisores** | A definir (ver Questões em aberto) |
| **Criado em** | 2026-11-22 |
| **Última atualização** | 2026-11-22 |
| **Tags** | rate-limiting, gateway, kong, redis, api-publica, INC-4412 |

## Resumo

Não existe limite de requisições por cliente na API pública, e um único cliente derrubou a API para todos no incidente INC-4412. Este documento propõe um rate limit por token de API no gateway (Kong), com janela deslizante, contadores no Redis que já usamos para sessão e limites por plano. O gateway responde 429 com o header `Retry-After` quando o token estoura o limite.

## Contexto

Em 2026-11-21, um cliente com uma integração mal feita enviou cerca de 40x o tráfego normal à API pública. A API ficou fora do ar para todos os clientes por 25 minutos (INC-4412). Hoje não existe limite por cliente, então nada contém automaticamente um cliente que abusa da API.

O tráfego da API pública passa pelo gateway (Kong) e pela malha de serviços antes de chegar a cada serviço. O time já opera um Redis para sessão.

## Objetivos

- Nenhum token excede o limite do seu plano por mais de 1 segundo.
- A API suporta um cliente abusivo sem degradar os demais clientes.

Limites por plano:

| Plano | Limite |
|---|---|
| Free | 10 rps |
| Pro | 100 rps |
| Enterprise | Negociado por cliente |

## Proposta

O gateway conta as requisições de cada token de API em uma janela deslizante, com os contadores guardados no Redis de sessão. Quando um token ultrapassa o limite do seu plano, o gateway rejeita a requisição com 429 e inclui o header `Retry-After`, para que o cliente saiba quando tentar de novo. A requisição rejeitada não chega à malha nem aos serviços.

O limite vale por token, não por IP. Clientes que compartilham um IP (NAT) não dividem a mesma cota.

### Compensações

- ✓ O gateway rejeita a requisição antes de ela consumir a malha e os serviços
- ✓ A proposta reaproveita o Redis que o time já opera, sem contratar nem integrar produto novo
- ✓ O limite por plano dá a cada cliente uma cota previsível
- ✗ Cliente legítimo em pico (Black Friday, por exemplo) pode receber 429. Mitigação: o `Retry-After` orienta o retry, e um alerta avisa o time de contas, que avisa os clientes enterprise
- ✗ O Redis de sessão passa a receber a contagem de todas as requisições da API pública e pode virar ponto de contenção (ver Riscos)

## Alternativas consideradas

| Alternativa | Resultado | Motivo |
|---|---|---|
| Não fazer nada | Descartada | Nada contém um cliente abusivo, e o INC-4412 pode se repetir |
| Limitar dentro de cada serviço | Descartada | Age tarde demais: a requisição já consumiu o gateway e a malha |
| Módulo pago do gateway gerenciado | Descartada | Custo e lock-in |
| **Rate limit por token no gateway com Redis** | **Escolhida** | Rejeita no gateway, reaproveita o Redis existente e evita o custo e o lock-in do módulo pago |

## Riscos

| Risco | Mitigação |
|---|---|
| O Redis de sessão vira ponto de contenção com a carga dos contadores | Medir a carga no Redis antes de ativar o enforcing |
| Cliente legítimo recebe 429 em pico de tráfego | `Retry-After` na resposta e alerta para o time de contas avisar os clientes enterprise |

## Plano de entrega

1. Shadow mode: o gateway só mede, sem rejeitar requisições
2. Enforcing no plano free
3. Enforcing em todos os planos

## Questões em aberto

- Quem revisa este documento? Quais times de Plataforma, SRE e Contas entram como revisores?
- O que acontece com as requisições quando o Redis fica indisponível?
- Quem configura o limite negociado de cada cliente enterprise, e onde esse valor fica registrado?
- Qual condição dispara o alerta para o time de contas?
- Quais critérios autorizam a passagem de uma fase do plano de entrega para a seguinte, e quanto tempo dura cada fase?
