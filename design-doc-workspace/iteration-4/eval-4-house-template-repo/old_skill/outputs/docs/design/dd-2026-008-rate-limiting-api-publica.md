# DD-2026-008 · Rate limiting da API pública

| | |
|---|---|
| **Documento** | DD-2026-008 |
| **Estado** | Aprovado |
| **Autores** | — |
| **Revisores** | — |
| **Criado em** | 2026-06-07 |
| **Última atualização** | 2026-06-07 |
| **Tags** | api, rate-limiting, gateway, redis, resiliência |

## Resumo

A API pública não tem nenhum limite de tráfego por cliente. Ontem, um cliente com integração mal feita enviou 40x o tráfego normal e derrubou a API para todos por 25 minutos (INC-4412). Este documento propõe rate limiting por token de API no gateway (Kong), com janela deslizante e contadores no Redis, limites por plano e resposta `429` com `Retry-After`.

## Contexto

A API pública é compartilhada por todos os clientes e hoje não existe nenhum limite por cliente: um único integrador consegue consumir toda a capacidade. No INC-4412, um cliente com integração mal feita mandou cerca de 40x o tráfego normal e degradou a API para todo mundo por 25 minutos. Não há hoje mecanismo que isole um cliente abusivo dos demais.

O gateway em uso é o Kong. Já operamos um Redis para sessão, com capacidade e familiaridade do time.

## Objetivos

- Nenhum token excede seu limite por mais de 1 segundo.
- A API aguenta um cliente abusivo sem degradar os demais.

## Proposta

Rate limit **por token de API**, aplicado no gateway (Kong), antes de a requisição alcançar os serviços. O algoritmo é **janela deslizante**, com contadores no **Redis que já usamos para sessão**.

Limites por plano:

| Plano | Limite |
|---|---|
| Free | 10 rps |
| Pro | 100 rps |
| Enterprise | Negociado |

Quando um token ultrapassa seu limite, o gateway responde **`429 Too Many Requests`** com o header **`Retry-After`**, indicando ao cliente quando voltar a tentar.

### Compensações

- ✓ Isola o cliente abusivo no gateway, antes de consumir os serviços e a malha — um cliente não derruba os demais.
- ✓ Reaproveita o Kong e o Redis de sessão; sem componente novo nem custo de licença.
- ✗ Um cliente legítimo em pico (ex.: Black Friday) pode tomar `429`. Mitigamos com o `Retry-After` e com alerta para o time de contas avisar os clientes enterprise antecipadamente.

## Alternativas consideradas

- **Limitar dentro de cada serviço.** Descartada: tarde demais. Quando a requisição chega ao serviço, ela já consumiu gateway e malha — exatamente os recursos que queremos proteger.
- **Módulo pago de rate limiting do gateway gerenciado.** Descartada: custo e lock-in. A solução com Kong + Redis de sessão entrega o mesmo resultado sem ambos.
- **Não fazer nada.** Descartada: mantém a exposição que causou o INC-4412 — qualquer cliente continua capaz de derrubar a API para todos.

## Riscos

| Risco | Mitigação |
|---|---|
| O Redis de sessão virar ponto de contenção sob a carga adicional dos contadores | Medir antes de ativar o enforcing |

## Plano de entrega

1. **Shadow mode** — apenas medindo, sem bloquear nenhuma requisição.
2. **Enforcing no plano free** — passa a responder `429` para tokens free acima do limite.
3. **Enforcing geral** — enforcing para todos os planos.
