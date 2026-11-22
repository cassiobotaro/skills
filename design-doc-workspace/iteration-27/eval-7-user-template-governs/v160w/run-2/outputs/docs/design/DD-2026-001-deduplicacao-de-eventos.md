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

O pipeline de ingestão recebe eventos duplicados dos produtores. A duplicata nasce quando o produtor reenvia o evento em um retry. Em outubro de 2026, medimos 4% de eventos duplicados.

As duplicatas inflam os relatórios de faturamento. O financeiro já reclamou duas vezes.

## Proposta

Vamos criar um serviço de deduplicação entre o ingestor e o Kafka. O ingestor envia cada evento ao serviço, e o serviço decide se o evento segue para o Kafka ou se é descartado.

A decisão usa a chave idempotente do evento. O serviço guarda a chave de cada evento no Redis por 24 horas. Quando chega um evento cuja chave já está no Redis, o serviço descarta o evento. Quando a chave é nova, o evento segue para o Kafka. Como a deduplicação acontece antes do Kafka, todos os consumidores recebem um fluxo sem os repetidos que o serviço reconhece.

### Alternativas consideradas

- **Deduplicar no consumidor.** Descartada. Cada consumidor teria que reimplementar a deduplicação.
- **Usar a idempotência nativa do produtor Kafka.** Descartada. Ela não cobre o reenvio entre reinícios do produtor.

Não fazer nada também é uma alternativa, mas mantém os 4% de duplicatas e as reclamações do financeiro.

### Trade-off aceito

O serviço adiciona um salto ao caminho crítico da ingestão. Estimamos +5 ms de latência por evento. O time aceita esse custo em troca da deduplicação centralizada, que os consumidores não precisam reimplementar.

## Riscos

- **Latência no caminho crítico.** O serviço soma uma chamada a cada evento ingerido, estimada em +5 ms. A estimativa ainda não foi medida. A medição entra nas métricas de sucesso.

Os demais riscos (indisponibilidade do serviço ou do Redis, retries fora da janela de 24 horas) e as mitigações de cada um dependem de decisões que ainda não tomamos. Estão em Perguntas abertas.

## Plano de rollout

O plano de fases, os critérios de avanço e o critério de rollback ainda não existem. Estão em Perguntas abertas.

## Métricas de sucesso

- Duplicatas abaixo de 0,1% dos eventos (linha de base: 4% em outubro de 2026).
- Latência adicionada na ingestão medida e comparada com a estimativa de +5 ms.

## Perguntas abertas

**Riscos**

1. Se o serviço ou o Redis ficar indisponível, o ingestor deve deixar o evento passar sem deduplicar (aceitando duplicatas) ou rejeitar o evento (aceitando perda de disponibilidade da ingestão)?
2. O que acontece com um reenvio que chega depois de 24 horas? A janela de 24 horas foi escolhida com base em algum dado sobre o intervalo máximo de retry dos produtores?
3. Qual é a latência máxima tolerável no caminho crítico? Os +5 ms vêm de medição ou de estimativa?

**Proposta**

4. A chave idempotente já existe em todos os eventos? Quem a gera, o produtor ou o ingestor?
5. O serviço grava a chave no Redis antes ou depois de publicar no Kafka? Isso define se uma falha no meio pode perder um evento ou deixar passar uma duplicata.
6. Qual é a capacidade esperada (eventos por segundo) e o tamanho do Redis para 24 horas de chaves?

**Plano de rollout**

7. Como o serviço entra em produção: em fases, por produtor ou por percentual de tráfego? Qual critério permite avançar de fase e qual dispara o rollback?

**Revisão**

8. Quem são os revisores deste documento?
