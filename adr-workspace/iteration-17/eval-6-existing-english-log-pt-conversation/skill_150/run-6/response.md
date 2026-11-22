Registrei a decisão como ADR 3, em `doc/adr/0003-use-redis-for-user-session-cache.md`, com status `Accepted` e data 2026-11-22.

- **Idioma:** o log existente (ADRs 1 e 2) está em inglês, então escrevi o título e o texto em inglês para manter a consistência. Os rótulos `Date:`, `## Status`, `## Context`, `## Decision` e `## Consequences` seguem o padrão do adr-tools.
- **Contexto:** usei só o que você informou. A alternativa era guardar as sessões no PostgreSQL, e os motivos foram tirar carga de leitura do banco principal e ter expiração automática das chaves.
- **Consequências:** listei os dois ganhos e os dois custos que você aceitou. Os custos são mais um componente de infraestrutura para operar e a perda de todas as sessões se o Redis reiniciar sem persistência.
- **ADR 2:** não o supersedi nem o emendei. O PostgreSQL continua sendo a persistência principal, então nenhum arquivo existente foi alterado.
