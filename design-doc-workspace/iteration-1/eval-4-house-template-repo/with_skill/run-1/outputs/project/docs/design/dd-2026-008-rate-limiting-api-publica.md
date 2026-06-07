# DD-2026-008 · Rate limiting da API pública

| | |
|---|---|
| **Documento** | DD-2026-008 |
| **Estado** | Proposto |
| **Autores** | Cássio Botaro |
| **Revisores** | _(a definir — sugeridos: Plataforma/Gateway, SRE, Contas/Customer Success)_ |
| **Criado em** | 2026-06-07 |
| **Última atualização** | 2026-06-07 |
| **Tags** | rate-limiting, gateway, kong, redis, resiliência |

## Glossário

- **rps** — requisições por segundo.
- **Janela deslizante** — contagem de requisições sobre uma janela de tempo que avança continuamente, em vez de zerar em fronteiras fixas; evita o pico de borda do contador fixo.
- **429** — código HTTP `Too Many Requests`, devolvido quando o cliente excede o limite.
- **Retry-After** — header HTTP que informa ao cliente quantos segundos esperar antes de tentar de novo.
- **Shadow mode** — modo em que o limite é apenas medido e registrado, sem rejeitar requisições.
- **Token de API** — credencial por cliente usada para autenticar chamadas à API pública; é a chave do rate limit.

## Resumo

Hoje a API pública não tem nenhum limite por cliente: um único integrador pode consumir toda a capacidade e derrubar a API para todos. Este documento propõe rate limiting por token de API no gateway (Kong), com janela deslizante apoiada no Redis de sessão que já operamos, limites por plano e resposta `429` com `Retry-After`.

## Contexto

A API pública atende todos os clientes pelo mesmo gateway (Kong) e pela mesma malha de serviços, sem nenhum limite por cliente. Em INC-4412, um cliente com integração mal feita disparou cerca de 40x o tráfego normal e degradou a API para todos os demais por 25 minutos. Não há, hoje, mecanismo que isole o consumo de um cliente do consumo dos outros.

Já operamos um Redis para sessão, com baixa latência e disponível para o caminho do gateway.

## Objetivos e fora de escopo

**Objetivos**

- Nenhum token excede o limite do seu plano por mais de 1 segundo — o limite é aplicado por janela deslizante no gateway, antes da malha de serviços.
- A API absorve um cliente abusivo (padrão INC-4412, ~40x o tráfego normal de um token) sem degradar os demais clientes — o excesso de um token é rejeitado com `429`, não propagado para os serviços.
- Limites por plano: free 10 rps, pro 100 rps, enterprise negociado por contrato.

**Fora de escopo**

- Limite por IP. O limite é por token de API; compartilhamento de IP (NAT) não influencia a contagem.
- Cotas de longo prazo (ex.: volume diário/mensal por cliente). Aqui tratamos de vazão (rps), não de cota agregada.
- Limitar tráfego interno entre serviços da malha.

## Proposta

Aplicar o rate limit **no gateway (Kong)**, identificado **pelo token de API**, usando **janela deslizante com contadores no Redis** que já usamos para sessão. A cada requisição autenticada, o gateway incrementa e consulta o contador do token na janela corrente; se o token estiver acima do limite do seu plano, o gateway responde `429` com `Retry-After` e a requisição **não** entra na malha de serviços. Os limites por plano são: free 10 rps, pro 100 rps, enterprise negociado.

Aplicar no gateway é deliberado: é o primeiro ponto onde a requisição pode ser barrada sem já ter consumido gateway + malha. A janela deslizante (em vez de contador fixo por segundo) evita que um cliente dispare o dobro do limite na virada de duas janelas adjacentes — o que importa para o objetivo de "não exceder por mais de 1s".

### Compensações

- ✓ Isola o consumo por token: o excesso de um cliente é barrado no gateway e não chega à malha, atendendo ao objetivo de aguentar um cliente abusivo sem degradar os demais.
- ✓ Reaproveita o Redis de sessão — sem nova peça de infraestrutura para operar.
- ✓ Janela deslizante elimina o pico de borda do contador fixo, sustentando o limite de "no máximo 1s acima".
- ✗ Cliente legítimo em pico (ex.: Black Friday) pode tomar `429`. Mitigação: `Retry-After` para o backoff automático do cliente, e alerta para o time de contas avisar os clientes enterprise antes de eventos previstos.
- ✗ Coloca o Redis de sessão no caminho crítico de toda requisição da API pública (ver Riscos).

## Alternativas consideradas

| Alternativa | Trade-off | Decisão |
|---|---|---|
| **Limitar no gateway por token (Redis)** | Barra o excesso no primeiro ponto possível; reusa infra existente; adiciona o Redis ao caminho crítico | ✓ Escolhida |
| Limitar dentro de cada serviço | A requisição já consumiu gateway e malha quando chega ao serviço — tarde demais para proteger a capacidade compartilhada | ✗ Descartada |
| Módulo pago do gateway gerenciado | Resolveria de forma gerenciada, mas com custo recorrente e lock-in no fornecedor | ✗ Descartada |
| Não fazer nada | Mantém a exposição que causou o INC-4412: um cliente continua capaz de derrubar a API para todos | ✗ Descartada |

## Riscos

| Risco | Mitigação |
|---|---|
| O Redis de sessão vira ponto de contenção ao entrar no caminho crítico de toda requisição | Medir o impacto antes do enforcing (latência e carga adicional no Redis), começando pelo shadow mode |

## Plano de entrega

1. **Shadow mode** — apenas medindo: o gateway conta por token e registra quem teria sido limitado, sem devolver `429`. Serve para dimensionar o impacto no Redis e validar os limites por plano.
2. **Enforcing no plano free** — passa a devolver `429` com `Retry-After` para tokens do plano free acima de 10 rps.
3. **Enforcing geral** — estende o enforcing para pro (100 rps) e enterprise (negociado).

## Questões em aberto

- Quem são os revisores formais (Plataforma/Gateway, SRE, Contas)? Sugeridos no cabeçalho, ainda a confirmar.
- Qual o critério de promoção entre as fases (ex.: limiar de latência adicional no Redis aceitável para passar de shadow para enforcing)?
