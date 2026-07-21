Pronto. O log já existente está em inglês, então mantive o novo ADR em inglês também (um log em duas línguas fica pior que qualquer uma das duas); a estrutura do adr-tools continua em inglês de qualquer forma.

Arquivos:

- `doc/adr/0004-use-stateless-jwt-sessions.md` (novo) — status `Accepted` + `Supersedes [2. Store sessions in Redis](0002-store-sessions-in-redis.md)`. O Context registra o cluster Redis como ponto único de falha nos deploys multi-região e o custo de replicá-lo; a Decision fixa JWT stateless com expiração de 15 minutos; as Consequences incluem o trade-off aceito: não dá mais para revogar sessão imediatamente, a janela fica limitada pelos 15 minutos e a renovação de token passa a ser mais frequente.
- `doc/adr/0002-store-sessions-in-redis.md` (editado) — só a seção Status mudou: a palavra `Accepted` saiu e no lugar entrou `Superseded by [4. Use stateless JWT sessions](0004-use-stateless-jwt-sessions.md)`. O corpo do ADR 2 continua intacto, porque ele ainda documenta o que valia antes.
