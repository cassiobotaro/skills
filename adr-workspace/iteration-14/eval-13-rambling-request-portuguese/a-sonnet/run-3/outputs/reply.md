Escrevi como ADR, já com a decisão da sync de plataforma. Não existia log de decisões no repositório, então criei `doc/adr/` com o ADR 0001 de praxe ("Registrar a arquitetura com ADRs", traduzido) e a sua decisão virou o 0002.

Arquivos:
- `doc/adr/0001-registrar-a-arquitetura-com-adrs.md`
- `doc/adr/0002-gerar-pdfs-de-fatura-em-background-com-sidekiq.md` (status Accepted)

O 0002 registra o contexto (os 3 incidentes de outubro, o limite de 30s, os 41 tickets, o cliente com ~4 mil itens), as alternativas descartadas (timeout de 120s e API de PDF de terceiros, vetada pelo jurídico), a decisão (Sidekiq, bucket de documentos, e-mail com link) e as consequências que vocês aceitaram: fim do download imediato, mesmo para fatura pequena, e o risco para o time de e-mail por causa da fila compartilhada. Os rótulos em inglês (`Date:`, `## Status` etc.) ficam assim de propósito, porque o adr-tools e o importador `!adrs` do Structurizr leem esses literais. O texto está em português.

Deixei de fora a ideia de renomear o módulo de billing. Foi um comentário solto, não uma decisão. Se virar decisão, vale um ADR próprio.

Perguntas, caso queira completar o registro:
1. A decisão está fechada mesmo (Accepted), ou ainda aguarda alguém? Se aguarda, troco para Proposed.
2. Alguém objetou ou ficou de fora da sync (o time de e-mail, por exemplo)? Não registrei isso porque você não disse.
