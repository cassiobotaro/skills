Antes de escrever, preciso de algumas coisas que só você sabe — um ADR vale pelo *porquê* registrado, e eu não vou inventar motivo, alternativa ou consequência que você não disse. Do seu pedido eu tenho só metade da decisão ("vamos trocar o Redis") e nada das forças nem dos trade-offs.

Quatro perguntas rápidas:

1. **Trocar o Redis por o quê, e em qual uso?** O Redis costuma acumular papéis (cache, sessão, fila, lock distribuído, pub/sub). Está saindo de todos ou só de um? E o que entra no lugar — Valkey, Memcached, Postgres, um broker dedicado, cache em memória do próprio serviço?

2. **Por que agora?** O que está incomodando hoje: custo, mudança de licença, limite de memória/latência, dificuldade de operação, um incidente específico? É esse "o que está errado com o status quo" que dá valor ao registro.

3. **Que alternativas ficaram na mesa e por que foram descartadas?** Mesmo uma descartada rápido ajuda quem ler daqui a dois anos.

4. **Que desvantagem o time aceitou?** Toda troca cobra alguma coisa — migração de dados, reescrita de código, perder algum recurso do Redis, risco de janela de indisponibilidade. E: a decisão já está fechada (`Accepted`) ou ainda depende de aval de alguém (`Proposed`)?

Com isso eu escrevo direto. Um aviso sobre o que vou criar: aqui não existe nenhum log de decisões ainda, então vou seguir o `adr init` — crio `doc/adr/`, com o ADR inicial `0001` ("Registrar decisões de arquitetura"), e a sua decisão vira o `0002`. A prosa fica em português; só o andaime que as ferramentas leem (`Date:`, os quatro títulos `## Status`/`## Context`/`## Decision`/`## Consequences` e a palavra de status) fica em inglês, senão o `adr generate` e o importador do Structurizr param de ler o arquivo.
