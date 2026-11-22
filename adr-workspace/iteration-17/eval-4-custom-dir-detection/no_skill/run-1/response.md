Criei o ADR 3 em `docs/architecture/decisions/0003-version-public-api-by-url-path.md`, seguindo o formato Nygard dos ADRs 1 e 2. Como os anteriores estão em inglês, escrevi este em inglês também.

- **Status:** Accepted, com data de hoje (2026-11-22) e link para o ADR 2 (API REST).
- **Contexto:** a necessidade de versionar a API pública, com as duas opções consideradas: versão na URL ou em header.
- **Decisão:** versionar por prefixo de URL (`/v1`, `/v2`) e manter no máximo duas versões ativas ao mesmo tempo.
- **Consequências:**
  - Positivas: os SDKs já esperam esse formato, o gateway roteia por versão e a versão fica visível em logs e `curl`.
  - Negativas: as URLs proliferam, e é preciso aposentar a versão mais antiga antes de lançar uma terceira.

Não commitei nada. Se preferir o texto em português, é só pedir.
