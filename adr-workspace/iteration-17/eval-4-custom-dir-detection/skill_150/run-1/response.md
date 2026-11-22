Registrei a decisão como ADR 3, com status `Accepted` e data de hoje (2026-11-22):
`docs/architecture/decisions/0003-version-the-public-api-by-url-path.md`

- **Contexto:** usei só o que você me passou. Os três motivos são os clientes de SDK, o roteamento por versão no gateway e a visibilidade em logs e `curl`.
- **Decisão:** versionar por URL (`/v1`, `/v2`) em vez de header, com no máximo duas versões ativas ao mesmo tempo.
- **Consequências:** além dos pontos positivos, registrei o contra que vocês anotaram. As URLs proliferam, e criar uma nova versão obriga a aposentar a mais antiga.

O log existente (ADRs 1 e 2) está em inglês, então escrevi o título e o texto em inglês para manter o log num idioma só. Se preferir em português, é só pedir.

Não ligo este ADR ao 0002 (REST), porque ele complementa aquele e não o substitui nem o altera. Por isso não mexi em nenhum ADR existente.
