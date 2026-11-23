# Serviço de deduplicação de eventos · DD-2026-001

| | |
|---|---|
| **Documento** | DD-2026-001 |
| **Estado** | Rascunho |
| **Autores** | Rafael Nunes |
| **Revisores** | A definir (ver [Perguntas abertas](#perguntas-abertas)) |
| **Criado em** | 2026-11-23 |
| **Última atualização** | 2026-11-23 |

## Motivação

O pipeline de ingestão recebe eventos duplicados dos produtores, que reenviam o mesmo evento quando fazem retry. No mês passado medimos 4% de eventos duplicados. As duplicatas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes.

Hoje nada no caminho entre o ingestor e o Kafka descarta esses repetidos, então eles chegam a todos os consumidores.

## Proposta

Criar um serviço de deduplicação que fica entre o ingestor e o Kafka. Para cada evento recebido, o serviço consulta a chave idempotente do evento no Redis:

- Se a chave não existe, o serviço a grava no Redis com validade de 24h e encaminha o evento ao Kafka.
- Se a chave já existe, o evento é um repetido e o serviço o descarta.

Como o serviço fica antes do Kafka, a deduplicação acontece uma vez só, e os consumidores recebem o fluxo já limpo. A janela de deduplicação é de 24h: um reenvio dentro desse prazo é detectado, e um reenvio depois dele não é coberto por esta proposta.

O serviço entra no caminho crítico da ingestão. Estimamos que isso acrescente 5ms de latência por evento. A equipe aceitou esse custo em troca de resolver as duplicatas na origem.

### Alternativas consideradas

O documento acrescenta esta seção ao template, porque as alternativas discutidas não têm outro lugar nele.

**Não fazer nada.** Descartada pela dor descrita na Motivação: 4% de duplicatas inflando o faturamento, com duas reclamações do financeiro.

**Deduplicar no consumidor.** Cada consumidor teria que reimplementar a deduplicação. Descartada por esse motivo.

**Idempotência nativa do produtor Kafka.** Não cobre o reenvio entre reinícios do produtor, que é parte do problema. Descartada por essa lacuna.

**Serviço entre o ingestor e o Kafka (escolhida).** Resolve a deduplicação em um ponto só, ao custo de mais um salto no caminho crítico.

## Riscos

**Latência no caminho crítico (aceito).** O serviço adiciona um salto à ingestão, estimado em +5ms. A equipe aceitou esse custo. O número é uma estimativa, ainda não medida.

Os demais riscos da proposta e suas mitigações ainda não foram levantados. Ver [Perguntas abertas](#perguntas-abertas).

## Plano de rollout

O plano de fases, os critérios de avanço e o de rollback ainda não foram definidos. Ver [Perguntas abertas](#perguntas-abertas).

## Métricas de sucesso

| Métrica | Hoje | Meta |
|---|---|---|
| Taxa de eventos duplicados | 4% (medido no mês passado) | abaixo de 0,1% |
| Latência adicionada à ingestão | n/a | +5ms (estimativa aceita) |

## Perguntas abertas

Perguntas para o Rafael responder antes de o documento sair de rascunho:

1. **Chave idempotente.** Qual campo, ou combinação de campos, forma a chave de cada evento? Os produtores já a enviam, ou o serviço precisa derivá-la?
2. **Indisponibilidade do Redis.** O que o serviço faz quando o Redis não responde: encaminha os eventos sem deduplicar ou bloqueia a ingestão?
3. **Falhas do próprio serviço.** Quais outros modos de falha a equipe enxerga (por exemplo, a perda dos dados do Redis) e como cada um é mitigado?
4. **Atomicidade.** O que acontece com a chave se o serviço a grava e falha antes de entregar o evento ao Kafka?
5. **Rollout.** Em quais fases o serviço entra em produção, com que critério se avança de uma fase para a seguinte e como se faz o rollback?
6. **Origem da meta.** A meta de 0,1% vale para qual janela de medição? E por que 24h é a validade da chave: ela cobre o intervalo máximo entre um evento e seus retries?
7. **Estimativa de latência.** Em que se baseia o +5ms, e existe um teto de latência que a ingestão não pode ultrapassar?
8. **Capacidade do Redis.** Qual o volume de eventos por dia e a memória que as chaves de 24h vão ocupar? O Redis é um cluster existente ou novo?
9. **Observabilidade.** Como o serviço expõe a contagem de descartados, para medir a taxa de duplicatas depois do rollout?
10. **Revisores.** Quem revisa este documento, e quais equipes são impactadas (financeiro, donos dos produtores, consumidores do Kafka, quem opera o Redis)?
