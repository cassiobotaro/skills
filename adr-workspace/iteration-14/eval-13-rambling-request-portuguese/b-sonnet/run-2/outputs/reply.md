Escrevi o ADR como aceito (vocês disseram que ficou decidido na sync de quinta). Como não havia log de decisões no repositório, criei `doc/adr/` com o ADR 0001 padrão ("Registrar decisões de arquitetura") e a sua decisão ficou como 0002.

Arquivos:
- doc/adr/0001-registrar-decisoes-de-arquitetura.md
- doc/adr/0002-gerar-pdfs-de-fatura-em-background-com-sidekiq.md

Notas:
- O texto está em português. Date:, os títulos de seção (Status, Context, Decision, Consequences) e o status Accepted ficam em inglês de propósito, porque o adr-tools e o importador !adrs do Structurizr leem esses termos.
- Usei só o que você contou: os incidentes de outubro, os 41 tickets, o descarte do timeout de 120s e da API de terceiros, e as consequências aceitas (fim do download imediato e fila compartilhada com e-mail). Não inventei prazos, métricas nem detalhes de implementação.
- A ideia de renomear o módulo de billing ficou de fora. É outra decisão e ainda não foi tomada, então não há o que registrar. Se vocês decidirem, vale um ADR próprio.

Perguntas, se quiser refinar:
1. O status deve ser Accepted mesmo, ou alguém ainda precisa concordar (então seria Proposed)?
2. Querem registrar algum detalhe que não mencionou, como o que acontece se a geração falhar, ou mudar o nome do bucket? Deixei de fora por não ter sido dito.
