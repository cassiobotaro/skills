# Serviço de deduplicação de eventos · DD-2026-<seq>

| | |
|---|---|
| **Documento** | DD-2026-<seq> (a numeração aguarda resposta, ver Perguntas abertas) |
| **Estado** | Rascunho |
| **Autores** | Rafael Nunes |
| **Revisores** | Aguarda resposta (ver Perguntas abertas) |
| **Criado em** | 2026-11-22 |
| **Última atualização** | 2026-11-22 |

## Motivação

O pipeline de ingestão recebe eventos duplicados dos produtores, que reenviam o mesmo evento quando fazem retry. No mês passado medimos 4% de eventos duplicados. As duplicatas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes.

## Proposta

Um novo serviço de deduplicação fica entre o ingestor e o Kafka. Para cada evento recebido, o serviço consulta a chave idempotente do evento no Redis. Se a chave já existe, o serviço descarta o evento. Se não existe, o serviço grava a chave no Redis com validade de 24 horas e encaminha o evento ao Kafka.

O custo aceito é um salto a mais no caminho crítico da ingestão, estimado em +5 ms de latência.

### Alternativas consideradas

Esta seção não existe no template; foi adicionada porque a decisão depende dela.

| Alternativa | Resultado | Motivo |
|---|---|---|
| Deduplicar no consumidor | ✗ Descartada | Cada consumidor teria que reimplementar a deduplicação. |
| Idempotência nativa do produtor Kafka | ✗ Descartada | Não cobre reenvio entre reinícios do produtor. |
| Serviço entre o ingestor e o Kafka, com Redis | ✓ Escolhida | Deduplica uma vez, antes do Kafka, em um único lugar. |

A alternativa "não fazer nada" aguarda resposta (ver Perguntas abertas).

### Trade-offs aceitos

Esta seção também não existe no template.

- ✓ Os repetidos saem do fluxo antes de chegar ao Kafka e aos consumidores.
- ✗ Um salto a mais no caminho crítico da ingestão, com +5 ms de latência estimados.

## Riscos

Aguarda resposta: o autor ainda não listou os riscos e as mitigações (pergunta 2 em Perguntas abertas).

## Plano de rollout

Aguarda resposta: fases, critérios de avanço e de rollback ainda não foram informados (pergunta 3 em Perguntas abertas).

## Métricas de sucesso

- Meta: taxa de eventos duplicados abaixo de 0,1%, contra os 4% medidos no mês passado.

Como a taxa será medida e onde o resultado será acompanhado aguarda resposta (pergunta 4 em Perguntas abertas).

## Perguntas abertas

1. Qual é o número sequencial deste documento (DD-2026-`<seq>`) e quem são os revisores, com a área de cada um?
2. Quais riscos você enxerga nesta proposta e como cada um será mitigado? Por exemplo: o que acontece com o fluxo se o Redis ficar indisponível?
3. Como o serviço entra em produção? Em fases ou de uma vez, com qual critério de avanço e qual plano de rollback?
4. Como vocês vão medir a taxa de duplicatas e o +5 ms de latência em produção, e quem acompanha?
5. Por que não fazer nada não é aceitável, além do impacto no faturamento que já descrevemos?
