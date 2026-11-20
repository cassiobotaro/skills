Escrevi a ADR da geração de PDF de fatura em background, junto com a ADR 0001 que inicia o log, porque o repositório não tinha nenhum registro de decisões ainda.

Arquivos criados:

- `doc/adr/0001-registrar-decisoes-de-arquitetura.md`: seed padrão do adr-tools ("Registrar decisões de arquitetura"), com título e texto em português e o cabeçalho `Date:`, os `##` e o status em inglês, como o adr-tools e o importador `!adrs` do Structurizr exigem.
- `doc/adr/0002-gerar-pdfs-de-fatura-em-background-via-sidekiq.md`: a decisão. Status `Accepted`. O contexto registra os três timeouts de outubro, os 41 tickets, a rejeição de subir o timeout para 120s e a rejeição da API de terceiros pelo jurídico. As consequências registram a perda do download imediato, mesmo para faturas pequenas, e a fila compartilhada com os e-mails.

Observações:

- O nome do arquivo 0002 foi transliterado para ASCII (`gerar-pdfs-de-fatura-...`). O seed 0001 também foi transliterado (`registrar-decisoes-de-arquitetura`), removendo acentos do slug. Se a convenção do time for manter os acentos no nome do arquivo, me avise.
- A renomeação do módulo de billing não entrou: é outra decisão e ainda não foi tomada. Quando o time decidir, ela vira uma ADR própria.
- Não registrei nomes de pessoas (Rafael, Marta) no texto, para a ADR ficar impessoal.

Perguntas:

1. A data de hoje (2026-11-20) está correta para o campo `Date:` da 0002, ou a decisão foi tomada na sync de quinta e você prefere a data dela?
2. O time já aceitou formalmente a perda do download imediato, ou ainda há gente que não concordou? Se alguém discordar, eu mudaria o status para `Proposed`.
