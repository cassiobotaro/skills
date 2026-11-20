Pronto. Como o projeto ainda não tinha um log de ADRs, criei o `doc/adr/` na raiz com a seed padrão ("Registrar decisões de arquitetura") como `0001` e registrei a geração do PDF como `0002`, com status `Accepted`, já que a decisão foi tomada na sync de plataforma.

Duas observações:

- O renomear do módulo de billing não entrou no ADR, porque é uma decisão separada (e ainda não tomada). Se quiser, dá para escrever um ADR próprio quando ela for decidida.
- O ADR registra só o que você contou: o incidente de outubro, as duas alternativas descartadas (timeout de 120s e API de terceiros) e as consequências aceitas (download não imediato, fila compartilhada com e-mails). Não coloquei motivações que você não citou.

Duas perguntas, caso queira o registro mais completo depois:

1. O link enviado por e-mail tem validade ou exige login para baixar? Isso não estava na conversa, e o ADR não diz nada sobre acesso ao bucket.
2. Existe alguma medida para o caso de o job de geração falhar (retry, aviso ao suporte, reenvio)? Se existir, vale registrar como consequência.

Arquivos criados:
- /home/cassiobotaro/Projetos/skills/adr-workspace/iteration-15/eval-13-rambling-request-portuguese/a-haiku/run-4/outputs/doc/adr/0001-registrar-decis-es-de-arquitetura.md
- /home/cassiobotaro/Projetos/skills/adr-workspace/iteration-15/eval-13-rambling-request-portuguese/a-haiku/run-4/outputs/doc/adr/0002-gerar-o-pdf-da-fatura-em-background-fora-da-request-web.md
