Salvei o rascunho em `docs/design/deduplicacao-de-eventos.md`. Ele segue o `TEMPLATE.md` com as mesmas seções e na mesma ordem: Motivação, Proposta, Riscos, Plano de rollout, Métricas de sucesso e Perguntas abertas. Duas seções ficaram sem conteúdo, porque você não me deu o material para elas.

**O que está preenchido**
- **Motivação:** os 4% de duplicatas, o reenvio em retry e as duas reclamações do financeiro.
- **Proposta:** o serviço entre o ingestor e o Kafka, com a chave idempotente guardada no Redis por 24h. Incluí o trade-off aceito, os +5ms de latência no caminho crítico.
- **Métricas de sucesso:** duplicatas abaixo de 0,1%.

**Um desvio do template, para você aceitar ou não**
O template não tem lugar para alternativas. Criei uma subseção "Alternativas consideradas" dentro de Proposta, com as duas que você descreveu e o motivo de cada descarte. Se a arquitetura preferir isso em outro lugar, é só mover.

**O que ficou aguardando você**
Não inventei conteúdo para estas seções. Cada uma tem uma linha dizendo que aguarda resposta, apontando para Perguntas abertas.
1. **Riscos:** o que pode dar errado e como mitigar? Por exemplo, o que acontece com a ingestão se o serviço ou o Redis ficarem fora do ar?
2. **Plano de rollout:** quais fases, qual critério de avanço e qual critério de rollback?
3. **Latência:** os +5ms são só estimativa. Existe um limite máximo aceitável e como vamos medir o valor real?
4. **Cabeçalho:** qual o número de sequência do DD (deixei `DD-2026-<seq>`) e quem são os revisores?
5. **Fazer nada:** manter o cenário atual foi descartado só pelo custo das duplicatas no faturamento, ou há outro motivo a registrar?

Me responda essas perguntas e eu completo o documento. O estado continua "Rascunho" até lá.
