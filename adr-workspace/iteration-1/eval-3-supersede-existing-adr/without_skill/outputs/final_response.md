Criei um novo ADR substituindo o ADR 2 e atualizei o status do antigo, seguindo a convenção do adr-tools (Michael Nygard) já usada no repositório.

## O que foi feito

**Novo: `doc/adr/0004-use-stateless-jwt-tokens-for-sessions.md`**
- Status: `Accepted` + `Supersedes [2. Store sessions in Redis]`
- Contexto: explica que o cluster Redis virou ponto único de falha nos deploys multi-região e que manter ele replicado não compensa o custo.
- Decisão: passar a usar tokens JWT stateless (sessão carregada no próprio token assinado), com expiração curta de 15 minutos.
- Consequências: remoção da dependência de Redis no caminho de login e do SPOF multi-região; validação sem round-trip a um session store; e o trade-off aceito de não conseguir revogar sessão imediatamente, mitigado pela expiração de 15 minutos.

**Modificado: `doc/adr/0002-store-sessions-in-redis.md`**
- Status alterado de `Accepted` para `Superseded by [4. Use stateless JWT tokens for sessions]`, com link para o novo ADR.

## Observações

- Numerei como ADR 4 porque o repositório já tinha o ADR 3 (gRPC), então o próximo número livre é o 4. A relação de substituição é registrada via Supersedes/Superseded by, não pela renumeração.
- O conteúdo dos ADRs está em inglês para manter consistência com os ADRs existentes do repositório.
