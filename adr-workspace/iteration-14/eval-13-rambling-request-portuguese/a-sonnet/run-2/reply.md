Oi! Escrevi o ADR da geração de PDF em background. Como não havia log de decisões no repositório, criei também o seed padrão do `adr init` (traduzido para português):

- `doc/adr/0001-registrar-decisoes-de-arquitetura.md`
- `doc/adr/0002-gerar-pdfs-de-fatura-em-background.md` (Status: Accepted, já que a decisão foi tomada na sync)

Usei só o que você contou: os incidentes de outubro, os 41 tickets, o limite de 30s, as duas alternativas descartadas (timeout de 120s e API de terceiros) e as consequências aceitas (fim do download imediato e fila compartilhada do Sidekiq). Os títulos e textos estão em português, mas `Date:`, os cabeçalhos (`## Status`, `## Context`...) e o status ficam em inglês, porque o adr-tools e o importador `!adrs` do Structurizr leem esses termos exatos.

Deixei de fora a ideia de renomear o módulo de billing: é outro assunto e não foi uma decisão tomada. Se virar decisão, vira um ADR próprio.

Perguntas, se quiser refinar:
1. Quem aprovou na sync (o Rafael e o time de plataforma)? Posso citar, se fizer sentido.
2. Existe algum prazo ou formato de aviso combinado com o time de e-mail sobre a fila compartilhada (ex.: fila separada depois)? Não registrei nada disso porque não foi dito.
