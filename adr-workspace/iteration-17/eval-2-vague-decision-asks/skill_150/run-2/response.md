Ainda não escrevi o ADR. O repositório está vazio: não tem log de ADRs nem qualquer menção ao Redis. Preciso de alguns fatos seus, porque não quero inventar o motivo da decisão.

1. **Pelo que vamos trocar o Redis?** Pode ser Memcached, Valkey, Postgres ou outra coisa.
2. **Para que o Redis é usado hoje?** Por exemplo cache, sessões, fila ou rate limit. E por que trocar agora: custo, licença, operação, limitação técnica?
3. **Que alternativas foram consideradas** e por que perderam?
4. **Qual o custo aceito com a troca?** Por exemplo migração, perda de algum recurso ou risco de rollout.
5. **A decisão já está fechada (`Accepted`) ou ainda aguarda aprovação (`Proposed`)?**

Com isso crio o log em `doc/adr/`. O `0001` será o ADR padrão "Registrar decisões de arquitetura", e o da troca do Redis será o `0002`. A prosa fica em português, e a estrutura (`Date:`, `## Status` etc.) fica em inglês, como o adr-tools espera.
