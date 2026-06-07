Registrei a decisão como ADR 3.

**Arquivo criado:** `docs/architecture/decisions/0003-version-the-public-api-by-url-path.md`

Uma observação sobre o idioma: seu log de decisões já existente (ADRs 0001 e 0002, no diretório que o `.adr-dir` aponta, `docs/architecture/decisions`) está escrito em inglês. Para um log de decisões, a consistência interna vale mais do que o idioma da conversa — um log em dois idiomas é pior do que um log inteiro em qualquer um deles. Por isso escrevi a ADR 3 em inglês também, acompanhando 0001 e 0002. Se você quiser, posso traduzir o log inteiro para português (as três ADRs de uma vez), mas não traduzo só a nova.

A ADR não supersede nem emenda nenhuma das anteriores: a ADR 0002 escolheu expor a API como REST, e esta apenas acrescenta a estratégia de versionamento por cima dela — as duas continuam válidas.

O conteúdo, resumido:

- **Context:** a API pública precisa de um esquema de versionamento explícito; as opções na mesa eram versão no path da URL (`/v1`, `/v2`) ou em header.
- **Decision:** "We will version the public API by URL path … instead of carrying the version in a request header."
- **Consequences:** os três pontos a favor que você levantou (é o que os clientes de SDK já esperam, o gateway roteia direto pelo path, e a versão fica visível em logs e curl) e o ponto contra que vocês anotaram — as URLs proliferam, e por isso vamos manter no máximo duas versões ativas ao mesmo tempo, aposentando as mais antigas.

Os arquivos estão em formato adr-tools puro, então `adr list`, `adr generate toc` e `adr generate graph` continuam funcionando sem alteração.
