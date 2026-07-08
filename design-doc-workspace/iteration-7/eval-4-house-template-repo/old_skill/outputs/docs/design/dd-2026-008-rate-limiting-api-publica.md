# DD-2026-008 · Rate limiting da API pública

| | |
|---|---|
| **Documento** | DD-2026-008 |
| **Estado** | Rascunho |
| **Autores** | *(a preencher)* |
| **Revisores** | *(a preencher)* |
| **Criado em** | 2026-07-07 |
| **Última atualização** | 2026-07-07 |
| **Tags** | rate-limiting, api-pública, gateway, redis |

## Resumo

Hoje a API pública não impõe nenhum limite de tráfego por cliente: um único cliente abusivo consegue derrubar a API para todos, como aconteceu no incidente INC-4412. Este documento propõe rate limiting por token de API no gateway (Kong), com janela deslizante sobre contadores no Redis e limites definidos por plano, respondendo `429` com o header `Retry-After` quando o limite é excedido.

## Contexto

Em 2026-07-06, um cliente com integração mal feita enviou 40× o tráfego normal e derrubou a API pública para todos os clientes por 25 minutos (incidente INC-4412). Não existe hoje nenhum limite por cliente: qualquer token pode consumir a capacidade inteira da API. A proposta abaixo foi fechada no war room do incidente. O tráfego da API pública já passa pelo Kong como gateway, e o time já opera um Redis usado para sessão.

## Objetivos

- Nenhum token excede seu limite por mais de 1 segundo.
- A API sustenta um cliente abusivo sem degradar os demais clientes.

## Proposta

O Kong aplica rate limit **por token de API**, com **janela deslizante** calculada sobre contadores armazenados no Redis que já usamos para sessão. Os limites são definidos por plano:

| Plano | Limite |
|---|---|
| Free | 10 rps |
| Pro | 100 rps |
| Enterprise | Negociado por contrato |

Quando um token excede seu limite, o gateway responde `429 Too Many Requests` com o header `Retry-After`, indicando ao cliente quando tentar de novo.

Como o limite é por token e não por IP, clientes distintos atrás de um NAT compartilhado não geram falsos positivos: cada um conta contra o próprio limite.

### Compensações

- ✓ Bloqueia o cliente abusivo no gateway, antes de a requisição consumir gateway e malha de serviços
- ✓ Reaproveita o Redis que já usamos para sessão — nenhuma peça nova de infraestrutura
- ✗ Cliente legítimo em pico (ex.: Black Friday) pode receber `429`; mitigamos com o `Retry-After` e com um alerta para o time de contas avisar os clientes enterprise
- ✗ O Redis de sessão passa a ficar no caminho crítico de toda requisição da API pública (ver Riscos)

## Alternativas consideradas

1. **Limitar dentro de cada serviço** — descartada: o limite atua tarde demais, porque a requisição já consumiu gateway e malha de serviços quando chega ao serviço.
2. **Módulo pago do gateway gerenciado** — descartada: custo e lock-in no fornecedor.
3. **Não fazer nada** — descartada: sem limite por cliente, um único cliente abusivo repete o cenário do INC-4412 e derruba a API para todos.

## Riscos

| Risco | Mitigação |
|---|---|
| O Redis de sessão virar ponto de contenção com os contadores de rate limit | Medir a carga no Redis antes de ativar o enforcing — a fase de shadow mode mede sem aplicar limite |

## Plano de entrega

1. Shadow mode: contadores ativos no gateway, só medindo, sem aplicar limite
2. Enforcing no plano free
3. Enforcing geral (pro e enterprise)
