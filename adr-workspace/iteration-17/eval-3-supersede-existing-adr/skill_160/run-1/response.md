Escrevi o ADR 4 e marquei o ADR 2 como substituído. Não rodei `adr list` nem nenhuma outra ferramenta.

- **Criado:** `doc/adr/0004-use-stateless-jwt-sessions.md`, com status `Accepted` e a linha `Supersedes [2. Store sessions in Redis](0002-store-sessions-in-redis.md)`.
- **Editado:** `doc/adr/0002-store-sessions-in-redis.md`. Só a seção Status mudou: `Accepted` virou `Superseded by [4. Use stateless JWT sessions](0004-use-stateless-jwt-sessions.md)`. O `git diff` confirma que é a única alteração e que o corpo do ADR 2 está intacto.

- **Idioma:** escrevi o ADR em inglês, porque os ADRs 1 a 3 estão em inglês e o log deve ficar em um idioma só. Os rótulos `Date:`, `## Status` e `## Context`, os demais títulos de seção e o `Supersedes` ficam em inglês de qualquer forma, porque o adr-tools e o `!adrs` do Structurizr leem esses termos exatos. Se preferir o log em português, traduzo o texto do ADR 4. Nesse caso os ADRs 1 a 3 continuariam em inglês.
- **Conteúdo:** usei só o que você disse. O contexto fala do Redis como ponto único de falha no multi-região e do custo da replicação. A decisão é usar JWT stateless com expiração de 15 minutos. O trade-off é perder a revogação imediata, limitada pelos 15 minutos.
- **Consequência que eu derivei:** o ADR 4 diz que o logout global deixa de ser um único `DELETE`, como era no ADR 2. Isso decorre do trade-off que você descreveu e do texto do ADR 2, mas não foi uma frase sua. Tire a linha se não quiser registrar isso.
- **Fora do ADR:** não mencionei refresh tokens nem o algoritmo de assinatura, porque você não falou deles. Se já decidiram algo sobre isso, vale um ADR separado.
- **Commit:** não fiz.
