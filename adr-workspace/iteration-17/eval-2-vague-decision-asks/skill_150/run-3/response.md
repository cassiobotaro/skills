Antes de escrever o ADR, preciso de algumas informações. O repositório não tem log de decisões nem qualquer menção ao Redis, então não consigo deduzir nada daqui, e não quero inventar o motivo.

1. **Vão trocar pelo quê?** Por exemplo Memcached, Valkey, Postgres ou um cache em memória. E para qual uso: cache, sessões, filas, outro?
2. **Por que trocar, e por que agora?** Pode ser custo, operação, licença, desempenho ou outro motivo. Quero registrar as razões reais do time.
3. **Que alternativas foram consideradas** e descartadas?
4. **Qual downside vocês aceitaram?** Pode ser trabalho de migração, perda de algum recurso do Redis ou risco durante a transição.
5. **A decisão já está fechada?** Se estiver, o ADR fica como `Accepted`. Se ainda aguarda aprovação de alguém, fica como `Proposed`.

Com essas respostas eu escrevo o ADR em português. Como não existe log ainda, também crio `doc/adr/` com o ADR 0001 padrão de "registrar decisões de arquitetura". O ADR do Redis fica como 0002.

Se já existir um ADR antigo que adotou o Redis em outro lugar, me diga onde. Aí eu marco esse ADR como substituído e ligo os dois.
