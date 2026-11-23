# Serviço de deduplicação de eventos · DD-2026-001

| | |
|---|---|
| **Documento** | DD-2026-001 |
| **Estado** | Rascunho |
| **Autores** | Rafael Nunes |
| **Revisores** | |
| **Criado em** | 2026-11-23 |
| **Última atualização** | 2026-11-23 |

## Motivação

O pipeline de ingestão recebe eventos duplicados dos produtores, que reenviam o mesmo evento quando fazem retry. No mês passado medimos 4% de eventos duplicados. As duplicatas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes.

## Proposta

Criamos um serviço de deduplicação entre o ingestor e o Kafka. Para cada evento recebido do ingestor, o serviço consulta no Redis a chave idempotente do evento. Se a chave já existe, o serviço descarta o evento. Se não existe, o serviço grava a chave no Redis com validade de 24 horas e encaminha o evento ao Kafka.

```
Produtores → Ingestor → Serviço de deduplicação → Kafka
                                 │
                               Redis
                        (chaves, TTL de 24h)
```

O serviço fica no caminho crítico da ingestão: nenhum evento chega ao Kafka sem passar por ele. Com isso, a deduplicação acontece uma única vez, antes de qualquer consumidor, e os consumidores não precisam tratar duplicatas.

O custo aceito é um salto a mais no caminho crítico, que estimamos em +5ms de latência de ingestão.

## Alternativas consideradas

Esta seção não existe no template; foi acrescentada para registrar o raciocínio da escolha, mantendo as demais seções na ordem do template.

- **Deduplicar no consumidor.** Descartada. Cada consumidor teria que reimplementar a deduplicação.
- **Idempotência nativa do produtor Kafka.** Descartada. Ela não cobre o reenvio entre reinícios do produtor, e esse é um dos casos que geram as duplicatas.

## Riscos

| Risco | Mitigação |
|---|---|
| Latência: o serviço adiciona um salto ao caminho crítico da ingestão, estimado em +5ms. | Custo aceito pelo time em troca da deduplicação central. |

Outros riscos ainda não foram levantados; ver Perguntas abertas.

## Plano de rollout

Ainda não definido; ver Perguntas abertas.

## Métricas de sucesso

| Métrica | Hoje | Meta |
|---|---|---|
| Eventos duplicados | 4% (mês passado) | Abaixo de 0,1% |

Acompanhamos também a latência de ingestão. A estimativa é de +5ms com o serviço no caminho.

## Perguntas abertas

1. **Revisores.** Quem revisa este documento no time de arquitetura?
2. **Chave idempotente.** Quem gera a chave de cada evento (produtor ou ingestor) e de que campos ela é composta?
3. **Janela de 24h.** Por que 24h? Existe retry de produtor que reenvia depois desse prazo?
4. **Falhas do serviço e do Redis.** O que o serviço faz com o evento se o Redis estiver indisponível: encaminha ou rejeita? Há outros riscos que o time quer registrar além da latência?
5. **Latência.** Os +5ms vêm de medição ou de estimativa? Existe um limite de latência acima do qual a proposta deixa de valer?
6. **Rollout.** Em quais fases o serviço entra em produção, com qual critério de avanço e qual critério de rollback?
7. **Medição.** Como medimos a taxa de duplicatas (os 4% de hoje e os 0,1% da meta) e em que prazo esperamos atingir a meta?
8. **Não fazer nada.** Houve alternativa de manter o cenário atual (por exemplo, corrigir só nos relatórios de faturamento)? Se sim, por que perdeu?
