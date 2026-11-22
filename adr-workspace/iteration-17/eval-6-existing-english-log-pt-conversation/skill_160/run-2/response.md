Registrei a decisão como ADR 3, com status `Accepted` e data 2026-11-22. O arquivo é `doc/adr/0003-use-redis-for-user-session-cache.md`.

- **Idioma:** o log existente está em inglês, então escrevi o título e o texto em inglês para manter o log consistente, mesmo você tendo escrito em português. Se preferir o log em português, traduzo esse registro. Os rótulos como `Date:` e `## Status` ficam em inglês de qualquer forma, para o `adr-tools` e o Structurizr continuarem lendo os arquivos.
- **Contexto:** usei só os motivos que você deu, ou seja, tirar carga de leitura do banco principal e ter expiração automática das chaves.
- **Consequências:** estão as duas partes do trade-off que você aceitou. Há mais um componente de infraestrutura para operar, e as sessões se perdem se o Redis reiniciar sem persistência.
- **Outros ADRs:** não alterei nenhum. Esta decisão complementa o ADR 2 (PostgreSQL para persistência) sem substituí-lo.
