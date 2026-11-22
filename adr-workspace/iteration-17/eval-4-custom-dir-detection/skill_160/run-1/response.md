Registrei a decisão como ADR 3, com status `Accepted` e data de hoje (2026-11-22). O arquivo é `docs/architecture/decisions/0003-version-the-public-api-by-url-path.md`, no diretório que o `.adr-dir` aponta.

- **Idioma:** o log existente (ADRs 1 e 2) está em inglês, então escrevi o título e o texto em inglês para manter o log num idioma só. O formato segue o do `adr-tools`.
- **Contexto:** descreve só a pergunta, URL (`/v1`, `/v2`) ou header de versão.
- **Decisão:** traz os três motivos que você deu: SDKs já esperam URL, roteamento por versão no gateway, e a versão fica óbvia em logs e `curl`.
- **Consequências:** inclui o contra que vocês anotaram: as URLs proliferam e vamos manter no máximo duas versões ativas ao mesmo tempo.
- **Alternativas:** a única que aparece é o header de versão. Não inventei outras.
- **Outros ADRs:** nenhum foi alterado. O ADR 2 (REST) continua válido, e este não o substitui.
