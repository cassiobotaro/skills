Escrevi a decisão como ADR. Como não havia log de decisões no repositório, criei `doc/adr/` com o ADR 0001 padrão (registrar decisões de arquitetura, traduzido) e a sua decisão virou o 0002:

- `doc/adr/0001-registrar-decisoes-de-arquitetura.md`
- `doc/adr/0002-gerar-pdfs-de-fatura-em-background-via-sidekiq.md` (Status: Accepted, pois você disse que ficou decidido)

Só usei o que você contou: os incidentes de outubro, o limite de 30s, os 41 tickets, as alternativas descartadas (timeout de 120s e API de terceiros), o Sidekiq compartilhado e o fim do download imediato. Os títulos e textos estão em português. Os rótulos que o adr-tools e o importador do Structurizr leem (`Date:`, `## Status`, `Accepted` etc.) ficaram em inglês de propósito.

Duas observações:
- A renomeação do módulo de billing ficou de fora: é outro assunto e ainda não é uma decisão. Se virar uma, me avise e escrevo outro ADR.
- Uma pergunta: o ADR deve citar quem participou da sync de plataforma? Deixei de fora porque você não pediu.
