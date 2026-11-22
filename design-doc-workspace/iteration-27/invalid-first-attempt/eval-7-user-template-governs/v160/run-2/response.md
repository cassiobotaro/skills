Salvei o doc em `docs/design/DD-2026-001-deduplicacao-de-eventos.md`. Ele usa as seis seções do template, na mesma ordem e com os mesmos títulos.

- **Numeração:** só existia o `TEMPLATE.md` na pasta, então usei DD-2026-001 e a data de hoje (2026-11-22). Se o time tem outra sequência, é só ajustar.
- **Alternativas:** o template não tem seção de alternativas. Para não criar seção nova, coloquei as duas descartadas como subseção `### Alternativas descartadas` dentro de **Proposta**.
- **Trade-off dos +5ms:** está em **Riscos**, marcado como estimativa ainda não medida.
- **Revisores:** deixei em branco, porque você não informou quem são.
- **Plano de rollout:** não inventei nada, porque você não me deu fases nem critérios. A seção diz "a definir" e aponta para as Perguntas abertas.
- **Perguntas abertas:** acrescentei quatro que você não mencionou:
  - o que acontece se o Redis cair (deixar passar ou bloquear);
  - quem gera a chave idempotente;
  - como medir a latência real;
  - quais são as fases do rollout.
- **Janela de 24h:** incluí em Riscos que duplicata reenviada depois das 24h não é detectada. Isso decorre do TTL de 24h, mas confirme se vale para o caso de vocês.

Antes de enviar ao time de arquitetura, vale preencher o rollout e responder pelo menos a pergunta do Redis. O comportamento com Redis fora do ar muda o risco da proposta.
