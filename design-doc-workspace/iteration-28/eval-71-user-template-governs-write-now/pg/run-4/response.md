O doc está em `docs/design/DD-2026-001-deduplicacao-de-eventos.md`. Usei `DD-2026-001` porque não havia outros docs na pasta.

Segui as seções do template na ordem: Motivação, Proposta, Riscos, Plano de rollout, Métricas de sucesso e Perguntas abertas.

**Desvio do template, para você aceitar ou não:** ele não tem lugar para alternativas nem para o trade-off aceito. Coloquei os dois como subseções dentro de Proposta, com os três itens que você discutiu (deduplicar no consumidor, idempotência nativa do Kafka e não fazer nada). O time de arquitetura pode não aceitar isso. Se não aceitar, é só mover o conteúdo para Motivação ou Riscos.

**O que ficou incompleto:**
- **Plano de rollout:** só diz que ainda não está definido, porque você não falou nada sobre fases ou rollback.
- **Riscos:** só tem a latência de +5ms. Os outros riscos viraram perguntas, por exemplo o que acontece se o Redis cair.
- **Métricas de sucesso:** tem a meta de menos de 0,1% de duplicatas. A latência aparece como estimativa de +5ms, sem limite máximo.
- **Perguntas abertas:** são 15, agrupadas por seção. Algumas delas:
  - a origem da chave idempotente;
  - a atomicidade da checagem no Redis;
  - o motivo das 24h;
  - fail-open ou fail-closed;
  - a capacidade esperada;
  - os critérios de rollout;
  - quem revisa o doc.

O campo Revisores está vazio e o Estado é Rascunho. Datas são de hoje, 2026-11-23.
