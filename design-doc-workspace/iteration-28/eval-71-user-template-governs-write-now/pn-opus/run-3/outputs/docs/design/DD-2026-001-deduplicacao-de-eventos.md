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

O pipeline de ingestão recebe eventos duplicados dos produtores. As duplicatas vêm do reenvio em retry, quando o produtor envia de novo um evento que o pipeline já tinha recebido.

No mês passado medimos 4% de eventos duplicados. As duplicatas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes.

## Proposta

Vamos construir um serviço de deduplicação que fica entre o ingestor e o Kafka. O serviço identifica cada evento pela sua chave idempotente, um identificador que se repete quando o produtor reenvia o mesmo evento (a origem da chave é a pergunta 1 em [Perguntas abertas](#perguntas-abertas)). O serviço guarda a chave de cada evento no Redis por 24 horas:

- quando a chave ainda não está no Redis, o serviço registra a chave e publica o evento no Kafka;
- quando a chave já está no Redis, o serviço descarta o evento.

Com isso, um reenvio feito dentro de 24 horas do envio original não chega ao Kafka.

### Trade-off aceito

- ✓ A deduplicação acontece em um único ponto, antes do Kafka. Todos os consumidores recebem o fluxo já limpo, sem reimplementar nada.
- ✓ A deduplicação cobre reenvios feitos depois de um reinício do produtor, porque a chave fica guardada fora do produtor.
- ✗ O serviço adiciona mais um salto no caminho crítico da ingestão. Estimamos +5 ms de latência por evento, e o time aceitou esse custo.
- ✗ A janela é de 24 horas. Um reenvio que chegue depois disso passa como evento novo (ver [Perguntas abertas](#perguntas-abertas)).

### Alternativas consideradas

| Alternativa | Por que perdeu |
|---|---|
| Não fazer nada | Mantém os 4% de duplicatas inflando os relatórios de faturamento, problema que o financeiro já levou ao time duas vezes. |
| Deduplicar no consumidor | Cada consumidor teria que reimplementar a deduplicação. Descartada. |
| Idempotência nativa do produtor Kafka | Não cobre reenvio entre reinícios do produtor, que é parte do problema. Descartada. |
| **Serviço de deduplicação entre ingestor e Kafka (escolhida)** | Resolve nos dois casos acima, ao custo de um salto extra estimado em +5 ms. |

## Riscos

O risco já identificado e aceito é a latência: o serviço entra no caminho crítico da ingestão, com custo estimado de +5 ms.

Os demais riscos e suas mitigações ainda não foram levantados. As perguntas 3, 4 e 5 em [Perguntas abertas](#perguntas-abertas) listam os pontos que esta seção precisa responder antes da revisão.

## Plano de rollout

Ainda não definido. Ver a pergunta 6 em [Perguntas abertas](#perguntas-abertas).

## Métricas de sucesso

| Métrica | Hoje | Meta |
|---|---|---|
| Eventos duplicados que chegam ao Kafka | 4% (mês passado) | Abaixo de 0,1% |

A forma de medir essa taxa depois da entrada do serviço está na pergunta 7 em [Perguntas abertas](#perguntas-abertas).

## Perguntas abertas

1. **Chave idempotente.** De onde ela vem? Todos os produtores já enviam uma chave estável entre reenvios, ou parte deles precisa passar a enviar? O que o serviço faz com um evento sem chave?
2. **Janela de 24 horas.** Que dado sustenta as 24 horas? Sabemos que fração dos reenvios chega depois desse prazo?
3. **Indisponibilidade do Redis.** Se o Redis cair ou ficar lento, o serviço deixa os eventos passarem (aceitando duplicatas) ou bloqueia a ingestão (aceitando perda de disponibilidade)?
4. **Falha entre registrar a chave e publicar no Kafka.** Se o serviço registrar a chave antes de publicar e a publicação falhar, o reenvio seguinte seria descartado e o evento se perderia. Em que ordem o serviço faz essas duas operações, e o que acontece quando uma delas falha?
5. **Capacidade e escala.** Qual é o volume de eventos por segundo e quanto de memória o Redis precisa para 24 horas de chaves? O Redis é novo ou compartilhado com outro time?
6. **Rollout.** O serviço entra de uma vez ou em fases (por exemplo, por produtor, ou primeiro em modo que só mede sem descartar)? Qual é o critério para avançar de fase e como fazemos rollback?
7. **Medição.** Como mediremos a taxa de duplicatas depois do serviço, e é a mesma medição que deu os 4%? Qual métrica de latência confirma ou derruba a estimativa de +5 ms?
8. **Revisores.** Quem revisa? Candidatos pelas áreas tocadas: o time dono do Kafka e do Redis, os times produtores e o financeiro como consumidor dos relatórios.
9. **Dados históricos.** Os relatórios de faturamento já emitidos com duplicatas precisam ser corrigidos, ou isso fica fora do escopo deste serviço?
