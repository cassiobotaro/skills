# DD-2026-008 · Rate limiting da API pública

| | |
|---|---|
| **Documento** | DD-2026-008 |
| **Estado** | Proposto |
| **Autores** | — |
| **Revisores** | — |
| **Criado em** | 2026-06-07 |
| **Última atualização** | 2026-06-07 |
| **Tags** | api, rate-limiting, gateway, kong, redis |

## Resumo

A API pública não tem nenhum limite de tráfego por cliente. No incidente INC-4412, um cliente com integração mal feita enviou 40x o tráfego normal e derrubou a API para todos por 25 minutos. Este documento propõe rate limiting por token de API no gateway (Kong), com janela deslizante baseada em contadores no Redis, limites por plano e resposta 429 com header `Retry-After`.

## Contexto

Hoje não existe nenhum limite de requisições por cliente na API pública. Qualquer cliente pode consumir toda a capacidade compartilhada.

No incidente INC-4412 (ontem), um cliente com integração mal feita passou a enviar cerca de 40x o tráfego normal. Sem nenhum limite por cliente, esse tráfego saturou o gateway e a malha de serviços e a API ficou indisponível para todos os demais clientes por 25 minutos.

A decisão de mitigação foi fechada em war room: precisamos de um mecanismo que isole o impacto de um cliente abusivo para que ele não degrade a experiência dos outros.

## Objetivos

- Nenhum token de API excede o seu limite por mais de 1 segundo.
- A API suporta um cliente abusivo sem degradar o atendimento dos demais clientes.

## Proposta

Rate limit **por token de API no gateway (Kong)**, aplicado antes que a requisição consuma o gateway e a malha de serviços.

- **Algoritmo:** janela deslizante (sliding window) com contadores no Redis.
- **Armazenamento:** reuso do Redis que já usamos para sessão (sem nova peça de infraestrutura).
- **Limites por plano:**
  - Free: 10 rps
  - Pro: 100 rps
  - Enterprise: negociado por contrato
- **Resposta ao exceder o limite:** HTTP `429 Too Many Requests` com header `Retry-After` indicando quando o cliente pode tentar novamente.

### Alternativas consideradas

- **Limitar dentro de cada serviço** — descartada. É tarde demais: quando a requisição chega ao serviço ela já consumiu gateway e malha, exatamente o recurso que queremos proteger.
- **Módulo pago do gateway gerenciado** — descartada por custo e lock-in.

### Compensações

- ✓ Isola o impacto de um cliente abusivo: ele atinge o próprio limite sem degradar os demais.
- ✓ Reuso do Redis de sessão, sem introduzir nova infraestrutura.
- ✓ Limite aplicado no gateway, antes de consumir a malha de serviços.
- ✗ Um cliente legítimo em pico (ex.: Black Friday) pode tomar 429. Mitigamos com o `Retry-After` e com alerta para o time de contas avisar os clientes enterprise antecipadamente.

## Riscos

| Risco | Mitigação |
|---|---|
| O Redis de sessão virar ponto de contenção sob a carga adicional dos contadores de rate limit | Medir o impacto antes da ativação geral (durante o shadow mode) |

## Plano de entrega

1. **Shadow mode** — apenas medindo, sem bloquear nenhuma requisição.
2. **Enforcing no plano free** — bloqueio efetivo (429) aplicado primeiro ao plano free.
3. **Enforcing geral** — bloqueio efetivo para todos os planos.
