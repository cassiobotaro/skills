# DD-2026-008 · Rate limiting da API pública

| | |
|---|---|
| **Documento** | DD-2026-008 |
| **Estado** | Rascunho |
| **Autores** | A definir |
| **Revisores** | A definir |
| **Criado em** | 2026-11-22 |
| **Última atualização** | 2026-11-22 |
| **Tags** | api, gateway, rate-limiting, redis, incidente |

## Resumo

A API pública não tem limite de requisições por cliente, e um único cliente com uma integração mal feita derrubou a API para todos por 25 minutos (INC-4412). Este documento propõe um rate limit por token de API no gateway (Kong), com janela deslizante e contadores no Redis, limites por plano e resposta 429 com `Retry-After`. A entrega é em fases: shadow mode, enforcing no plano free e enforcing geral.

## Contexto

Em 2026-11-21, um cliente enviou cerca de 40 vezes o tráfego normal por causa de uma integração mal feita. A API ficou indisponível para todos os clientes por 25 minutos (INC-4412). Hoje não existe nenhum limite por cliente.

O gateway é o Kong. O Redis que guarda as sessões já está em produção e é a base de contadores proposta.

## Objetivos

- Nenhum token excede seu limite por mais de 1 segundo.
- A API aguenta um cliente abusivo sem degradar os demais.

## Proposta

O Kong aplica o limite por token de API em cada requisição. Os contadores ficam no Redis de sessão, com janela deslizante. Quando o token passa do limite do seu plano, o gateway responde 429 com o header `Retry-After` e a requisição não chega aos serviços.

Limites por plano:

| Plano | Limite |
|---|---|
| Free | 10 rps |
| Pro | 100 rps |
| Enterprise | Negociado por cliente |

O limite é por token, não por IP. Por isso, clientes distintos que saem pelo mesmo IP não dividem o mesmo contador.

Quando um cliente enterprise toma 429, um alerta chega ao time de contas, que avisa o cliente.

### Compensações

- ✓ O gateway barra a requisição acima do limite antes que ela consuma a malha ou os serviços
- ✓ Sem custo de licença e sem dependência do módulo pago do gateway gerenciado
- ✗ Cliente legítimo em pico (Black Friday, por exemplo) pode tomar 429. Mitigação: `Retry-After` na resposta e alerta ao time de contas para avisar os enterprise
- ✗ O Redis de sessão passa a receber uma operação de contador por requisição da API pública, e o rate limit passa a depender dele

## Alternativas consideradas

| Alternativa | Por que perdeu |
|---|---|
| Não fazer nada | O incidente INC-4412 mostra o custo: sem limite por cliente, um cliente derrubou a API para todos por 25 minutos |
| Limitar dentro de cada serviço | Tarde demais: a requisição já consumiu gateway e malha |
| Módulo pago de rate limiting do gateway gerenciado | Custo e lock-in |
| **Rate limit por token no Kong com contadores no Redis (escolhida)** | Barra a requisição na entrada, usa o Redis que já operamos e não adiciona custo de licença |

## Riscos

| Risco | Mitigação |
|---|---|
| O Redis de sessão virar ponto de contenção | Medir a carga dos contadores antes de ativar o enforcing (é o objetivo do shadow mode) |
| Cliente legítimo tomar 429 em pico | `Retry-After` na resposta e alerta ao time de contas para avisar os clientes enterprise |

## Plano de entrega

1. Shadow mode: o gateway só mede e registra quem passaria do limite, sem responder 429
2. Enforcing no plano free
3. Enforcing em todos os planos

## Perguntas em aberto

- Quem são os autores e os revisores deste documento? Pela área impactada, faz sentido incluir Plataforma, SRE e o time de contas.
- O que o gateway faz quando o Redis está indisponível: deixa passar ou bloqueia?
- Qual é o critério para sair do shadow mode e de cada fase seguinte, e qual a duração prevista de cada uma?
- Qual limite de carga no Redis de sessão decide que ele virou ponto de contenção?
- Qual condição dispara o alerta ao time de contas: o primeiro 429 ou a aproximação do limite?
- O que fica fora de escopo nesta entrega?
