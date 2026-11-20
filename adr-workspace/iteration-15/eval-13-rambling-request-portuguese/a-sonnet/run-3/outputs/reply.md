Escrevi o ADR como decisão já tomada (status Accepted), em português, em `doc/adr/0002-gerar-pdfs-de-fatura-em-background-com-sidekiq.md`.

Como não havia log de decisões no repositório, criei também o `0001-registrar-decis-es-de-arquitetura.md` (o ADR inicial padrão do `adr init`, traduzido). Seu ADR ficou como 0002. Os rótulos em inglês (`Date:`, `## Status`, `## Context`, etc.) ficam assim de propósito, porque o adr-tools e o importador do Structurizr leem esses termos.

O que registrei vem só do que você contou: os três incidentes de outubro, o limite de 30s, os 41 tickets, o timeout de 120s e a API de terceiros descartados, e as desvantagens aceitas (fim do download imediato e fila compartilhada com o time de e-mail). Não acrescentei métricas, prazos nem alternativas.

Deixei de fora a ideia de renomear o módulo de billing, porque é outro assunto e não é uma decisão tomada. Se virar decisão, vale um ADR próprio.

Perguntas, se quiser refinar:
1. Algum detalhe da implementação já foi decidido (nome da fila, prazo de validade do link, retenção dos arquivos no bucket)? Não registrei nada disso por não ter sido dito.
2. Quem decidiu na sync de quinta? Posso citar as pessoas ou o time, se for útil para o histórico.
