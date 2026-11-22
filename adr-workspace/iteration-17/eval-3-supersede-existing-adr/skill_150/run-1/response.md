Escrevi o ADR 4, que substitui o ADR 2, e atualizei o status do ADR 2. Não rodei `adr list` nem o `!adrs` do Structurizr.

- **Criado:** `doc/adr/0004-use-stateless-jwt-sessions.md`, com status `Accepted` e a linha `Supersedes [2. Store sessions in Redis](0002-store-sessions-in-redis.md)`.
  - **Contexto:** o cluster Redis virou ponto único de falha nos deploys multi-região, e o custo de mantê-lo replicado não compensa.
  - **Decisão:** usar JWT stateless com expiração de 15 minutos.
  - **Consequências:** o login deixa de depender de consulta ao Redis. Em troca, não dá mais para revogar uma sessão na hora, e o "logout em todos os lugares" do ADR 2 (um único DELETE) deixa de existir.
- **Editado:** `doc/adr/0002-store-sessions-in-redis.md`. Só a seção Status mudou. A palavra `Accepted` saiu e entrou `Superseded by [4. Use stateless JWT sessions](0004-use-stateless-jwt-sessions.md)`. O corpo do ADR 2 ficou intacto.

**Idioma:** escrevi o ADR 4 em inglês, e não em português, porque os ADRs existentes estão em inglês e o skill manda manter o idioma do log. As seções (`Date:`, `## Status` etc.) seguem o padrão do adr-tools, em inglês.

**Fora do ADR:** o texto só traz o que você disse. Não citei alternativas que você não mencionou. Também não escrevi que o Redis sai da infraestrutura, porque você não disse isso. Se quiser registrar como será o refresh de token ou se o Redis continua para cache, é melhor outro ADR, ou me diga e eu acrescento.
