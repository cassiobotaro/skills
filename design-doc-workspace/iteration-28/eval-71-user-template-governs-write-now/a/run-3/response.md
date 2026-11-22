Rafael, o doc está em `docs/design/servico-de-deduplicacao-de-eventos.md`. Segui o `TEMPLATE.md` na ordem original: Motivação, Proposta, Riscos, Plano de rollout, Métricas de sucesso e Perguntas abertas.

**Fora do template:** ele não tem lugar para as alternativas que você descreveu, então criei uma seção "Alternativas consideradas" logo depois de Proposta. Ela traz as duas que vocês descartaram e "não fazer nada". Pus os trade-offs como subseção de Proposta. O resto do esqueleto ficou intacto, mas confirme se o time de arquitetura aceita essa seção extra. Se não aceitar, ela volta para dentro de Proposta.

**O que você já tinha dito:**
- A Motivação traz os 4% de duplicatas e as duas reclamações do financeiro.
- A Proposta descreve o serviço entre o ingestor e o Kafka, com a chave no Redis por 24h.
- O custo aceito é +5 ms de latência.
- A meta de duplicatas abaixo de 0,1% está em Métricas de sucesso.

**O que ficou em aberto:** não preenchi nada que você não disse.
- **Riscos e Plano de rollout:** só mencionam a latência e apontam para as perguntas.
- **Cabeçalho:** o ID `DD-2026-<seq>` e os revisores estão em branco.
- **Perguntas abertas (9):**
  - número do documento e revisores;
  - origem da chave idempotente;
  - o que acontece se o Redis cair;
  - duplicatas que chegam depois de 24h;
  - outros riscos e mitigações;
  - fases do rollout e rollback;
  - como medir a taxa de duplicatas e a latência;
  - o que fica fora de escopo;
  - quem mais é impactado.

Não incluí diagrama, porque os componentes e protocolos que ele exigiria não foram definidos. O estado do documento é Rascunho, com data de 2026-11-22. Não rodei a skill `unslop` nem outra validação.
