Escrevi a ADR em `doc/adr/`. Como o repositório ainda não tinha log de decisões, criei também a seed `0001-registrar-decisões-de-arquitetura.md` (o equivalente ao `adr init`, traduzida para português; os cabeçalhos `Date:`, `## Status`, `## Context`, `## Decision`, `## Consequences` e o status `Accepted` ficam em inglês para o adr-tools e o `!adrs` do Structurizr continuarem lendo os arquivos).

A decisão ficou como `0002-gerar-pdf-de-fatura-em-background.md`, com status `Accepted`: a geração sai da request web e passa para o Sidekiq, o arquivo vai para o bucket de documentos e o cliente recebe o link por e-mail. Registrei as alternativas descartadas (subir o timeout para 120s e a API de PDF de terceiros) no Context, e as consequências que o time aceitou, incluindo o fim do download imediato e o compartilhamento da fila com os e-mails.

Não criei ADR para a renomeação do módulo de billing: ainda não é uma decisão tomada, e um ADR só registra escolhas feitas.

Duas perguntas antes de considerar a ADR final:
1. O link enviado por e-mail tem controle de acesso ou expiração? Não registrei nada sobre isso porque não foi dito na conversa, mas se for uma decisão já tomada, vale constar nas consequências.
2. A geração de PDF vai usar a mesma fila de e-mails ou uma fila separada no Sidekiq? A conversa diz que a fila é compartilhada, mas se o time pretende separar, isso muda a seção de consequências.
