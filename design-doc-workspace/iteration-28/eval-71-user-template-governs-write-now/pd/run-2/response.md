Salvei o doc em `docs/design/dd-2026-001-servico-de-deduplicacao-de-eventos.md`. Não rodei nenhuma checagem do arquivo além da própria escrita.

- **Template:** segui as seções na ordem original. Como `docs/design/` só tinha o template, numerei como DD-2026-001. O estado ficou em Rascunho e a data é 2026-11-23. Deixei o campo Revisores vazio.
- **Seção extra:** o template não tem lugar para as alternativas que você descartou. Coloquei uma subseção "Alternativas consideradas" dentro de Proposta, com o aviso de que ela não é do template. Se o time de arquitetura não aceitar subseções, é só remover o título e deixar o texto.
- **Seções sem substância sua:** Riscos registra só o trade-off de +5ms que você aceitou. Rollout diz que ainda não foi definido. Em ambos, não escrevi riscos nem fases por conta própria. Os dois apontam para as perguntas.
- **Perguntas abertas:** são 11, agrupadas por seção. As mais importantes:
  - como se forma a chave idempotente;
  - o que o serviço faz se o Redis cair;
  - o que acontece com reenvios depois das 24h;
  - o comportamento com requisições concorrentes do mesmo evento;
  - o plano de rollout e os critérios de rollback;
  - como a taxa de duplicatas será medida depois do rollout.

Não incluí diagrama, porque o doc não define tecnologias nem protocolos para colocar nele.
