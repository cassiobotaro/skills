Escrevi a ADR da decisão de tirar a geração de PDF da request web e movê-la para background, pelo Sidekiq que já existe, com o link enviado por e-mail.

Como o repositório não tinha log de decisões, criei o log em `doc/adr/` com a seed padrão `0001-record-architecture-decisions.md` (traduzida para português no título e no corpo, com os cabeçalhos em inglês para o adr-tools e o importador do Structurizr continuarem lendo). A decisão do time virou a `0002-gerar-pdfs-de-fatura-em-background-fora-da-request-web.md`, com status `Accepted`, porque a sync de quinta já a fechou.

Pontos da conversa que registrei:
- Contexto: os três timeouts de outubro, os 4 mil itens de linha, o limite de 30s do load balancer e os 41 tickets.
- Alternativas descartadas, com o motivo dado por vocês: subir o timeout para 120s e a API de PDF de terceiros (o jurídico não aceita dado de fatura fora da infraestrutura).
- Consequências, todas: o download imediato some até para faturas pequenas (aceito pelo time), há um único caminho de código, e a fila do Sidekiq é compartilhada com o time de e-mail, que sabe do risco.

Deixei de fora a renomeação do módulo de billing. Ela não é uma decisão arquitetural já tomada, então não entra em um ADR. Se quiserem registrá-la, vale um ADR próprio quando a mudança for decidida.

Uma pergunta: a ADR diz que o cliente depende do e-mail para receber o link. Se houver um caminho de consulta na própria tela de faturamento para quem não recebeu o e-mail, me avisem, porque isso muda a seção de Consequências.
