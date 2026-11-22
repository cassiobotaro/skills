# Serviço de deduplicação de eventos · DD-2026-<seq>

| | |
|---|---|
| **Documento** | DD-2026-<seq> (número aguarda resposta, ver Perguntas abertas) |
| **Estado** | Rascunho |
| **Autores** | Rafael Nunes |
| **Revisores** | Aguarda resposta (ver Perguntas abertas) |
| **Criado em** | 2026-11-22 |
| **Última atualização** | 2026-11-22 |

## Motivação

O pipeline de ingestão recebe eventos duplicados dos produtores, que reenviam o mesmo evento quando fazem retry. No mês passado medimos 4% de duplicatas. As duplicatas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes.

## Proposta

Um novo serviço de deduplicação fica entre o ingestor e o Kafka. Para cada evento recebido, o serviço consulta a chave idempotente do evento no Redis. Se a chave já existe, o serviço descarta o evento. Se não existe, o serviço guarda a chave no Redis por 24 horas e deixa o evento seguir para o Kafka.

### Trade-offs aceitos

- ✓ A deduplicação acontece uma vez, num ponto só, em vez de em cada consumidor.
- ✓ Cobre o reenvio de retry mesmo quando o produtor reinicia entre as tentativas.
- ✗ O serviço vira mais um salto no caminho crítico da ingestão. A estimativa é de +5ms de latência (estimativa, sem medição).

### Alternativas consideradas

| Alternativa | Por que perdeu |
|---|---|
| Não fazer nada | Mantém os 4% de duplicatas e o erro nos relatórios de faturamento, que o financeiro já reclamou duas vezes. |
| Deduplicar no consumidor | Cada consumidor teria que reimplementar a deduplicação. Descartada. |
| Idempotência nativa do produtor Kafka | Não cobre o reenvio entre reinícios do produtor. Descartada. |
| **Serviço de deduplicação com Redis (escolhida)** | Ver os trade-offs acima. |

## Riscos

Aguarda resposta do autor: os riscos desta proposta e suas mitigações ainda não foram levantados. Ver pergunta 3 em Perguntas abertas.

## Plano de rollout

Aguarda resposta do autor: fases, critério de avanço e rollback não foram definidos. Ver pergunta 4 em Perguntas abertas.

## Métricas de sucesso

- Duplicatas abaixo de 0,1% (hoje: 4%, medido no mês passado).

Como e onde essa taxa será medida aguarda resposta do autor. Ver pergunta 5 em Perguntas abertas.

## Perguntas abertas

1. Qual é o número deste documento (`DD-2026-<seq>`) e quem são os revisores, com a área de cada um? O time de arquitetura revisa?
2. Qual é a chave idempotente de um evento e quem a gera (o produtor ou o ingestor)?
3. Quais riscos o time enxerga, e como mitiga cada um? Em particular: o que o serviço faz quando o Redis está indisponível, deixa o evento passar ou o rejeita?
4. Como a proposta entra em produção: de uma vez ou em fases? Qual o critério para avançar e qual o rollback?
5. Como e onde a taxa de duplicatas será medida, e em que prazo se espera chegar a menos de 0,1%?
6. O +5ms de latência vem de medição ou de estimativa? Existe um limite de latência que a ingestão não pode ultrapassar?
7. O que é explicitamente não objetivo deste trabalho?
