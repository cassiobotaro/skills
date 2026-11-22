Escrevi o ADR 4, que substitui o ADR 2, e marquei o ADR 2 como substituído.

- **Criado:** `doc/adr/0004-use-stateless-jwt-sessions.md`. O status é `Accepted`, com a linha `Supersedes [2. Store sessions in Redis](0002-store-sessions-in-redis.md)`.
- **Editado:** `doc/adr/0002-store-sessions-in-redis.md`. Só a seção Status mudou: o `Accepted` virou `Superseded by [4. Use stateless JWT sessions](0004-use-stateless-jwt-sessions.md)`. O restante do arquivo ficou intacto, como o `git diff` confirma.

O texto do ADR 4 está em inglês, não em português. Os ADRs existentes estão em inglês, e manter o log num idioma só é a regra. Os rótulos (`Date:`, `## Status` e os demais) ficam em inglês de qualquer jeito, por causa do adr-tools.

Usei só o que você me deu:
- **Contexto:** o Redis virou ponto único de falha nos deploys multi-região, e o custo de mantê-lo replicado não compensa.
- **Decisão:** JWT stateless com expiração de 15 minutos.
- **Consequências:**
  - O Redis deixa de ser dependência do caminho de login.
  - Não dá mais para revogar uma sessão na hora. Um token revogado ou comprometido pode continuar válido por até 15 minutos, e a expiração curta é o que limita isso.
  - O "logout em todos os lugares" deixa de ser um único DELETE.

Não registrei alternativas que vocês tenham avaliado, refresh tokens nem o que acontece com o Redis depois da migração, porque você não falou disso. Se quiserem que isso fique no registro, me diga e eu incluo.
