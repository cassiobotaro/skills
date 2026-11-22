# Serviço de deduplicação de eventos · DD-2026-001

| | |
|---|---|
| **Documento** | DD-2026-001 |
| **Estado** | Rascunho |
| **Autores** | Rafael Nunes |
| **Revisores** | Aguardando resposta, ver pergunta 1 |
| **Criado em** | 2026-11-22 |
| **Última atualização** | 2026-11-22 |

## Motivação

O pipeline de ingestão recebe eventos duplicados dos produtores, que reenviam o mesmo evento quando fazem retry. No mês passado medimos 4% de eventos duplicados. As duplicatas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes.

## Proposta

Criamos um serviço de deduplicação entre o ingestor e o Kafka. Para cada evento recebido, o serviço consulta a chave idempotente do evento no Redis. Se a chave já existe, o serviço descarta o evento. Se não existe, o serviço guarda a chave no Redis por 24 horas e o evento segue para o Kafka.

A deduplicação acontece uma vez, antes do Kafka, e nenhum consumidor precisa reimplementá-la. A janela de 24 horas define o alcance da garantia: um reenvio que chegue depois de 24 horas do primeiro evento não é reconhecido como repetido.

O custo aceito é um salto a mais no caminho crítico da ingestão. Estimamos +5 ms de latência por evento. Esse número é uma estimativa.

Detalhes de projeto que a proposta ainda não fixa (origem da chave idempotente, ordem entre gravar a chave e publicar no Kafka, comportamento quando o Redis estiver indisponível) estão nas Perguntas abertas 2, 3 e 4.

## Alternativas consideradas

Este template não tem seção de alternativas. Incluímos esta seção para registrar as opções discutidas, mantendo a ordem das demais seções do template.

- **Não fazer nada.** As duplicatas continuam inflando os relatórios de faturamento. O motivo para rejeitar esta alternativa aguarda resposta, ver pergunta 5.
- **Deduplicar no consumidor.** Descartada. Cada consumidor teria que reimplementar a deduplicação.
- **Usar a idempotência nativa do produtor Kafka.** Descartada. Ela não cobre o reenvio entre reinícios do produtor, que é parte do problema que queremos resolver.

## Riscos

O serviço adiciona um salto ao caminho crítico da ingestão, estimado em +5 ms de latência. A proposta aceita esse custo em troca de deduplicar em um único ponto.

Os demais riscos e suas mitigações aguardam resposta, ver pergunta 4.

## Plano de rollout

Aguarda resposta, ver pergunta 6.

## Métricas de sucesso

- Taxa de eventos duplicados abaixo de 0,1%. A linha de base é 4%, medida no mês passado.

Os demais números (latência aceitável no caminho crítico, por exemplo) aguardam resposta, ver pergunta 7.

## Perguntas abertas

1. **Revisores.** Quem revisa este documento pelo time de arquitetura e quais outros times são impactados (financeiro, donos dos produtores, donos dos consumidores)?
2. **Chave idempotente.** Quem gera a chave de cada evento, o produtor ou o ingestor? Todos os produtores já enviam uma chave estável entre retries?
3. **Ordem das operações.** O serviço grava a chave no Redis antes ou depois de publicar no Kafka? Se a publicação falhar depois de a chave ser gravada, o retry do produtor seria descartado como duplicata e o evento se perderia. Como tratamos esse caso?
4. **Riscos e mitigações.** O que acontece com a ingestão se o Redis ficar indisponível: o serviço bloqueia a ingestão, deixa os eventos passarem sem deduplicar ou descarta? Há outros riscos que o time já identificou, como dimensionamento do Redis para 24 horas de chaves ou o novo serviço virar ponto único de falha?
5. **Não fazer nada.** O time quer registrar algum argumento além do impacto no faturamento para rejeitar esta alternativa?
6. **Rollout.** Como o serviço entra em produção: em fases, com qual critério de avanço de uma fase para a seguinte e qual critério de rollback?
7. **Métricas.** Além da taxa de duplicatas, quais números acompanhamos (latência p99 do caminho crítico, taxa de descarte, falhas do Redis) e com quais limites?
8. **Numeração.** `docs/design/` só tem o template. DD-2026-001 é a primeira numeração do ano ou existe sequência em outro lugar (wiki do time de arquitetura)?
9. **Janela de 24 horas.** Por que 24 horas? Existe um dado sobre o intervalo máximo entre um evento e seus reenvios?
