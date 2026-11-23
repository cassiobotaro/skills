# Serviço de deduplicação de eventos · DD-2026-001

| | |
|---|---|
| **Documento** | DD-2026-001 |
| **Estado** | Rascunho |
| **Autores** | Rafael Nunes |
| **Revisores** | (a definir, ver [pergunta 1](#perguntas-abertas)) |
| **Criado em** | 2026-11-23 |
| **Última atualização** | 2026-11-23 |

## Motivação

O pipeline de ingestão recebe eventos duplicados dos produtores. A duplicata nasce do reenvio em retry: o produtor manda o mesmo evento de novo e o pipeline aceita as duas cópias.

No mês passado, medimos 4% de duplicatas. Esses eventos repetidos inflam os relatórios de faturamento, e o time financeiro já reclamou duas vezes.
## Proposta

Vamos construir um serviço de deduplicação que fica entre o ingestor e o Kafka. Todo evento que o ingestor publica passa por ele antes de chegar ao Kafka.

Fluxo para cada evento:

1. O ingestor entrega o evento ao serviço de deduplicação.
2. O serviço lê a chave idempotente do evento, isto é, o identificador que se repete em todo reenvio do mesmo evento.
3. O serviço consulta essa chave no Redis.
   - Chave ausente: o serviço grava a chave no Redis com expiração de 24h e publica o evento no Kafka.
   - Chave presente: o serviço descarta o evento, que é um reenvio de algo já publicado.

A janela de 24h define o alcance da deduplicação: o serviço só reconhece como repetido um reenvio que chegue dentro de 24h do evento original.

A deduplicação acontece num único ponto, antes do Kafka, e por isso nenhum consumidor precisa tratar duplicatas por conta própria.

## Trade-offs e alternativas consideradas

> Seção acrescentada ao template: o time discutiu alternativas e aceitou um custo explícito, e o template não tem outro lugar para registrar isso.

### O que a proposta custa

- ✓ Remove as duplicatas num ponto só, antes de qualquer consumidor.
- ✓ Cobre o reenvio que acontece depois de um reinício do produtor, caso que a idempotência nativa do Kafka não cobre, desde que a chave se repita no reenvio ([pergunta 2](#perguntas-abertas)).
- ✗ Acrescenta mais um salto no caminho crítico da ingestão. Estimamos +5ms de latência por evento, e o time aceitou esse custo.

### Alternativas

**Não fazer nada.** Descartada: os 4% de duplicatas continuam inflando os relatórios de faturamento, que já geraram duas reclamações do financeiro.

**Deduplicar no consumidor.** Cada consumidor do Kafka descartaria os eventos repetidos que recebe. Descartada porque cada consumidor teria que reimplementar a deduplicação.

**Idempotência nativa do produtor Kafka.** Descartada porque não cobre o reenvio entre reinícios do produtor.

**Serviço de deduplicação entre o ingestor e o Kafka (escolhida).** Resolve nos dois pontos em que as outras falham, ao custo do salto extra descrito acima.

## Riscos

| Risco | Mitigação |
|---|---|
| Latência maior na ingestão: o serviço é mais um salto no caminho crítico, estimado em +5ms. | Custo aceito pelo time. O orçamento de latência e o alarme ainda não estão definidos ([pergunta 5](#perguntas-abertas)). |

Os demais riscos da proposta, como o comportamento quando o Redis ou o próprio serviço ficam indisponíveis, dependem de decisões listadas nas [perguntas abertas](#perguntas-abertas) (3, 4 e 6).

## Plano de rollout

As fases, os critérios de avanço e o caminho de rollback dependem das [perguntas 7 e 8](#perguntas-abertas).

## Métricas de sucesso

| Métrica | Hoje | Meta |
|---|---|---|
| Duplicatas nos eventos ingeridos | 4% (mês passado) | abaixo de 0,1% |

A forma de medir a meta deve ser a mesma que produziu os 4% ([pergunta 9](#perguntas-abertas)).

## Perguntas abertas

1. **Revisores.** Quem revisa este documento e de quais áreas? Sugestões a confirmar: o time dono do Redis e do Kafka, que recebe a nova carga, e alguém do financeiro, que reportou o problema.
2. **Origem da chave idempotente.** Quem gera a chave: o produtor, o ingestor ou o próprio serviço (por exemplo, a partir de um hash do conteúdo)? Todos os produtores já enviam uma chave estável entre reenvios?
3. **Redis indisponível.** Se o serviço não conseguir consultar o Redis, ele deixa o evento passar (aceitando duplicatas) ou bloqueia a ingestão até o Redis voltar?
4. **Falha entre gravar a chave e publicar no Kafka.** Se o serviço grava a chave no Redis e a publicação no Kafka falha, o reenvio seguinte seria descartado e o evento se perderia. Qual a ordem de gravação e o tratamento desse caso?
5. **Orçamento de latência.** Os +5ms são uma estimativa. Há um limite de latência que, se ultrapassado, conta como falha? Como pretendemos medir?
6. **Janela de 24h.** De onde vem o valor? Os reenvios que geram os 4% acontecem todos dentro de 24h, ou parte deles fica de fora?
7. **Rollout.** O serviço entra de uma vez ou em fases (por produtor, por percentual de tráfego, em modo sombra só contando duplicatas)? Qual o critério para avançar de fase?
8. **Rollback.** Como o ingestor volta a publicar direto no Kafka se o serviço der problema?
9. **Medição.** Como os 4% foram medidos, e o serviço deve expor uma contagem de eventos descartados para acompanhar a meta?
10. **Dimensionamento.** Qual o volume de eventos por segundo e quanto de memória o Redis precisa para guardar 24h de chaves?
11. **Dados históricos.** Os relatórios de faturamento já afetados pelas duplicatas passadas serão corrigidos, ou isso fica fora do escopo deste serviço?
