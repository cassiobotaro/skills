Pronto. Registrei a nova decisão e marquei a antiga como substituída.

**Arquivo criado:**

- `doc/adr/0004-use-stateless-jwt-sessions.md` — ADR 4 "Use stateless JWT sessions", status `Accepted`, com a linha `Supersedes [2. Store sessions in Redis]`. O Context explica que o cluster Redis virou ponto único de falha nos deploys multi-região e que replicá-lo não compensava; o Decision descreve o JWT stateless com expiração de 15 minutos; e o Consequences registra o trade-off aceito de não conseguir revogar sessão imediatamente, mitigado pela expiração curta.

**Arquivo editado:**

- `doc/adr/0002-store-sessions-in-redis.md` — só a seção Status mudou: o `Accepted` foi removido e substituído por `Superseded by [4. Use stateless JWT sessions](0004-use-stateless-jwt-sessions.md)`. O corpo do ADR antigo permanece intacto, porque continua valendo saber qual ERA a decisão.

Segui as convenções do adr-tools (numeração sequencial, nome `NNNN-slug.md`, par supersede/superseded), então suas ferramentas existentes funcionam sem alteração: `adr list`, `adr generate toc`, `adr generate graph` e o importador `!adrs doc/adr` do Structurizr.

Uma observação: os ADRs são escritos em inglês de propósito (cabeçalhos e corpo), para o log ficar consistente de ponta a ponta e compatível com a tooling que espera os nomes de seção em inglês — a conversa segue em português normalmente.
