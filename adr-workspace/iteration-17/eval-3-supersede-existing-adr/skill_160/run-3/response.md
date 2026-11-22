Escrevi o ADR 4, que substitui o ADR 2, e atualizei o status do ADR 2.

- **Criado:** `doc/adr/0004-use-stateless-jwt-sessions.md`. O status é `Accepted` e ele tem a linha `Supersedes [2. Store sessions in Redis](0002-store-sessions-in-redis.md)`.
- **Editado:** `doc/adr/0002-store-sessions-in-redis.md`. Só a seção Status mudou: `Accepted` virou `Superseded by [4. Use stateless JWT sessions](0004-use-stateless-jwt-sessions.md)`. O `git diff` mostra só essa linha alterada.

- **Idioma:** o log existente está em inglês, então o título e o texto do ADR 4 também estão em inglês, para manter o log num idioma só. Os rótulos e cabeçalhos (`Date:`, `## Status` etc.) seguem o padrão do adr-tools de qualquer forma.
- **Conteúdo:** usei só o que você disse.
  - **Contexto:** o Redis virou ponto único de falha nos deploys multi-região, e o custo de manter o cluster replicado não compensa.
  - **Decisão:** usar tokens JWT stateless com expiração de 15 minutos.
  - **Consequências:** o Redis deixa de ser dependência das sessões, e perdemos a revogação imediata, com a expiração curta limitando o impacto.
- **Fora do ADR:** não citei alternativas que vocês avaliaram nem outras consequências, porque você não mencionou nenhuma. Se houver algo assim, como o fluxo de logout ou o uso de refresh token, me conta e eu incluo no ADR 4.

Não rodei nenhum commit.
