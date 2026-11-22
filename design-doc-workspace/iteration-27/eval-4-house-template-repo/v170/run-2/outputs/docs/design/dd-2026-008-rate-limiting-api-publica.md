# DD-2026-008 · Rate limiting da API pública

| | |
|---|---|
| **Documento** | DD-2026-008 |
| **Estado** | Rascunho |
| **Autores** | cassiobotaro |
| **Revisores** | A definir |
| **Criado em** | 2026-11-22 |
| **Última atualização** | 2026-11-22 |
| **Tags** | api, gateway, rate-limiting, redis, kong |

## Resumo

Hoje a API pública não limita o tráfego por cliente. No incidente INC-4412, um cliente com uma integração mal feita derrubou a API para todos por 25 minutos. Este documento propõe um rate limit por token de API no gateway (Kong), com janela deslizante e contadores no Redis de sessão, limites por plano e resposta `429` com `Retry-After`.

## Contexto

Em 2026-11-21, um cliente com uma integração mal feita enviou 40x o tráfego normal e a API ficou indisponível para todos os clientes por 25 minutos (INC-4412). Não existe hoje limite por cliente na API pública.

O gateway é o Kong. O Redis que guarda as sessões já está em uso e é a base proposta para os contadores.

## Objetivos

- Nenhum token excede o limite do seu plano por mais de 1 segundo.
- A API suporta um cliente abusivo sem degradar os demais.

## Proposta

O Kong aplica o limite por token de API, antes de a requisição chegar aos serviços. Os contadores usam janela deslizante e ficam no Redis de sessão. Quando o token estoura o limite, o gateway responde `429` com o header `Retry-After`.

Limites por plano:

| Plano | Limite |
|---|---|
| Free | 10 rps |
| Pro | 100 rps |
| Enterprise | Negociado por cliente |

O limite é por token e não por IP. Por isso clientes que compartilham um NAT não afetam uns aos outros, e esse cenário não é um risco deste desenho.

### Compensações

- ✓ A requisição de um cliente abusivo é barrada no gateway, sem consumir os serviços nem a malha
- ✓ Sem custo de módulo pago e sem lock-in
- ✗ Um cliente legítimo em pico (por exemplo, Black Friday) pode receber `429`
- ✗ O Redis de sessão passa a receber também a carga dos contadores

Para o primeiro custo, o `Retry-After` diz ao cliente quando tentar de novo, e um alerta chega ao time de contas, que avisa os clientes enterprise.

## Alternativas consideradas

| Alternativa | Por que perdeu |
|---|---|
| Não fazer nada | O INC-4412 mostra o custo: um único cliente derrubou a API para todos por 25 minutos |
| Limitar dentro de cada serviço | Tarde demais: a requisição já consumiu o gateway e a malha |
| Módulo pago do gateway gerenciado | Custo e lock-in |
| **Rate limit por token no Kong com Redis de sessão (escolhida)** | |

## Riscos

| Risco | Mitigação |
|---|---|
| O Redis de sessão vira ponto de contenção | O time mede a carga no Redis antes de ativar o limite |
| Cliente legítimo toma `429` em pico | O `Retry-After` orienta o cliente, e o alerta chega ao time de contas, que avisa os clientes enterprise |

## Plano de entrega

1. Shadow mode: o limite só mede, sem bloquear
2. Enforcing no plano free
3. Enforcing em todos os planos

## Perguntas em aberto

- Quem revisa o documento (áreas de Plataforma, SRE, Contas)?
- Qual o comportamento quando o Redis fica indisponível: o gateway deixa passar ou bloqueia?
- Como o gateway associa cada token ao plano e ao limite negociado dos clientes enterprise?
- Qual o comportamento para requisições sem token válido?
- Quanto tempo dura cada fase do plano de entrega e qual critério libera a passagem para a seguinte?
