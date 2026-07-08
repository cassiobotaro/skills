# DD-2026-007 · Cache de catálogo de produtos

| | |
|---|---|
| **Documento** | DD-2026-007 |
| **Estado** | Aprovado |
| **Autores** | Marina Costa |
| **Revisores** | João Prata (Plataforma), Lia Mendes (SRE) |
| **Criado em** | 2026-03-02 |
| **Última atualização** | 2026-03-20 |
| **Tags** | catálogo, cache, latência |

## Resumo

A página de produto consulta o serviço de catálogo a cada renderização e a latência P99 passou de 800ms na última campanha. Este documento propõe um cache read-through com Redis na frente do catálogo, com invalidação por evento de atualização de produto.

## Contexto

O serviço de catálogo serve cerca de 3 mil rps em pico, 95% leituras de produtos que mudam poucas vezes ao dia. Cada leitura hoje vai ao Postgres. A última campanha de marketing dobrou o tráfego e o P99 da página de produto chegou a 800ms, com o banco a 85% de CPU.

## Proposta

Cache read-through no Redis com TTL de 15 minutos e invalidação ativa: o serviço de catálogo publica `product.updated` e um consumidor remove a chave correspondente. Chave por produto (`catalog:product:{id}`), valor é a resposta serializada da API.

### Compensações

- ✓ P99 esperado abaixo de 200ms para produtos quentes (medido em prova de conceito)
- ✓ Reduz a carga de leitura do Postgres em ~80%
- ✗ Janela de até 15 minutos de dado desatualizado se o evento de invalidação for perdido
- ✗ Mais uma peça de infraestrutura no caminho crítico da página de produto

## Riscos

| Risco | Mitigação |
|---|---|
| Estouro de memória do Redis com o catálogo completo | TTL + maxmemory com política allkeys-lru |
| Avalanche de cache misses após deploy do Redis | Warm-up dos 10 mil produtos mais acessados |

## Plano de entrega

1. Prova de conceito com réplica de tráfego (1 semana) — feito
2. Cache em shadow mode medindo hit rate (1 semana)
3. Ativação para 10% do tráfego, depois 100%
