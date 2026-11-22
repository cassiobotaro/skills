Criei o ADR 3, com status `Accepted`:

`docs/architecture/decisions/0003-version-public-api-by-url-path.md`

- **Decisão:** versionar a API pública por URL (`/v1`, `/v2`) em vez de header de versão.
- **Contexto:** os clientes de SDK já esperam a versão na URL, dá para rotear por versão no gateway, e a versão fica visível em logs e `curl`.
- **Consequências:** as URLs proliferam, e vamos manter no máximo duas versões ativas ao mesmo tempo. Também listei os ganhos que você deu.

Escrevi o ADR em inglês, não em português. Os ADRs 1 e 2 do log já estão em inglês, e um log em dois idiomas fica pior do que em um só. Os rótulos `Date:`, `## Status` e os outros cabeçalhos ficam em inglês de qualquer forma, porque o adr-tools e o importador do Structurizr leem esses termos. Se preferir o texto em português, é só pedir.

Só usei o que você disse. Não inventei alternativas além do header de versão nem outras consequências. Nenhum ADR existente foi alterado, porque esta decisão não substitui nem emenda o ADR 2.
