Oi! Escrevi a decisão como ADR. Como o repositório ainda não tinha um log de decisões, criei o log em `doc/adr/` e incluí o ADR de inicialização (`0001-registrar-decis-es-de-arquitetura.md`), que é o padrão do `adr init`. A decisão da sync de plataforma ficou como `0002`.

Arquivos criados:

- `doc/adr/0001-registrar-decis-es-de-arquitetura.md`
- `doc/adr/0002-mover-a-gera-o-de-pdfs-de-fatura-para-segundo-plano.md`

O ADR 0002 está com status `Accepted`, porque o time já decidiu. Ele registra:

- **Contexto:** o PDF é gerado na requisição web; os três timeouts de outubro, com o cliente de 4 mil itens, o limite de 30 s do load balancer e os 41 tickets; as duas alternativas descartadas (subir o timeout e a API de terceiros, pelo jurídico) e a fila Sidekiq compartilhada.
- **Decisão:** gerar em background pelo Sidekiq existente, gravar no bucket de documentos e enviar o link por e-mail.
- **Consequências:** o download imediato acaba, inclusive para faturas pequenas, por escolha de não manter dois caminhos; a requisição deixa de segurar um web worker; e a fila compartilhada pode atrasar os e-mails, risco que o time de e-mail aceitou.

Não registrei a renomeação do módulo de billing. Ela não é uma decisão tomada, então não cabe num ADR. Se virar decisão, vale um ADR próprio.

Duas coisas para conferir: o título do ADR está em português e o cabeçalho `Date:` é a data de hoje (2026-11-20). Os rótulos `Date:`, `## Status`, `## Context`, `## Decision`, `## Consequences` e a palavra `Accepted` seguem em inglês de propósito, para que o `adr` e o importador `!adrs` do Structurizr continuem lendo os arquivos.
