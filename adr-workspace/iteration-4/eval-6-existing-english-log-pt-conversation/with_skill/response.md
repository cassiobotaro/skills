Registrei a decisão como **ADR 3**, em `doc/adr/0003-use-redis-for-user-session-cache.md`.

Uma observação importante: o seu log de decisões já existe e está escrito em **inglês** (as ADRs 0001 e 0002). Para manter o log consistente — um log em dois idiomas é pior do que em qualquer um deles —, escrevi esta nova ADR também em inglês, mesmo conversando com você em português. O conteúdo segue fielmente o que você descreveu:

- **Context**: as sessões hoje ficam no PostgreSQL (o armazenamento primário, conforme a ADR 0002), o que adiciona carga de leitura ao banco principal e exige limpeza explícita das sessões expiradas.
- **Decision**: passar a guardar as sessões no Redis, usando a expiração automática de chaves.
- **Consequences**: menos carga de leitura no PostgreSQL e expiração automática das sessões; em contrapartida, mais um componente de infraestrutura para operar e o risco de perder as sessões se o Redis reiniciar sem persistência.

Não criei nenhum link de supersede/amend para a ADR 0002, porque essa decisão não a reverte: o PostgreSQL continua sendo o armazenamento primário do serviço; apenas o cache de sessões foi movido para o Redis.

Arquivos:
- Criado: `doc/adr/0003-use-redis-for-user-session-cache.md`

Se você preferir que eu mantenha o log em português daqui para frente (e, opcionalmente, traduza as ADRs já existentes), é só dizer.
