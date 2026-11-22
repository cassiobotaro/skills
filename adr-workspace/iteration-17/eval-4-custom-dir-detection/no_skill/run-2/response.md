Criei o ADR em `docs/architecture/decisions/0003-version-public-api-by-url-path.md`. Ele segue o formato Nygard dos ADRs 0001 e 0002, e escrevi em inglês para combinar com eles. O status é Accepted, com data de hoje (2026-11-22), e há um link para o ADR 0002 (API REST).

- **Contexto:** a escolha era entre versão na URL e versão em header.
- **Decisão:** versionamento por prefixo de path (`/v1`, `/v2`), sem header de versão, com no máximo duas versões ativas ao mesmo tempo.
- **Consequências positivas:** é o que os clientes de SDK esperam, o gateway roteia só pelo path, e a versão aparece nos logs e no `curl`.
- **Consequências negativas:** as URLs proliferam, e o limite de duas versões obriga a aposentar a mais antiga antes de lançar uma terceira.

Acrescentei por conta própria que vamos precisar de um processo e um prazo de deprecação para os parceiros. Isso decorre do limite de duas versões, mas não foi algo que vocês anotaram, então ajuste ou remova se preferir.

Não fiz commit.
