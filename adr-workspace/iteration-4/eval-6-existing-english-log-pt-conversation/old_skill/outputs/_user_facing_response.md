Registrei a decisão como uma nova ADR:

- **`doc/adr/0003-use-redis-for-user-session-cache.md`** (ADR 3, status `Accepted`)

Uma observação importante: o seu log de decisões já existe e está **todo em inglês**
(ADRs 0001 e 0002). Para que o log permaneça consistente de ponta a ponta — um log
misturando dois idiomas é pior do que qualquer um deles —, escrevi esta ADR também em
inglês, seguindo o idioma do log e não o da nossa conversa. Se preferir, posso passar o
log inteiro para português, mas aí o ideal é migrar todas as ADRs de uma vez.

O conteúdo registra exatamente o que você descreveu:

- **Context**: hoje as sessões ficam no PostgreSQL (que também é a camada de persistência
  principal), cada requisição soma carga de leitura ao banco principal, e o PostgreSQL não
  tem expiração automática de chaves.
- **Decision**: "We will use Redis to store the user session cache, instead of keeping
  sessions in PostgreSQL", usando o TTL nativo do Redis para expiração.
- **Consequences**: tira carga de leitura do banco principal e ganha expiração automática
  via TTL — e, como trade-offs aceitos, mais um componente de infraestrutura para operar e
  perda de sessões se o Redis reiniciar sem persistência.

Não foi necessário supersede/amend: a ADR 0002 (PostgreSQL como persistência principal)
continua valendo — esta decisão apenas tira as sessões do banco principal, não substitui
o PostgreSQL.

Os arquivos estão no formato adr-tools padrão, então `adr list`, `adr generate toc` e
`adr generate graph` funcionam normalmente.
