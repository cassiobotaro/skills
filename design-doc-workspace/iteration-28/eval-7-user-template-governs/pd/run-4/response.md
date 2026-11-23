Salvei o doc em `docs/design/dd-2026-001-deduplicacao-de-eventos.md`, no estado Rascunho. Ele segue as seções do `TEMPLATE.md` na ordem do template, e não criei nenhuma seção nova.

- **ID:** `docs/design/` só tinha o template, então usei DD-2026-001 como primeiro doc. Se o time numera de outro jeito, é só trocar.
- **Alternativas e trade-off:** o template não tem seção para eles, e você me deu três. Pus como subseções dentro de **Proposta**: o trade-off dos +5 ms, o descarte do consumidor, o descarte da idempotência nativa do Kafka e "não fazer nada". Assim o formato continua o que a arquitetura aceita.
- **Diagrama:** só tem os componentes que você citou (produtores, ingestor, serviço, Redis, Kafka). Deixei de fora tecnologias e protocolos que você não disse.
- **Dados do texto:** escrevi "outubro de 2026" no lugar de "mês passado", para o número não perder o sentido com o tempo.

Você não me deu o conteúdo de algumas seções, e não inventei nada para preenchê-las. Elas apontam para **Perguntas abertas**, onde ficaram estas perguntas para você responder:

1. **Riscos:** o que pode dar errado além dos +5 ms? Por exemplo, o que o serviço faz com o evento quando o Redis não responde?
2. **Rollout:** quais são as fases, o critério de avanço e o critério de rollback?
3. **Latência:** os +5 ms foram medidos ou projetados? Acima de quanto o custo deixa de ser aceitável?
4. **Chave idempotente:** quem gera a chave e em que ponto do fluxo?
5. **Revisores:** quem entra no campo, que está vazio?

Me passe as respostas e eu preencho as seções e tiro as perguntas respondidas da lista.
