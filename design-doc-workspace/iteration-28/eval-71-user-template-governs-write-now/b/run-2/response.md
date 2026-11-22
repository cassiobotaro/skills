Rafael, salvei o doc em `docs/design/servico-de-deduplicacao-de-eventos.md`. Ele segue o `TEMPLATE.md` na ordem original: Motivação, Proposta, Riscos, Plano de rollout, Métricas de sucesso e Perguntas abertas. O cabeçalho está preenchido com você como autor, estado Rascunho e data 2026-11-22.

Escrevi só o que você me contou. Na Proposta entram o serviço entre o ingestor e o Kafka, a chave idempotente no Redis por 24h e o descarte dos repetidos. Em Motivação ficaram os 4% de duplicatas e as duas reclamações do financeiro. Em Métricas de sucesso ficou a meta de menos de 0,1%.

**Desvio do template:** ele não tem lugar para as alternativas que vocês descartaram nem para o trade-off aceito (+5 ms no caminho crítico). Criei duas subseções dentro de Proposta, "Alternativas consideradas" e "Trade-offs aceitos", e disse isso no próprio texto. Se a arquitetura não aceitar seções extras, é só mover o conteúdo ou removê-las.

**Seções que aguardam você:** Riscos e Plano de rollout estão com uma linha dizendo que esperam resposta. Não inventei riscos nem fases. Revisores e o número sequencial do DD também estão em aberto.

**Perguntas abertas, também no fim do doc:**
1. Qual é o número sequencial do DD-2026-`<seq>`, e quem são os revisores, com a área de cada um?
2. Quais riscos você vê e como cada um será mitigado? Por exemplo, o que acontece com o fluxo se o Redis ficar fora do ar?
3. Como o serviço entra em produção? Em fases ou de uma vez, com qual critério de avanço e qual plano de rollback?
4. Como vocês vão medir a taxa de duplicatas e os +5 ms em produção, e quem acompanha?
5. Por que não fazer nada não é aceitável, além do impacto no faturamento? A alternativa "não fazer nada" ficou pendente por isso.

Não incluí diagrama, porque o template pede um só junto com texto explicativo e eu teria que inventar detalhes de tecnologia e protocolo. Se quiser um, me passe esses detalhes. Também não rodei o `unslop`, porque ele não está disponível aqui.
