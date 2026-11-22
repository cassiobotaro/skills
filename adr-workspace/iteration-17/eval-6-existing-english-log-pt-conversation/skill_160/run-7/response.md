Registrei a decisão em `doc/adr/0003-use-redis-for-user-session-cache.md`, com status `Accepted` e data de hoje (2026-11-22). Não editei nenhum outro arquivo.

- **Idioma:** o log existente (ADRs 0001 e 0002) está em inglês, então escrevi o título e o texto em inglês para manter o log consistente. Os rótulos (`Date:`, `## Status`, `## Context` etc.) seguem o padrão do adr-tools.
- **Contexto:** só usei o que você disse. A alternativa era guardar as sessões no PostgreSQL, o que poria a carga de leitura no banco principal. O Redis dá expiração automática das chaves.
- **Consequências:** registrei os dois lados.
  - Ganhos: a leitura de sessões sai do PostgreSQL e as chaves expiram sozinhas.
  - Custos aceitos: mais um componente de infraestrutura para operar, e as sessões se perdem se o Redis reiniciar sem persistência.
- **ADR 0002:** não marquei como superado. Ele trata do PostgreSQL como persistência principal, e essa decisão continua valendo. O ADR novo só tira as sessões do banco.
