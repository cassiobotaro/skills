Boa! Posso registrar isso como o primeiro ADR do projeto (ainda não existe nenhum log de decisões aqui, então vou começar um em `doc/adr/`). Mas "trocar o Redis" sozinho não dá pra escrever um ADR honesto — um ADR vale justamente pelo *porquê*, e eu não quero inventar motivos que vocês não decidiram. Me ajuda com 3 coisinhas:

1. **Trocar o Redis por o quê?** Qual a tecnologia/solução que vai entrar no lugar (ex.: Valkey, Memcached, Postgres, DragonflyDB, KeyDB...)?

2. **Por que agora?** O que está incomodando no Redis hoje — custo, licença (a mudança pra licença SSPL/RSAL?), performance, operação, algum limite que bateram? Esse é o ponto mais importante.

3. **Qual o custo que vocês toparam pagar?** Todo ADR tem trade-off: o que fica mais difícil/arriscado com essa troca (migração de dados, retreinar o time, perder algum recurso específico do Redis, downtime)?

E só pra confirmar: essa decisão já está **fechada** (Accepted) ou ainda é uma **proposta** que falta alguém aprovar (Proposed)?

Assim que você me passar isso, eu já gero o arquivo. Como o log vai começar agora, eu também crio o ADR-0001 padrão ("Registrar decisões de arquitetura") e a sua decisão entra como ADR-0002 — tudo no formato adr-tools, em português, pra ficar consistente.
