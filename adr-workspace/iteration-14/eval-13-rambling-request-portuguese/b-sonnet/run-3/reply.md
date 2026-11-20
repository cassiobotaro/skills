Escrevi como ADR, com o log começando do zero:

- `doc/adr/0001-registrar-decisoes-de-arquitetura.md` — o ADR inicial padrão ("registrar decisões de arquitetura"), que o `adr init` criaria, traduzido para português. Não havia log no repositório.
- `doc/adr/0002-gerar-pdfs-de-fatura-em-background-via-sidekiq.md` — a sua decisão, com status `Accepted`.

O Context tem só o que você contou: os 3 incidentes de outubro, os 4 mil itens de linha, o limite de 30s, os 41 tickets e as duas alternativas descartadas (timeout de 120s e API de terceiros, com o motivo de cada uma). O Consequences registra o fim do download imediato, mesmo para fatura pequena, e o risco da fila compartilhada para o time de e-mail. Os títulos e textos estão em português. `Date:`, os cabeçalhos `## Status/Context/Decision/Consequences` e `Accepted` ficam em inglês, porque o adr-tools e o `!adrs` do Structurizr leem esses literais.

Deixei de fora de propósito a ideia de renomear o módulo de billing. Não é parte desta decisão (um ADR por decisão). Se quiser registrá-la, me avise quando ela for decidida.

Perguntas, se quiser ajustar:
1. A decisão já está fechada (`Accepted`) ou ainda espera o aval de alguém (`Proposed`)? Presumi `Accepted`, pois você disse que ficou decidido.
2. Há mais algum ponto aceito ou algum risco que eu não registrei? Por exemplo, o que o cliente vê enquanto espera o e-mail, ou um limite de tamanho para a fila. Não incluí nada disso porque você não mencionou.
