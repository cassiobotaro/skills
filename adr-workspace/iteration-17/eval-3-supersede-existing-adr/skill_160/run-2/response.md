Criei o ADR 4, que substitui o ADR 2, e marquei o ADR 2 como superado.

- **`doc/adr/0004-use-stateless-jwt-sessions.md`** (novo): status `Accepted`, com a linha `Supersedes [2. Store sessions in Redis](0002-store-sessions-in-redis.md)`. A data é 2026-11-22.
- **`doc/adr/0002-store-sessions-in-redis.md`** (editado): só a seção Status mudou. `Accepted` virou `Superseded by [4. Use stateless JWT sessions](0004-use-stateless-jwt-sessions.md)`, e o diff confirma que o resto do arquivo está intacto.

O texto do ADR 4 está em inglês, porque os ADRs 1 a 3 estão. Os títulos e as seções (`Date:`, `## Status`, `## Context` e os outros) seguem o formato do adr-tools.

Usei só o que você disse:
- **Contexto:** o cluster Redis virou ponto único de falha nos deploys multi-região, e o custo de mantê-lo replicado não compensa.
- **Decisão:** passar a usar tokens JWT stateless, com expiração de 15 minutos.
- **Trade-off:** não dá para revogar uma sessão na hora. Um token emitido vale até expirar, então 15 minutos é o tempo máximo que uma sessão revogada continua funcionando.

Não escrevi nada sobre alternativas que vocês tenham considerado, nem sobre a mudança de logout global (que no ADR 2 era um único DELETE), porque você não falou disso. Se quiser registrar alguma delas, me diga e eu acrescento.

Não fiz commit.
