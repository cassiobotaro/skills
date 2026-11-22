Ainda não escrevi o ADR, porque faltam informações que só você tem. O repositório não tem log de decisões nem qualquer menção ao Redis, então não consigo tirar isso do código. Se eu preenchesse, estaria inventando os motivos.

1. **Qual vai ser o substituto?** Por exemplo Valkey, Memcached, Postgres ou outra coisa. E para qual uso o Redis é usado hoje: cache, sessões, filas, outro?
2. **Por que trocar, e por que agora?** Qual problema o Redis causa hoje? Pode ser licença, custo, operação ou outro motivo.
3. **Que alternativas vocês avaliaram e descartaram?** E o que vocês aceitam perder ou assumir com a troca, como esforço de migração, perda de algum recurso ou risco?
4. **A decisão já foi tomada ou ainda aguarda aprovação?** Isso define se o status é `Accepted` ou `Proposed`.

Como não existe um log, vou criar `doc/adr/`. Ele começa com o ADR 0001, "Registrar decisões de arquitetura", e a decisão sobre o Redis vira o 0002. O texto fica em português e a estrutura do adr-tools (`Date:`, `## Status`, `## Context` e assim por diante) fica em inglês.
