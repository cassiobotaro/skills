Criei o ADR 4 e marquei o ADR 2 como substituído. Não commitei nada e não rodei nenhum teste, porque são só arquivos de documentação.

- **`doc/adr/0004-use-stateless-jwt-for-sessions.md`** (novo): status Accepted, com a linha "Supersedes" apontando para o ADR 2. Usei o mesmo formato dos outros ADRs, com data 2026-11-22.
  - **Contexto:** o Redis virou ponto único de falha no multi-região e o custo de replicação não compensa.
  - **Decisão:** tokens JWT stateless, assinados, com expiração de 15 minutos e validação local.
  - **Consequências:** o Redis sai do caminho de login. Em troca, a revogação imediata deixa de existir, e o ADR diz isso explicitamente. O "logout em todos os lugares com um DELETE" também some.
- **`doc/adr/0002-store-sessions-in-redis.md`**: o status mudou de "Accepted" para "Superseded by 4", com link. O resto do texto ficou como estava, porque o ADR antigo continua sendo o registro histórico.

Acrescentei por conta própria, na seção de consequências, dois pontos que você não mencionou:

- Com tokens de 15 minutos, o cliente vai precisar de um mecanismo de refresh para não forçar novo login. O ADR diz que isso fica para outra decisão.
- A gestão e a rotação das chaves de assinatura entre regiões também passam a ser necessárias.

Se vocês já decidiram alguma dessas duas coisas, me diga e eu incorporo ao texto.
