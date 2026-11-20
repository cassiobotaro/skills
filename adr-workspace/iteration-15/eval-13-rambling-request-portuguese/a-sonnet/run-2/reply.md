Escrevi o ADR como registro de uma decisão já tomada, com status Accepted. Como o repositório não tinha log de decisões, criei `doc/adr/` com o ADR 0001 (o de praxe, "Registrar decisões de arquitetura") e a sua decisão virou o 0002:

- `doc/adr/0001-registrar-decis-es-de-arquitetura.md`
- `doc/adr/0002-gerar-pdfs-de-fatura-em-background-via-sidekiq.md`

O nome do arquivo perde os acentos (`decis-es`) por causa da regra de slug do adr-tools. O título dentro do arquivo mantém. Os rótulos que o adr-tools e o importador `!adrs` do Structurizr leem (`Date:`, `## Status`, `## Context`, `## Decision`, `## Consequences`, `Accepted`) ficam em inglês. O texto está em português.

Usei só o que você contou: os incidentes de outubro, os 41 tickets da Marta, as alternativas descartadas (timeout de 120s e API de terceiros, com os motivos), a decisão e os dois custos aceitos (fim do download imediato e fila compartilhada com o time de e-mail). Não acrescentei métricas nem motivos.

Duas observações:
1. A renomeação do módulo de billing ficou fora. Não é uma decisão tomada, e um ADR sobre ela teria que inventar o que foi decidido. Quando decidirem, peça que eu escrevo.
2. Se quiserem marcar o ADR como Proposed porque o pessoal ainda não fechou formalmente, é só avisar. Entendi que "ficou decidido" significa Accepted.
