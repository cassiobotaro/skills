Registrei a decisão como ADR 3.

**Arquivo criado:** `docs/architecture/decisions/0003-version-the-public-api-by-url-path.md`

O diretório veio do `.adr-dir` do repositório (`docs/architecture/decisions`), então gravei lá em vez do `doc/adr` padrão. O número 3 é o próximo na sequência, depois de `0002-expose-public-api-as-rest.md`.

Uma observação: o log existente (ADRs 1 e 2) está escrito em inglês, e mantive o novo ADR em inglês para o log não ficar bilíngue. Se você preferir passar o log para português, me avise — mas aí vale traduzir os anteriores junto.

Conteúdo do registro:

- **Context** — a necessidade de um esquema de versionamento para a API pública e as duas opções que estavam na mesa (path na URL vs. header), com as forças que você citou: expectativa dos clientes de SDK, roteamento por versão no gateway, visibilidade em logs e `curl`.
- **Decision** — versionar por path, com a versão maior no primeiro segmento (`/v1`, `/v2`), e não usar header de versão.
- **Consequences** — os ganhos acima e o contra que vocês anotaram: proliferação de URLs, limitada pelo compromisso de manter no máximo duas versões ativas (ou seja, lançar `/v(n+1)` implica aposentar `/v(n-1)`).

Não marquei nada como superseded: o ADR 2 (expor a API pública como REST) continua valendo — este aqui complementa, não substitui.
