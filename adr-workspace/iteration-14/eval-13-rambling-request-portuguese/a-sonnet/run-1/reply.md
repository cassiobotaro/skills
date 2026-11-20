Escrevi a decisão como ADR. Como não havia log de decisões no repositório, criei também o ADR inicial, como o `adr init` faz:

- `doc/adr/0001-registrar-decisoes-de-arquitetura.md` (ADR inicial padrão, "Registrar decisões de arquitetura")
- `doc/adr/0002-gerar-pdf-de-fatura-em-segundo-plano.md` (a sua decisão, status Accepted porque a sync já fechou)

O ADR 0002 usa só o que você contou: os três incidentes de outubro, o cliente com cerca de 4 mil itens de linha, o limite de 30s, os 41 tickets, o timeout de 120s e a API de terceiros descartados (com os motivos), Sidekiq, bucket de documentos, e-mail com link. Nas Consequences ficaram os dois custos que você citou: o fim do download imediato, mesmo para fatura pequena, e a fila compartilhada do Sidekiq com o time de e-mail. Não citei nomes de pessoas. Mantive em inglês só o que o adr-tools e o importador `!adrs` do Structurizr leem (`Date:`, `## Status`, `## Context`, `## Decision`, `## Consequences`, `Accepted`). O texto está em português. No nome do arquivo tirei os acentos.

Deixei de fora a ideia de renomear o módulo de billing. Não é uma decisão tomada, e um ADR só registra decisões já tomadas. Se isso virar decisão, vale um ADR próprio.

Perguntas, se quiser refinar (não bloqueiam nada):
1. Existe algum prazo esperado ou meta para a geração em segundo plano? Não incluí nenhum número, porque você não mencionou.
2. O time de e-mail já foi avisado formalmente? Se houver algum combinado, como fila separada ou prioridade, me diga e eu registro. Por enquanto, ficou só o risco que vocês já aceitaram.
