Criei o ADR em `docs/architecture/decisions/0003-version-public-api-by-url-path.md`. Não fiz commit.

Segui o formato dos ADRs 0001 e 0002, que é o de Nygard (Context, Decision, Consequences) e está em inglês. Status é "Accepted", a data é 2026-11-22, e ele tem link para o ADR 0002 (REST).

- **Decisão:** versionar a API pública por prefixo de URL (`/v1`, `/v2`) e não por header.
- **Motivos:** é o que os clientes de SDK esperam, o gateway roteia por versão e a versão fica visível em logs e `curl`.
- **Consequências:** as URLs proliferam, e manteremos no máximo duas versões ativas ao mesmo tempo.

Acrescentei por conta própria que lançar uma nova versão significa aposentar a mais antiga, então vamos precisar planejar a depreciação para os parceiros. Isso decorre do limite de duas versões, mas não foi dito por vocês, então ajuste se não refletir o combinado.
