Registrei a decisão como ADR 3. Estou só fechando a conferência final.

Criei `doc/adr/0003-use-redis-for-user-session-cache-instead-of-postgresql.md`, com status `Accepted` e data 2026-11-22.

- **Idioma:** o log existente está em inglês, então escrevi o título e o texto em inglês para manter tudo consistente. Os cabeçalhos e o `Date:` seguem o padrão do adr-tools, como nos ADRs anteriores.
- **Conteúdo:** só usei o que você informou.
  - O motivo foi tirar carga de leitura do banco principal e ter expiração automática das chaves.
  - Os trade-offs aceitos foram operar mais um componente e perder as sessões se o Redis reiniciar sem persistência.
- **ADR 2:** não marquei o ADR 2 (PostgreSQL para persistência) como superado. Ele trata da persistência principal, e esta decisão cobre só o cache de sessões. Não alterei nenhum arquivo existente.
