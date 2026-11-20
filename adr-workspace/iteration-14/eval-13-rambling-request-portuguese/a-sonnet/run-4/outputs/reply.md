Pronto, escrevi o ADR. Como não havia log de decisões no repositório, criei `doc/adr/` com o ADR 0001 padrão ("Registrar decisões de arquitetura", o equivalente ao `adr init`) e a sua decisão virou o 0002.

Arquivos:
- `doc/adr/0001-registrar-decisoes-de-arquitetura.md`
- `doc/adr/0002-gerar-pdfs-de-fatura-em-background-com-sidekiq.md` (status Accepted, data 2026-11-20)

O texto está em português. O `Date:`, os títulos `## Status/Context/Decision/Consequences` e o status ficam em inglês de propósito, porque o adr-tools e o importador `!adrs` do Structurizr leem esses termos exatos.

Usei só o que você contou: os incidentes de outubro (30s do load balancer, ~4 mil itens, 41 tickets), as duas alternativas descartadas (timeout de 120s e API de terceiros, com os motivos), a decisão (Sidekiq, bucket de documentos, e-mail com link) e os trade-offs que o time aceitou (sem download imediato nem para fatura pequena, fila compartilhada com o time de e-mail). Não acrescentei métricas nem motivos que você não deu.

Duas observações:
- A ideia de renomear o módulo de billing ficou de fora, porque é outra decisão e ainda não foi tomada. Se vocês decidirem, vira um ADR separado.
- Se o rafael ou alguém ainda não concordou com a decisão, me diga e eu troco o status para Proposed.
