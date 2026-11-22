Registrei a decisão como ADR 3, em `doc/adr/0003-use-redis-for-user-session-cache.md`. O status é `Accepted` e a data é 2026-11-22.

- **Idioma:** o log existente (ADRs 1 e 2) está em inglês, então escrevi o título e o texto em inglês para manter o log num idioma só. Se preferir o log em português, traduzo.
- **Decisão:** usaremos Redis como cache das sessões de usuário, em vez de guardá-las no PostgreSQL, com expiração automática das chaves.
- **Contexto:** o motivo é tirar a carga de leitura das sessões do banco principal e ter expiração automática. Citei só isso, sem acrescentar motivos que você não deu.
- **Consequências:** registrei os dois ganhos (menos leitura no PostgreSQL e expiração automática). Registrei também os dois custos que você aceitou: mais um componente de infraestrutura para operar, e perda das sessões se o Redis reiniciar sem persistência.
- **ADR 2:** não o marquei como superseded. Ele trata da persistência principal, que continua no PostgreSQL. O ADR 3 só faz referência a ele no Context.

Arquivo criado: `doc/adr/0003-use-redis-for-user-session-cache.md`. Nenhum outro arquivo foi alterado.
