Escrevi o ADR da decisão de tirar a geração do PDF da fatura da requisição web e fazê-la em background, com o envio do link por e-mail.

Como o repositório estava vazio, criei o log em `doc/adr/`. O ADR 0001 é o seed padrão de "registrar decisões de arquitetura", traduzido para português. O ADR 0002 é a decisão em si, com status `Accepted`, já que a sync de plataforma decidiu. O contexto registra os três timeouts de outubro, os 41 tickets e as duas alternativas descartadas (subir o timeout para 120s e a API de PDF de terceiros, vetada pelo jurídico). As consequências incluem a perda do download imediato, mesmo para faturas pequenas, e o risco na fila do Sidekiq compartilhada com e-mails.

Não registrei a renomeação do módulo de billing. Não é uma decisão tomada, só uma vontade ("a gente devia renomear alguma hora"). Se virar decisão, vale um ADR próprio.

Duas perguntas, para o caso de quererem completar o ADR depois:
1. Como o link enviado por e-mail é protegido: expira, exige login, ou é público? Não encontrei isso na conversa, então não o escrevi.
2. Vocês querem registrar algum limite ou monitoramento para a fila do Sidekiq? Se sim, isso entra como consequência ou como decisão separada.
