Documentei a decisão como um novo ADR, seguindo as convenções já existentes no repositório.

## O que foi feito

Criei o arquivo `docs/architecture/decisions/0003-version-the-public-api-by-url.md`.

Detectei as convenções do projeto a partir do que já existia:
- O arquivo `.adr-dir` aponta para `docs/architecture/decisions`, então o ADR foi criado nesse diretório.
- Os ADRs seguem o formato Nygard (padrão do `adr-tools`), com numeração sequencial e seções **Status / Context / Decision / Consequences**. Como já havia o `0001` e o `0002`, o novo recebeu o número `0003`.

## Conteúdo do ADR

- **Title:** 3. Version the public API by URL
- **Date:** 2026-06-04
- **Status:** Accepted
- **Context:** registra o problema (evoluir a API pública com breaking changes) e as duas opções avaliadas — versão na URL vs. header de versão. Inclui um link para o ADR 0002 (Expose public API as REST), com o qual esta decisão se relaciona.
- **Decision:** versionar a API pública por path de URL (`/v1`, `/v2`, ...) em vez de header.
- **Consequences:** os três motivos a favor (clientes de SDK já esperam, roteamento por versão no gateway, visibilidade em logs e `curl`) e o contra anotado (proliferação de URLs), com a mitigação de manter no máximo duas versões ativas ao mesmo tempo, aposentando a mais antiga quando uma terceira surgir.

O conteúdo do ADR está em inglês, alinhado com os ADRs existentes no projeto.
