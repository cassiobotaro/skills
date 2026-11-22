# Serviço de deduplicação de eventos · DD-2026-<seq>

| | |
|---|---|
| **Documento** | DD-2026-<seq> |
| **Estado** | Rascunho |
| **Autores** | Rafael Nunes |
| **Revisores** | Ver Perguntas abertas |
| **Criado em** | 2026-11-22 |
| **Última atualização** | 2026-11-22 |

## Motivação

O pipeline de ingestão recebe eventos duplicados dos produtores, que reenviam o mesmo evento quando fazem retry. No mês passado medimos 4% de eventos duplicados. As duplicatas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes.

## Proposta

Um novo serviço de deduplicação fica entre o ingestor e o Kafka. Para cada evento recebido, o serviço consulta a chave idempotente do evento no Redis. Se a chave já existe, o serviço descarta o evento. Se não existe, o serviço guarda a chave no Redis com validade de 24 horas e encaminha o evento ao Kafka.

Com isso, a deduplicação acontece uma única vez, antes do Kafka, e nenhum consumidor precisa tratá-la.

## Alternativas consideradas

- **Não fazer nada.** Os relatórios de faturamento continuam inflados por cerca de 4% de duplicatas e o financeiro continua reclamando. É a dor descrita na Motivação.
- **Deduplicar no consumidor.** Descartada: cada consumidor teria que reimplementar a deduplicação.
- **Idempotência nativa do produtor Kafka.** Descartada: ela não cobre o reenvio entre reinícios do produtor.
- **Serviço de deduplicação entre o ingestor e o Kafka.** Escolhida. Resolve o problema num único ponto e cobre o reenvio por retry.

## Trade-offs aceitos

- ✓ A deduplicação fica num só lugar, e os consumidores não a reimplementam.
- ✓ Cobre o reenvio entre reinícios do produtor, que a idempotência nativa do Kafka não cobre.
- ✗ Um salto a mais no caminho crítico da ingestão, com estimativa de +5 ms de latência. O time aceitou esse custo.

## Riscos

O único risco que o time levantou até agora é a latência adicional no caminho crítico da ingestão (+5 ms estimados, medição ainda não feita). Os demais riscos e suas mitigações estão em [Perguntas abertas](#perguntas-abertas).

## Plano de rollout

O plano ainda não foi definido. Ver [Perguntas abertas](#perguntas-abertas).

## Métricas de sucesso

| Métrica | Hoje | Meta |
|---|---|---|
| Taxa de eventos duplicados | 4% (mês passado) | Abaixo de 0,1% |
| Latência adicional na ingestão | não se aplica | +5 ms (estimativa) |

A meta de duplicatas é o critério de sucesso. Os +5 ms são uma estimativa do custo aceito, não uma meta.

## Perguntas abertas

Rafael não pôde responder durante a escrita; estas perguntas ficaram em aberto.

1. **Número do documento e revisores.** Qual é o número sequencial do DD (`DD-2026-<seq>`)? Quem revisa, e de quais áreas (por exemplo, arquitetura, financeiro, quem opera o Redis e o Kafka)?
2. **Riscos.** O que pode dar errado além da latência? Em particular, o que acontece com a ingestão se o Redis ficar indisponível ou perder dados, e o serviço deve deixar passar ou bloquear os eventos nesse caso? Como o time mitiga cada risco?
3. **Plano de rollout.** Como o serviço entra em produção, em fases? Qual o critério para avançar de fase e qual o plano de rollback?
4. **Chave idempotente.** De onde vem a chave de cada evento (os produtores a enviam ou o ingestor a calcula)?
5. **Medição.** Como e onde a taxa de duplicatas será medida depois do rollout, e em que prazo se espera atingir a meta de 0,1%?
6. **Fora de escopo.** O que este trabalho deliberadamente não resolve?
7. **Janela de 24 h.** Por que 24 horas? Duplicatas que chegam depois dessa janela passam, e o time aceita isso?
