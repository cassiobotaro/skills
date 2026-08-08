# DD-2026-008 · Rate limiting da API pública

| | |
|---|---|
| **Documento** | DD-2026-008 |
| **Estado** | Rascunho |
| **Autores** | _a definir_ |
| **Revisores** | _a definir_ |
| **Criado em** | 2026-08-07 |
| **Última atualização** | 2026-08-07 |
| **Tags** | rate limiting, gateway, disponibilidade |

## Resumo

Um cliente com integração mal feita enviou 40 vezes o tráfego normal e derrubou a API pública para todos os clientes por 25 minutos (INC-4412). Hoje não existe nenhum limite por cliente. Este documento propõe rate limiting por token de API no gateway Kong, com janela deslizante e contadores no Redis, limites por plano e resposta 429 com `Retry-After`.

## Contexto

A API pública é exposta pelo gateway Kong e não aplica nenhum limite de requisições por cliente: qualquer token pode consumir a capacidade compartilhada até onde a infraestrutura aguentar. Em 2026-08-06, um cliente com integração mal feita passou a enviar cerca de 40 vezes o seu tráfego normal; a API ficou indisponível para todos os clientes por 25 minutos (INC-4412).

Os clientes são separados em planos comerciais (free, pro e enterprise). Já existe um Redis em produção usado para sessão.

## Objetivos

- Nenhum token excede o seu limite contratado por mais de 1 segundo.
- A API absorve um cliente abusivo sem degradar o atendimento dos demais clientes.

## Proposta

Rate limiting por **token de API**, aplicado no gateway Kong — antes de a requisição chegar aos serviços. O algoritmo é de **janela deslizante**, com os contadores no Redis que já usamos para sessão.

Limites por plano:

| Plano | Limite |
|---|---|
| free | 10 rps |
| pro | 100 rps |
| enterprise | negociado por contrato |

Requisição acima do limite recebe **HTTP 429** com o header `Retry-After`, indicando ao cliente quando pode tentar de novo.

### Compensações

- ✓ Contém um cliente abusivo na borda, sem que o tráfego excedente consuma os serviços internos
- ✓ Aproveita o Kong e o Redis que já estão em produção — nenhuma peça nova de infraestrutura
- ✗ Cliente legítimo em pico (por exemplo, Black Friday) pode tomar 429. Mitigação: o `Retry-After` na resposta e um alerta para o time de contas avisar os clientes enterprise
- ✗ Coloca o Redis de sessão no caminho crítico de toda requisição da API pública

## Alternativas consideradas

**Limitar dentro de cada serviço** — descartado. O limite chegaria tarde demais: quando o serviço decide rejeitar, a requisição já consumiu o gateway e a malha de serviços, que é justamente a capacidade que o INC-4412 esgotou.

**Módulo pago de rate limiting do gateway gerenciado** — descartado por custo e por lock-in no fornecedor.

**Não fazer nada** — descartado. É o cenário atual, sem nenhum limite por cliente, e foi o que permitiu o INC-4412 derrubar a API para todos os clientes por 25 minutos.

## Riscos

| Risco | Mitigação |
|---|---|
| O Redis de sessão vira ponto de contenção ao absorver os contadores de rate limit | Medir o impacto antes de habilitar o enforcing, na fase de shadow mode |

## Plano de entrega

1. **Shadow mode** — o limite é avaliado e medido, mas nenhuma requisição é bloqueada
2. **Enforcing no plano free**
3. **Enforcing geral** (free, pro e enterprise)
