Registrei a decisão como ADR 3, com status `Accepted`:

`doc/adr/0003-use-redis-for-user-session-cache.md`

- **Decisão:** usar Redis como cache de sessões dos usuários, em vez de guardá-las no PostgreSQL.
- **Motivos (Context):** tirar carga de leitura do banco principal e ter expiração automática das chaves.
- **Trade-offs (Consequences):** mais um componente de infraestrutura para operar, e as sessões são perdidas se o Redis reiniciar sem persistência. Os dois ganhos também aparecem como consequências.

- **Idioma:** o log existente (ADR 1 e 2) está em inglês, então escrevi o título e o texto em inglês para manter o log consistente. Os rótulos (`Date:`, `## Status` etc.) são sempre em inglês, por compatibilidade com o adr-tools. Se preferir o texto em português, posso reescrever, mas o log ficaria com dois idiomas.
- **ADR 2:** não marquei o ADR 2 (PostgreSQL para persistência) como superseded nem emendado, porque ele continua valendo para o armazenamento principal. Só as sessões saem do PostgreSQL.
- **Alternativas:** não incluí outras alternativas além do PostgreSQL, porque você não citou nenhuma.
