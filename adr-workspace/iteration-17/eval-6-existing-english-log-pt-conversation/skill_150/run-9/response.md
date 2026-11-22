Registrei a decisão como ADR 3, em `doc/adr/0003-use-redis-for-user-session-cache.md`.

- **Status:** `Accepted`, com data 2026-11-22.
- **Contexto e decisão:** usei só o que você disse. Os motivos são tirar carga de leitura do PostgreSQL principal e ter expiração automática das chaves. A decisão é usar Redis para o cache de sessões no lugar do PostgreSQL.
- **Consequências:** registrei os dois lados. De bom, a leitura de sessões sai do banco e a expiração é automática. De ruim, há mais um componente de infraestrutura para operar, e as sessões se perdem se o Redis reiniciar sem persistência. Marquei esse último ponto como trade-off aceito.

O log existente (ADRs 1 e 2) está em inglês, então escrevi o título e o texto em inglês para manter o log num idioma só. Os rótulos `Date:`, `## Status` e os demais seguem o padrão do adr-tools, que é em inglês.

Não marquei o ADR 2 como superseded nem como amended. O PostgreSQL continua sendo a persistência principal, e esta decisão só tira as sessões dele. Por isso não editei nenhum arquivo existente.

Não rodei nenhuma verificação automática. Reli o texto contra o que você escreveu e tirei uma frase que eu tinha acrescentado sobre o PostgreSQL não ter expiração nativa de linhas, porque você não disse isso.
