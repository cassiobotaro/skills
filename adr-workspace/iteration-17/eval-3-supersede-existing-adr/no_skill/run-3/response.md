Escrevi o ADR 4 e marquei o ADR 2 como substituído. Não commitei nada.

- **`doc/adr/0004-use-stateless-jwt-for-sessions.md` (novo):** status Accepted, com "Supersedes" apontando para o ADR 2, e data de hoje (2026-11-22).
  - **Contexto:** o cluster Redis virou ponto único de falha nos deploys multi-região, e o custo de replicá-lo não compensa.
  - **Decisão:** JWT stateless com expiração de 15 minutos.
  - **Consequências:** o login deixa de depender do Redis, mas a sessão não pode mais ser revogada na hora, só expira em até 15 minutos. O "logout em todos os lugares" deixa de ser um DELETE, e a sessão deslizante de 30 dias some.
- **`0002-store-sessions-in-redis.md`:** só o status mudou, de Accepted para "Superseded by 4", com link. O resto do texto ficou como estava.

Acrescentei por conta própria duas consequências que você não mencionou: é preciso definir um mecanismo de renovação do token, e as chaves de assinatura precisam ser distribuídas entre as regiões e rotacionadas com segurança. Deixei o mecanismo de renovação explicitamente como "não decidido aqui". Se vocês já decidiram algo sobre isso, vale incluir no ADR.

O ADR 3 (gRPC) não menciona sessões em Redis, então não mexi nele.
