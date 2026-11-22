Registrei a decisão como ADR 3 em `doc/adr/0003-use-redis-for-user-session-cache.md`, com status `Accepted` e a data de hoje, 2026-11-22.

- **Contexto e decisão:** as sessões iriam para o PostgreSQL, o que aumenta a carga de leitura no banco principal e não dá expiração automática das chaves. Vamos usar Redis para o cache de sessões. O PostgreSQL continua como camada principal de persistência, conforme a ADR 2.
- **Consequências:** os ganhos são menos leitura no banco principal e expiração automática das chaves. Os custos são um componente de infraestrutura a mais para operar e a perda de todas as sessões se o Redis reiniciar sem persistência.
- **Idioma:** o log existente está em inglês, então escrevi o título e o texto em inglês para manter a consistência. Os rótulos do formato (`Date:`, `## Status` e os demais) também seguem o padrão do adr-tools.
- **ADR 2:** não a marquei como substituída nem alterada, porque o PostgreSQL continua sendo o armazenamento principal. Nenhum arquivo existente foi modificado.

Não incluí alternativas além do PostgreSQL nem detalhes de persistência do Redis, porque você não os mencionou. Se quiser registrar a estratégia de persistência ou de recuperação de sessões, isso pode virar uma ADR nova.
