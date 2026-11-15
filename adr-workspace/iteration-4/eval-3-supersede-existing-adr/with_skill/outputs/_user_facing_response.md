Pronto. Criei o novo ADR e marquei o antigo como substituído.

Os ADRs já existentes em `doc/adr` estão escritos em inglês, então mantive o novo registro em inglês também — um log de decisões em dois idiomas fica pior do que em qualquer um dos dois, então a consistência com o que já existe vale mais do que o idioma da conversa.

Arquivos:

- **Criado** `doc/adr/0004-use-stateless-jwt-sessions.md` — o novo ADR (número 4, o próximo na sequência). Status `Accepted` com `Supersedes [2. Store sessions in Redis]`. O Context registra que o cluster Redis virou ponto único de falha nos deploys multi-região e que o custo de replicá-lo não compensa; a Decision adota tokens JWT stateless; e as Consequences listam tanto o ganho (sumiu o ponto único de falha e o custo de replicação) quanto o trade-off aceito: não dá mais para revogar sessão na hora, mitigado com expiração curta de 15 minutos.

- **Editado** `doc/adr/0002-store-sessions-in-redis.md` — apenas a seção Status: troquei `Accepted` por `Superseded by [4. Use stateless JWT sessions](0004-use-stateless-jwt-sessions.md)`. O corpo do ADR 2 não foi alterado (ADRs são imutáveis a não ser pelo Status), justamente para preservar o registro de qual era a decisão antiga.

Os arquivos seguem o formato adr-tools, então `adr list` e `adr generate graph` reconhecem o vínculo de supersessão normalmente.
