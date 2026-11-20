Escrevi o ADR e salvei no repositório. Como não havia nenhum log de decisões, criei `doc/adr/` com o ADR 0001 padrão ("Registrar decisões de arquitetura", o equivalente ao `adr init`) e a sua decisão ficou como o 0002.

- `doc/adr/0001-registrar-decis-es-de-arquitetura.md`
- `doc/adr/0002-gerar-pdfs-de-fatura-em-background-com-sidekiq.md`

O 0002 está como `Accepted`, porque você disse que ficou decidido na sync de quinta. Ele registra o contexto (3 incidentes em outubro, 4 mil itens de linha, limite de 30s, 41 tickets), as duas alternativas descartadas (timeout de 120s e API de PDF de terceiros) e as consequências que vocês aceitaram (fim do download imediato e fila compartilhada com o time de e-mail). Escrevi só o que você contou, sem acrescentar nada.

Sobre a renomeação do módulo de billing: deixei de fora de propósito. Não é uma decisão tomada e seria outro ADR. Se vocês decidirem fazer, me avise que eu registro.

Perguntas, se quiser que o ADR cubra mais:
1. O link do e-mail expira, ou exige que o cliente esteja autenticado? Não registrei nada sobre isso porque você não disse.
2. A sync teve mais alguma decisão ou ressalva (por exemplo, uma fila dedicada no futuro caso a compartilhada vire problema)? Se sim, incluo em Consequences.
