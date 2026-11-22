Registrei a decisão como ADR 3, com status `Accepted` e a data de hoje (2026-11-22):
`docs/architecture/decisions/0003-version-the-public-api-by-url-path.md`

- **Idioma:** o log existente (ADRs 1 e 2) está em inglês, então escrevi o título e o texto em inglês para manter o log num idioma só. Os cabeçalhos e o `Date:` seguem o formato do adr-tools.
- **Contexto:** só tem o que você me passou. Os motivos são que os SDKs já esperam versão na URL, que o gateway consegue rotear por versão, e que a versão aparece em logs e `curl`. A alternativa considerada foi o header de versão.
- **Decisão:** versionar por URL (`/v1`, `/v2`), com no máximo duas versões ativas ao mesmo tempo.
- **Consequências:** listei os benefícios e os dois contras que você anotou, a proliferação de URLs e o limite de duas versões. Acrescentei uma consequência que você não citou, mas que decorre do limite: para lançar uma versão nova, uma antiga precisa ser desativada antes. Se isso não reflete o que o time pensa, é só tirar essa frase.

Não alterei nenhum ADR anterior, porque a decisão não substitui o ADR 2 (REST). Ela complementa esse ADR.
