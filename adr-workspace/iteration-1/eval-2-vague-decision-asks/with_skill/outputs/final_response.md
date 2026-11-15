Posso escrever o ADR, mas preciso de um pouco mais de substância antes — um ADR existe para o desenvolvedor do futuro entender o *porquê* da decisão, e se eu inventar os motivos o registro perde todo o valor (e fica enganoso). Olhei o repositório: é o `session-api` com um container `redis:7` no `docker-compose.yml`, e ainda não existe um log de decisões. Só "vamos trocar o Redis" não me diz o suficiente para preencher as seções Context / Decision / Consequences honestamente.

Me responde 3 coisas e eu já escrevo o ADR (e inicializo o log em `doc/adr/`, com o ADR seed `0001` mais a sua decisão como `0002`):

1. **Trocar o Redis por quê?** A tecnologia/serviço concreto que entra no lugar (ex.: Valkey, Memcached, Postgres, KeyDB, DragonflyDB, um cache gerenciado na nuvem...). O Redis hoje guarda o quê nesse `session-api` — sessões, cache, filas?

2. **Por que agora?** Qual a dor com o Redis atual que motiva a troca (licença/custo, escala, latência, operação, recurso que falta, decisão de fornecedor...). É isso que vai virar o Context.

3. **Qual o trade-off que vocês aceitam?** O que fica mais difícil, arriscado ou caro com a troca (migração de dados, reescrever código que usa comandos específicos do Redis, perder algum recurso, retreinar o time...). Todo ADR honesto lista pelo menos uma consequência negativa.

E, se for útil: já está **decidido e acordado** com o time (entra como `Accepted`) ou ainda é uma **proposta** aguardando aval (entra como `Proposed`)?

Me manda essas respostas que eu escrevo o ADR na hora.
