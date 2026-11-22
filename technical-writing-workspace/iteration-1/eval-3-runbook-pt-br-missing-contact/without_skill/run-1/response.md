Escrevi o runbook em português e salvei em `runbook-exports-dead-letter-high.md`. Ele está incompleto: você precisa preencher os campos marcados com **[PREENCHER]** antes de publicar.

Não conheço o seu sistema. Por isso, a estrutura e a lógica de diagnóstico são genéricas para um alerta de dead letter queue (DLQ):

- O que o alerta significa e quando é urgente.
- Passo a passo: dimensionar o problema, ler as mensagens e os logs, classificar a causa, corrigir, reprocessar e confirmar.
- Uma tabela que liga cada sintoma a uma ação (bug após deploy, dependência fora, credencial, mensagem inválida, worker parado).
- Critérios de escalonamento.

**O que preencher:**

- **Contato de escalonamento:** você não me passou quem acionar quando o plantão não resolve. Deixei o campo em aberto e avisei no documento. Sem ele, o plantão não tem a quem recorrer.
- **Nomes e links:** a fila, a DLQ, o worker, o dashboard e a query de logs.
- **Comandos:** rollback, restart e redrive.
- **Valores:** o limite do alerta, o nível normal da DLQ e a retenção das mensagens.

Pressupus que o alerta vem de uma fila de mensagens com DLQ e que reprocessar significa reenviar as mensagens para a fila principal. Se a sua DLQ funciona de outro jeito, o passo 4 muda.
