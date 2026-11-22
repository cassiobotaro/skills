Criei o novo ADR e marquei o ADR 2 como substituído. Não fiz commit.

- **`doc/adr/0004-use-stateless-jwt-for-sessions.md`** (novo): status "Accepted", com a linha "Supersedes" apontando para o ADR 2, no mesmo formato dos outros ADRs.
  - **Contexto:** o Redis virou ponto único de falha nos deploys multi-região, e o custo de mantê-lo replicado não compensa.
  - **Decisão:** JWT stateless, validado localmente por cada instância da API, com expiração de 15 minutos.
  - **Consequências:** o login deixa de depender do Redis. Não dá para revogar sessão na hora, então um token comprometido vale por até 15 minutos, e o texto diz que a gente aceita isso.
- **`doc/adr/0002-store-sessions-in-redis.md`**: o status mudou de "Accepted" para "Superseded by [4. Use stateless JWT for sessions]", com link. O resto do texto ficou como estava.

Acrescentei duas consequências que você não mencionou, mas que decorrem da decisão. Com expiração de 15 minutos, é preciso definir um mecanismo de renovação de token. As chaves de assinatura também precisam ser distribuídas e rotacionadas com segurança entre as instâncias. Se vocês já decidiram algo sobre isso, vale ajustar o texto.

Usei a data de hoje, 2026-11-22.
