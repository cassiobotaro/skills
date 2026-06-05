Criei um ADR registrando a intenção de trocar o Redis.

Arquivo: `docs/adr/0001-replace-redis.md` (formato Markdown ADR, status **Proposed**).

O que considerei do repositório: este é o `session-api` e o `docker-compose.yml` roda `redis:7`, então o Redis hoje é o backing store (provavelmente das sessões). Isso ficou registrado no contexto do ADR.

Importante: o pedido foi vago e faltam informações essenciais para uma decisão de verdade, então **não inventei** nada. Deixei marcado como **TODO** no ADR, e o documento só deve sair de *Proposed* para *Accepted* depois que você responder:

1. **Por que** trocar o Redis? (custo, operação, escala, durabilidade, licença, etc.)
2. **Trocar por quê?** (cache gerenciado, Postgres, Memcached, Valkey, DynamoDB, in-process, ...)
3. **Quais dados** o Redis guarda hoje e quais os requisitos de latência/durabilidade/consistência?
4. **Qual o plano de migração/cutover** e se aceita downtime?

Já deixei pré-preenchidas as consequências e os passos de follow-up que valem independentemente da escolha (atualizar `docker-compose.yml`, configuração de conexão, setup de dev/CI e documentação; risco de migração e de dependências de recursos específicos do Redis como TTL, pub/sub, operações atômicas e scripts Lua).

Se você me passar a tecnologia alvo e o motivo da troca, eu completo as seções de Decisão, Opções Consideradas e Consequências e marco o ADR como Accepted.
