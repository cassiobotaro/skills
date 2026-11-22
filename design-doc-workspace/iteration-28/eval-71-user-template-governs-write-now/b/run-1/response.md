Rafael, o doc está em `docs/design/deduplicacao-de-eventos.md`. Ele segue as seções do `TEMPLATE.md`, na ordem: Motivação, Proposta, Riscos, Plano de rollout, Métricas de sucesso e Perguntas abertas. O cabeçalho foi preenchido com você como autor, estado Rascunho e data de hoje.

**Seções fora do template.** O template não tem lugar para metas, trade-offs e alternativas, e você me deu esse conteúdo. Criei três subseções para ele, sem mexer na ordem das seções do template:
- "Metas", dentro de Motivação.
- "Trade-offs aceitos", dentro de Proposta. Inclui o +5ms de latência.
- "Alternativas consideradas", também dentro de Proposta. Inclui "não fazer nada", que se resume à dor que você descreveu: 4% de duplicatas e as duas reclamações do financeiro.

Se a arquitetura não aceitar essas subseções, é só removê-las ou mover o conteúdo.

**Seções que ficaram sem conteúdo.** Não inventei nada que você não tenha dito. Riscos e Plano de rollout ficaram com uma linha dizendo que aguardam resposta. Também deixei em aberto os revisores, o que fica fora do escopo e o número do documento (`DD-2026-<seq>`, porque não há outros docs para continuar a sequência).

**Perguntas abertas.** As 7 perguntas estão no fim do doc:
1. Qual é o número do documento?
2. Quem revisa, e de quais áreas?
3. O que fica fora do escopo?
4. O que compõe a chave idempotente, e quem a gera?
5. Quais são os riscos? Em especial, o que o serviço faz se o Redis cair, e o que acontece com um duplicado que chega depois das 24h?
6. Como é o rollout, com critério de avanço e de rollback?
7. Como medimos a taxa de duplicatas? A medição dos 4% usou o mesmo método?

Não incluí diagrama, porque você não descreveu tecnologias ou protocolos além de Redis e Kafka. Posso adicionar um quando você confirmar o fluxo.
