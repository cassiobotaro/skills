Escrevi o ADR 4 e marquei o ADR 2 como substituído.

- **Criado:** `doc/adr/0004-use-stateless-jwt-sessions.md`, com status `Accepted` e a linha `Supersedes [2. Store sessions in Redis](0002-store-sessions-in-redis.md)`.
- **Editado:** `doc/adr/0002-store-sessions-in-redis.md`. Só mudei a seção Status, que agora diz `Superseded by [4. Use stateless JWT sessions](0004-use-stateless-jwt-sessions.md)`. O resto do arquivo ficou como estava.

O conteúdo do ADR 4 vem só do que você me disse:
- **Contexto:** o Redis virou ponto único de falha nos deploys multi-região, e o custo de mantê-lo replicado não compensa.
- **Decisão:** passar a usar tokens JWT stateless com expiração de 15 minutos.
- **Consequências:** o login deixa de depender do Redis. Em troca, não dá para revogar sessão imediatamente, e o limite é a expiração de 15 minutos. O logout global também deixa de ser um único DELETE, como era no ADR 2.

Escrevi o ADR em inglês, porque os ADRs 1 a 3 estão em inglês e o log fica mais consistente assim. Os títulos das seções e o rótulo `Date:` também ficam em inglês, que é o que o adr-tools espera. A data é 2026-11-22.

Não incluí nada que você não tenha dito, como algoritmo de assinatura, refresh token ou alternativas avaliadas. Se a equipe decidiu algo sobre isso, como mitigação para revogação ou um mecanismo de renovação, me passe que eu acrescento ao ADR 4. Como ele é novo e ainda não foi commitado, dá para ajustar o texto sem criar outro ADR.

Não fiz commit.
