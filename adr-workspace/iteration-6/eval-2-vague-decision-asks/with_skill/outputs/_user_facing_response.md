Posso escrever, mas antes preciso de um pouco mais de substância — um ADR vale exatamente pelo *porquê* registrado, e "vamos trocar o Redis" ainda não me diz nem o que entra no lugar nem o que motivou a troca. Se eu preencher isso por conta própria, o registro vira ficção para quem ler daqui a dois anos.

Não achei nenhum log de decisões neste projeto (sem `.adr-dir`, sem `doc/adr/`), então este seria o primeiro: eu crio `doc/adr/`, semeio com o ADR canônico "Registrar decisões de arquitetura" (é o que o `adr init` faz) e a sua decisão fica como `0002`.

Quatro perguntas e eu escrevo:

1. **O que entra no lugar do Redis, e para qual uso?** Redis costuma acumular papéis (cache, sessões, fila, rate limiting, pub/sub) — está saindo de todos ou só de um? E o substituto é qual (Valkey, Memcached, Postgres, DragonflyDB, algo gerenciado)?

2. **Por que agora?** Qual pressão forçou a decisão — custo, licenciamento, limite de memória/performance, operação, uma incidência específica, decisão de fornecedor? É isso que vai para o Context.

3. **Que alternativas ficaram na mesa e foram descartadas?** Mesmo que a resposta seja "só avaliamos duas", quero registrar quais.

4. **Qual desvantagem o time aceitou junto?** Migração de dados, reescrita de código que usa comandos específicos do Redis, perda de alguma estrutura de dados, curva de aprendizado, risco na janela de corte. Decisão sem custo nenhum é sinal de que o custo ainda não apareceu — e Consequences precisa listar os dois lados.

Se puder, me diga também se isso já está **acordado** (status `Accepted`) ou ainda é uma proposta aguardando aval do time (`Proposed`).
