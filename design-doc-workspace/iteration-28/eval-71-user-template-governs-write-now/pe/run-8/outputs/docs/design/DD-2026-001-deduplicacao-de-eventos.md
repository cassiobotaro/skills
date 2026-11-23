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

Os produtores reenviam eventos quando fazem retry, e o pipeline de ingestão recebe essas cópias como se fossem eventos novos. No mês passado medimos 4% de eventos duplicados. As duplicatas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes por causa disso.

## Proposta

Criamos um serviço de deduplicação entre o ingestor e o Kafka. Para cada evento recebido, o serviço consulta a chave idempotente do evento no Redis. Quando a chave já existe, o serviço descarta o evento. Quando a chave é nova, o serviço a guarda no Redis por 24 horas. A meta é manter as duplicatas abaixo de 0,1%.

O serviço fica no caminho crítico da ingestão: todo evento passa por ele antes de chegar ao Kafka. Os detalhes de como a chave é obtida, do formato dos dados no Redis e da ordem entre registrar a chave e publicar no Kafka ainda estão em aberto (ver Perguntas abertas).

### Alternativas consideradas

**Deduplicar no consumidor.** Cada consumidor teria que implementar a própria deduplicação. Descartamos porque a lógica seria reimplementada em cada um deles.

**Idempotência nativa do produtor Kafka.** Descartamos porque ela não cobre o reenvio entre reinícios do produtor, que é um dos casos que geram as duplicatas.

**Não fazer nada.** Manter o pipeline como está significa continuar com cerca de 4% de duplicatas nos relatórios de faturamento.

### Custo aceito

O serviço adiciona um salto ao caminho crítico da ingestão. Estimamos +5 ms de latência por evento. O time aceita esse custo em troca de resolver a duplicidade uma única vez, antes do Kafka.

## Riscos

| Risco | Mitigação |
|---|---|
| Latência de ingestão aumenta cerca de 5 ms (estimativa) por causa do novo salto. | Custo aceito pelo time. Sem mitigação definida. |

Outros riscos e suas mitigações dependem das respostas em Perguntas abertas.

## Plano de rollout

Sem fases, critérios de avanço ou plano de rollback definidos. Ver Perguntas abertas.

## Métricas de sucesso

| Métrica | Hoje | Meta |
|---|---|---|
| Taxa de eventos duplicados | 4% (mês passado) | abaixo de 0,1% |
| Latência adicional na ingestão | não se aplica | estimativa de +5 ms; limite aceitável a definir |

## Perguntas abertas

1. **Chave idempotente.** Quem gera a chave (o produtor ou o ingestor)? Todos os eventos já a carregam? Que formato ela tem?
2. **Janela de 24 horas.** Por que 24 horas? Ela cobre o maior intervalo possível entre um evento e o seu reenvio? O que acontece com um reenvio que chega depois dela?
3. **Falhas do Redis e do serviço.** O que o serviço faz quando o Redis não responde: deixa os eventos passarem (aceitando duplicatas) ou bloqueia a ingestão? E se o próprio serviço cair?
4. **Consistência entre Redis e Kafka.** O serviço registra a chave antes ou depois de publicar no Kafka? Como evita perder um evento ou duplicá-lo se falhar entre os dois passos?
5. **Outros riscos.** Além da latência, quais riscos o time enxerga, e quais mitigações?
6. **Plano de rollout.** Quais são as fases, o critério para avançar entre elas e o critério de rollback?
7. **Medição.** A meta de 0,1% será medida do mesmo jeito que os 4%? O +5 ms é média ou p99, e qual é o limite de latência aceitável?
8. **Escopo.** O que fica fora deste trabalho (por exemplo, a correção das duplicatas já existentes nos relatórios de faturamento)?
9. **Impacto em outras equipes.** Quem precisa revisar ou ser avisado (financeiro, produtores, quem opera o Redis)? Quem são os revisores deste documento?
10. **Numeração e "não fazer nada".** O número DD-2026-001 vale, já que `docs/design/` só tem o template? A descrição de "não fazer nada" acima está correta e completa?
