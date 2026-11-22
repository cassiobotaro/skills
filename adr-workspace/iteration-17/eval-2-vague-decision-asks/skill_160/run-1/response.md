Não achei nenhum log de ADR no repositório, nem qualquer menção ao Redis nos arquivos. Não tenho como preencher o ADR sem inventar o motivo, então preciso de algumas respostas antes de escrever:

1. **Pelo que vamos trocar o Redis?** (Memcached, Valkey, Postgres, outra coisa?) E para que o Redis é usado hoje: cache, sessões, filas, outro?
2. **Por que trocar, e por que agora?** Qual problema o Redis causa ou qual pressão motivou a mudança (custo, licença, operação, desempenho...)?
3. **Que alternativas foram consideradas, e o que o time abre mão com a troca?** Pode ser um custo de migração, uma funcionalidade que se perde ou uma alternativa descartada.
4. **A decisão já está fechada (`Accepted`) ou ainda aguarda aprovação (`Proposed`)?**

Também não há log de ADR ainda. Quando você responder, crio `doc/adr/` com o ADR 0001 padrão ("Record architecture decisions") e a sua decisão entra como `0002`. Vou escrever em português e manter em inglês os rótulos do adr-tools (`Date:`, `## Status`, `## Context`, `## Decision`, `## Consequences`).
