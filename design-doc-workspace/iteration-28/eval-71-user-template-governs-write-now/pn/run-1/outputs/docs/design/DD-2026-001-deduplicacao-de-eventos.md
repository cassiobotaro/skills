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

O pipeline de ingestão recebe eventos duplicados dos produtores, que reenviam o mesmo evento quando fazem retry. No mês passado medimos 4% de duplicatas.

Essas duplicatas inflam os relatórios de faturamento. O financeiro já reclamou duas vezes.

## Proposta

Vamos criar um serviço de deduplicação que fica entre o ingestor e o Kafka. Para cada evento recebido, o serviço consulta no Redis a chave idempotente do evento. Se a chave já existe, o serviço descarta o evento. Se não existe, o serviço guarda a chave no Redis com validade de 24 horas e deixa o evento seguir para o Kafka.

Componentes:

- **Ingestor**: continua recebendo os eventos dos produtores e passa a entregá-los ao serviço de deduplicação, em vez de publicá-los direto no Kafka.
- **Serviço de deduplicação** (novo): decide se o evento é novo ou repetido, a partir da chave idempotente.
- **Redis**: guarda as chaves idempotentes por 24 horas.
- **Kafka**: recebe apenas os eventos que o serviço deixou passar.

Como a deduplicação acontece antes do Kafka, os consumidores não precisam implementar nada. A janela de 24 horas define o alcance da garantia: um reenvio que chegue depois que a chave expirou não será reconhecido como repetido.

### Alternativas consideradas

O template não tem uma seção para alternativas. Mantive a ordem e as seções do template e registrei as alternativas aqui, dentro da Proposta.

| Alternativa | Por que foi descartada |
|---|---|
| Deduplicar no consumidor | Cada consumidor teria que reimplementar a deduplicação. |
| Usar a idempotência nativa do produtor Kafka | Não cobre o reenvio entre reinícios do produtor. |

### Trade-off aceito

O serviço adiciona mais um salto no caminho crítico da ingestão. Estimamos +5 ms de latência por evento. Aceitamos esse custo em troca de resolver a duplicidade em um só lugar, sem mudança nos consumidores.

## Riscos

| Risco | Mitigação |
|---|---|
| Latência: o novo salto adiciona cerca de 5 ms (estimativa) ao caminho crítico da ingestão. | Aceito. Vamos medir a latência real no rollout e comparar com a estimativa. |
| Duplicatas fora da janela: um reenvio após 24 horas não é detectado. | Aceito como limite do desenho. A janela de 24 horas é a que escolhemos. |
| Dependência do Redis e do novo serviço no caminho crítico. | Em aberto. Ver Perguntas abertas. |

## Plano de rollout

Em aberto. As fases, os critérios de avanço e os critérios de rollback ainda não foram definidos. Ver Perguntas abertas.

## Métricas de sucesso

| Métrica | Hoje | Meta |
|---|---|---|
| Taxa de eventos duplicados | 4% (mês passado) | abaixo de 0,1% |
| Latência adicionada na ingestão | não se aplica | +5 ms (estimativa a confirmar com medição) |

## Perguntas abertas

1. **Falha do Redis.** Se o Redis ou o serviço de deduplicação ficar indisponível, o ingestor deixa os eventos passarem (e aceita duplicatas) ou bloqueia a ingestão? Qual é o comportamento esperado?
2. **Chave idempotente.** Quem gera a chave de cada evento? Os produtores já a enviam hoje ou ela precisa ser definida junto com eles? Qual é o formato?
3. **Ordem das operações.** O serviço grava a chave no Redis antes ou depois de publicar no Kafka? Se a publicação falhar depois da gravação, o retry do produtor seria descartado e o evento se perderia. Como tratamos isso?
4. **Rollout.** Em quais fases o serviço entra em produção (por produtor, por percentual de tráfego, em modo sombra)? Qual critério permite avançar de fase e qual dispara o rollback?
5. **Dimensionamento do Redis.** Qual é o volume de eventos por dia e, portanto, o tamanho esperado do conjunto de chaves em 24 horas?
6. **Alternativa "não fazer nada".** Existe um custo estimado das duplicatas para o financeiro (ou um paliativo, como correção nos relatórios) que sirva de comparação com o custo do novo serviço?
7. **Fora de escopo.** Há algo que este serviço deliberadamente não vai cobrir (por exemplo, deduplicação além de 24 horas ou eventos de outras origens)?
8. **Revisores e numeração.** Quem revisa este documento? E o número DD-2026-001 está correto, ou já existe outro documento com essa sequência fora deste repositório?
