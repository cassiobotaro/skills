# Serviço de deduplicação de eventos · DD-2026-<seq>

| | |
|---|---|
| **Documento** | DD-2026-<seq> (a definir, ver Perguntas abertas) |
| **Estado** | Rascunho |
| **Autores** | Rafael Nunes |
| **Revisores** | A definir (ver Perguntas abertas) |
| **Criado em** | 2026-11-22 |
| **Última atualização** | 2026-11-22 |

## Motivação

O pipeline de ingestão recebe eventos duplicados dos produtores, que reenviam o mesmo evento quando fazem retry. No mês passado medimos 4% de duplicatas. Elas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes.

Hoje nada no caminho de ingestão descarta esses repetidos antes de chegarem ao Kafka.

## Proposta

Criamos um serviço de deduplicação que fica entre o ingestor e o Kafka. Para cada evento recebido, o serviço consulta a chave idempotente do evento no Redis. Se a chave já existe, o serviço descarta o evento. Se não existe, o serviço guarda a chave por 24 horas e repassa o evento ao Kafka.

### Trade-offs

- ✓ A deduplicação acontece uma só vez, num ponto central, e nenhum consumidor precisa reimplementá-la.
- ✓ Cobre o reenvio de eventos entre reinícios do produtor.
- ✗ O serviço é mais um salto no caminho crítico da ingestão. Estimamos +5 ms de latência. Aceitamos esse custo em troca da redução de duplicatas.

## Alternativas consideradas

| Alternativa | Resultado | Motivo |
|---|---|---|
| Deduplicar no consumidor | ✗ Descartada | Cada consumidor teria que reimplementar a deduplicação. |
| Idempotência nativa do produtor Kafka | ✗ Descartada | Não cobre o reenvio entre reinícios do produtor. |
| Não fazer nada | ✗ Descartada | Os produtores seguem enviando duplicatas (4% no mês passado), o faturamento segue inflado e o financeiro segue reclamando. |
| **Serviço de deduplicação entre ingestor e Kafka (escolhida)** | ✓ | Ver Proposta. |

## Riscos

O único risco que a conversa estabeleceu é a latência: o novo salto no caminho crítico da ingestão acrescenta cerca de 5 ms (estimativa). A mitigação e os demais riscos estão em Perguntas abertas.

## Plano de rollout

Ainda não definido. As fases, os critérios de avanço e o plano de rollback estão em Perguntas abertas.

## Métricas de sucesso

| Métrica | Hoje | Meta |
|---|---|---|
| Proporção de eventos duplicados | 4% (mês passado) | Abaixo de 0,1% |

O custo aceito, +5 ms de latência na ingestão, é uma estimativa. Como vamos medi-lo está em Perguntas abertas.

## Perguntas abertas

1. **ID e revisores:** qual é o número de sequência deste documento (DD-2026-?) e quem deve revisar (arquitetura, financeiro, quem opera o Redis e o Kafka)?
2. **Chave idempotente:** de onde vem a chave de cada evento? Os produtores já a enviam ou o ingestor a calcula?
3. **Falha do Redis:** o que o serviço faz se o Redis ficar indisponível: deixa os eventos passarem (e aceita duplicatas) ou bloqueia a ingestão?
4. **Duplicatas após 24h:** um reenvio que chegue depois da janela de 24h passa. Esse limite é aceitável? Por que 24h?
5. **Riscos e mitigações:** além da latência, que riscos a equipe enxerga (disponibilidade do novo serviço, capacidade e custo do Redis, perda de eventos legítimos por colisão de chave) e como cada um é mitigado?
6. **Rollout:** como o serviço entra em produção (fases, por produtor, em modo sombra antes de descartar)? Qual o critério de avanço e como se faz rollback?
7. **Medição:** como medimos a taxa de duplicatas (os 4% e a meta de 0,1%) e a latência real, e com que painel ou alerta?
8. **Fora de escopo:** há algo que o time espera deste serviço e ele não cobre, por exemplo duplicatas já gravadas ou o reprocessamento dos relatórios passados?
9. **Quem é impactado:** que outras equipes ou sistemas são afetados (financeiro, produtores, plataforma)?
