Registrei a decisão como ADR 3 no seu log de decisões.

O `.adr-dir` aponta para `docs/architecture/decisions`, então gravei lá, dando sequência aos ADRs 0001 e 0002 que já existiam.

**Arquivo criado:**
- `docs/architecture/decisions/0003-version-the-public-api-by-url-path.md`

Conteúdo (em inglês, como manda o formato adr-tools):
- **Status:** Accepted
- **Context:** a necessidade de uma estratégia de versionamento, as duas opções (path na URL vs. header) e as forças que você citou — SDKs já assumem path versionado, o gateway roteia por requisição, e a URL aparece em logs/curl.
- **Decision:** "We will version the public API by URL path (`/v1`, `/v2`...)" em vez de header.
- **Consequences:** os três pontos a favor (SDKs continuam funcionando, roteamento direto no gateway, versão óbvia em logs e curl) e o contra que você anotou — URLs proliferam, com a mitigação de manter no máximo duas versões ativas ao mesmo tempo.

Não criei link de supersessão: essa decisão complementa o ADR 2 (expor a API como REST), não o substitui.

O arquivo está no formato adr-tools padrão, então `adr list`, `adr generate toc` e `adr generate graph` funcionam sem ajustes.
