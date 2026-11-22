Escrevi o ADR em `docs/architecture/decisions/0003-version-the-public-api-by-url-path.md`, com status `Accepted` e data 2026-11-22. Não alterei nenhum outro arquivo.

- **Idioma:** o log existente (ADRs 1 e 2) está em inglês, então escrevi o título e o texto em inglês para manter o log num idioma só. Os rótulos (`Date:`, `## Status`, etc.) seguem o padrão do adr-tools.
- **Contexto:** registrei só o que você disse: SDKs já esperam versão na URL, e a alternativa considerada era o header.
- **Consequências:** entraram os três ganhos (SDKs, roteamento no gateway, visibilidade em logs e `curl`) e os dois custos que você anotou (proliferação de URLs e no máximo duas versões ativas).
- **Acréscimo meu:** na última consequência escrevi que uma versão antiga precisa ser aposentada antes de uma terceira entrar no ar. É só o que decorre do limite de duas versões, mas não foi dito por você. Se não refletir o combinado, é fácil tirar.
