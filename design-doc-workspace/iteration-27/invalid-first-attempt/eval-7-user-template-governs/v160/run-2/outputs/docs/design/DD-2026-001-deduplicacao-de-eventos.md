# Serviço de deduplicação de eventos · DD-2026-001

| | |
|---|---|
| **Documento** | DD-2026-001 |
| **Estado** | Rascunho |
| **Autores** | Rafael Nunes |
| **Revisores** | |
| **Criado em** | 2026-11-22 |
| **Última atualização** | 2026-11-22 |

## Motivação

O pipeline de ingestão recebe eventos duplicados dos produtores, que reenviam o mesmo evento quando fazem retry. No mês passado medimos 4% de eventos duplicados. Os duplicados chegam aos relatórios de faturamento e inflam os valores. O financeiro já reclamou duas vezes.

Hoje nenhum ponto do pipeline descarta duplicatas. Cada consumidor recebe o evento repetido e o processa de novo.

## Proposta

Criar um serviço de deduplicação entre o ingestor e o Kafka. O serviço guarda no Redis a chave idempotente de cada evento por 24 horas e descarta os eventos cuja chave já existe.

```
Produtor --> Ingestor --> Serviço de deduplicação --> Kafka
                                   |
                                   v
                                 Redis
                          (chave idempotente, TTL 24h)
```

Fluxo para cada evento:

1. O ingestor entrega o evento ao serviço de deduplicação.
2. O serviço consulta a chave idempotente do evento no Redis.
3. Se a chave não existe, o serviço grava a chave com TTL de 24h e publica o evento no Kafka.
4. Se a chave existe, o serviço descarta o evento e não publica nada no Kafka.

### Alternativas descartadas

- **Deduplicar no consumidor.** Cada consumidor teria que reimplementar a deduplicação. Descartada.
- **Idempotência nativa do produtor Kafka.** Não cobre o reenvio entre reinícios do produtor, que é um dos casos que geram as duplicatas. Descartada.

## Riscos

- **Mais um salto no caminho crítico da ingestão.** Estimamos +5ms de latência por evento. Aceitamos esse trade-off para eliminar as duplicatas na entrada, em um único lugar. A estimativa ainda não foi medida; ver Perguntas abertas.
- **Redis indisponível.** O serviço depende do Redis para decidir. O comportamento nesse caso (deixar passar ou bloquear) ainda não está definido; ver Perguntas abertas.
- **Duplicata fora da janela de 24h.** Um reenvio que chegue depois de 24h da primeira entrega não será detectado, porque a chave já expirou.

## Plano de rollout

A definir. Este plano precisa de fases, de um critério de avanço e de um critério de rollback para cada fase; ver Perguntas abertas.

## Métricas de sucesso

- Taxa de eventos duplicados abaixo de 0,1% (linha de base: 4% no mês passado).
- Latência adicionada à ingestão medida e comparada com a estimativa de +5ms.

## Perguntas abertas

- Quais são as fases do rollout, e qual o critério de avanço e de rollback de cada uma?
- Se o Redis estiver indisponível, o serviço deixa o evento passar (risco de duplicata) ou bloqueia a ingestão (risco de perda de disponibilidade)?
- Como a chave idempotente é definida e quem a gera: o produtor ou o ingestor?
- Como vamos medir a latência real adicionada e confirmar a estimativa de +5ms?
- Quem revisa este documento pelo time de arquitetura?
