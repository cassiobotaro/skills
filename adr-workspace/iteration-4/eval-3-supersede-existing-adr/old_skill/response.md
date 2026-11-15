Pronto. Registrei a decisão e marquei o ADR antigo como substituído.

**Arquivos:**

- **Criado:** `doc/adr/0004-use-stateless-jwt-sessions.md` — o novo ADR (número 4, próximo na sequência). Status `Accepted`, com a linha `Supersedes [2. Store sessions in Redis](0002-store-sessions-in-redis.md)`. O Context descreve o Redis como ponto único de falha nos deploys multi-região e o custo de mantê-lo replicado; a Decision registra a troca para tokens JWT stateless com expiração de 15 minutos; as Consequences incluem o trade-off aceito — não dá mais para revogar uma sessão imediatamente, mitigado pela expiração curta.
- **Editado:** `doc/adr/0002-store-sessions-in-redis.md` — apenas a seção Status: a palavra `Accepted` foi removida e substituída por `Superseded by [4. Use stateless JWT sessions](0004-use-stateless-jwt-sessions.md)`. O corpo do ADR 2 permanece intacto (um ADR é imutável fora da seção Status — continua valioso saber qual ERA a decisão).

**Uma observação sobre idioma:** o log existente (`doc/adr/`) está em inglês. Para manter o log consistente de ponta a ponta, escrevi o ADR 4 também em inglês e usei os verbos `Supersedes` / `Superseded by` em inglês — um log misturando dois idiomas fica pior do que qualquer um dos dois. Se você preferir, posso reescrever todo o log em português; mas aí o ideal é converter todos os ADRs de uma vez.

Os arquivos seguem o formato adr-tools, então suas ferramentas existentes funcionam sem mudança: `adr list`, `adr generate toc`, `adr generate graph` e o importador `!adrs doc/adr` do Structurizr.
