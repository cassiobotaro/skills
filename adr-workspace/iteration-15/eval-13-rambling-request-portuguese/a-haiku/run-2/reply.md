Oi! Escrevi o ADR da decisão de tirar a geração do PDF da request web e mandar para background no Sidekiq. Como o repositório estava vazio, criei o log em `doc/adr/` com o seed padrão, "Registrar decisões de arquitetura", como `0001`, e o ADR da decisão é o `0002`.

Arquivos criados:
- `doc/adr/0001-registrar-decis-es-de-arquitetura.md`
- `doc/adr/0002-gerar-pdf-de-fatura-em-background-fora-da-request-web.md`

Algumas coisas que ficaram de fora ou que vale confirmar:

1. O ADR está como `Accepted`, porque vocês disseram que ficou decidido. Se alguma parte ainda depende de aprovação, me avise para marcar como `Proposed`.
2. A renomeação do módulo de billing não entrou. Ainda não foi decidida, então não há o que registrar. Quando houver uma decisão, vale um ADR próprio.
3. O Context usa só o que vocês contaram: os incidentes de outubro, os 41 tickets e as duas alternativas descartadas. Se a sync de quinta tiver outros motivos, como a previsão de volume ou o custo do bucket, me passe para eu incluir. Sem isso, o registro fica com só o que foi estabelecido.
4. Se a equipe já usa um log de ADRs em outro lugar, como `docs/adr` ou um `.adr-dir`, me diga, porque eu criei um novo `doc/adr/` do zero.
