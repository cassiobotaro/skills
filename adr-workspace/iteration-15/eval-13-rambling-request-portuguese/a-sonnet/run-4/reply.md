Oi! Escrevi a decisão como ADR. Como não havia log de decisões no repositório, criei `doc/adr/` com o ADR 0001 (o de praxe, "Registrar decisões de arquitetura") e a sua decisão virou o 0002.

Arquivos:
- doc/adr/0001-registrar-decis-es-de-arquitetura.md
- doc/adr/0002-gerar-pdfs-de-fatura-em-background-com-sidekiq.md

O que ficou registrado: o problema (PDF gerado na request, três incidentes em outubro, limite de 30s, 41 tickets), as duas alternativas descartadas (timeout de 120s e API de terceiros, com os motivos), a decisão (Sidekiq, bucket de documentos, e-mail com link) e as consequências (fim do download imediato, caminho de código único, fila compartilhada com o time de e-mail). Só usei o que você contou, sem acrescentar motivos nem números.

Marquei o status como Accepted, porque você disse que ficou decidido na sync. Se ainda falta alguém concordar, troco para Proposed.

Deixei de fora a ideia de renomear o módulo de billing: não é uma decisão tomada. Se virar uma, vira um ADR separado.

Perguntas, se quiser enriquecer o registro (nada disso foi inventado):
1. Qual a data da sync de quinta? Não coloquei nenhuma data de reunião no texto.
2. Há prazo de validade do link do e-mail ou algum controle de acesso ao arquivo no bucket? Não registrei nada disso por não ter sido dito.
