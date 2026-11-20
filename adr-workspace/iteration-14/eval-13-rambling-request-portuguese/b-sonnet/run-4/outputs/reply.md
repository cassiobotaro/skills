Pronto, escrevi como ADR. Como não havia log de decisões no repositório, criei também o ADR de semente, como o `adr init` faz:

- `doc/adr/0001-registrar-decisoes-de-arquitetura.md` (semente, traduzida para português)
- `doc/adr/0002-gerar-pdfs-de-fatura-em-background-com-sidekiq.md` (a decisão, status Accepted)

O texto está em português. Os rótulos que o adr-tools e o importador `!adrs` do Structurizr leem ficaram em inglês (`Date:`, `## Status`, `## Context`, `## Decision`, `## Consequences`, `Accepted`).

Usei só o que você contou: os 3 incidentes de outubro, o timeout de 30s e os 41 tickets. Registrei também as alternativas descartadas (timeout de 120s e API de terceiros, por causa do jurídico) e as consequências aceitas (fim do download imediato, fila compartilhada com o time de e-mail). Não acrescentei nenhum motivo seu.

A observação sobre renomear o módulo de billing ficou de fora, porque é outro assunto e não foi decidida. Se virar decisão, vira um ADR separado.

Perguntas, se quiser ajustar:
1. A decisão já está fechada (Accepted) ou ainda aguarda a aprovação de alguém (Proposed)? Assumi Accepted pela sua descrição.
2. Se quiser, posso acrescentar algum detalhe que não mencionou, como o prazo esperado para o e-mail chegar ou o tempo de retenção dos arquivos no bucket. Não incluí porque não foram ditos.
