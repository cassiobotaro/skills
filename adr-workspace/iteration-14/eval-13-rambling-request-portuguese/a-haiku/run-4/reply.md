Escrevi o ADR da decisão de mover a geração de PDF das faturas para um job em background.

Arquivos criados (o repositório não tinha log de ADRs, então comecei um em `doc/adr/` com o ADR 0001 padrão, "Registrar decisões de arquitetura", e a decisão de vocês entrou como 0002):

- `doc/adr/0001-registrar-decisoes-de-arquitetura.md`
- `doc/adr/0002-gerar-pdfs-de-fatura-em-background.md`

O ADR 0002 está como `Accepted`, porque a decisão já foi tomada na sync de plataforma. Ele registra o contexto (os três timeouts de outubro, os 41 tickets, o limite de 30 segundos do load balancer), as duas alternativas descartadas (subir o timeout para 120s e a API de PDF de terceiros) e a decisão em si. Nas consequências entraram o fim do download imediato, mesmo para faturas pequenas, o caminho de código único e o risco para a fila do Sidekiq compartilhada com e-mails.

Deixei de fora a renomeação do módulo de billing porque não é uma decisão tomada, então não há o que registrar. Se quiserem, dá para abrir um ADR quando alguém decidir o novo nome.

Não tenho perguntas bloqueantes. Só para confirmar: o diretório `doc/adr/` já existia vazio no repositório, então usei esse caminho padrão e não criei um `.adr-dir`.
