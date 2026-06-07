Registrei a decisão como um novo ADR.

**Arquivo criado:** `docs/architecture/decisions/0003-version-the-public-api-by-url.md`

Uma observação importante sobre o idioma: o `.adr-dir` aponta o log para `docs/architecture/decisions`, e os ADRs que já existem lá (0001 e 0002) estão em inglês. Como consistência do log vence o idioma da conversa, escrevi o novo ADR em inglês para não deixar o log misturado. Se você preferir manter o log em português daqui pra frente, me avise — mas aí o ideal seria migrar os anteriores também.

O ADR ficou como **0003** (próximo número na sequência) com status **Accepted**, e cobre:

- **Context**: a necessidade de uma estratégia explícita de versionamento e as duas opções avaliadas (versão na URL vs. header), com os motivos a favor do path — SDKs já esperam assim, dá pra rotear por versão no gateway, e fica visível em logs e `curl`.
- **Decision**: "We will version the public API in the URL path (`/v1`, `/v2`)…".
- **Consequences**: os pontos positivos e o contrapeso que vocês anotaram — as URLs proliferam, e por isso vamos manter no máximo duas versões ativas ao mesmo tempo.

Não mexi no ADR 0002 (REST): ele continua válido e não falava de versionamento, então não há nada a substituir nem emendar — esta é uma decisão nova e independente.

Os arquivos seguem o formato padrão do adr-tools, então `adr list` e `adr generate toc`/`graph` funcionam neles sem alteração.
