Escrevi o runbook em português: `docs/runbook-exports-dead-letter-high.md`. Eu o escrevi para quem está de plantão e talvez não conheça o serviço. Não rodei nenhum comando, nem o `--dry-run`, só li o código.

O runbook segue a ordem: o alerta, o impacto, como confirmar, descobrir a causa, reenfileirar, desfazer e escalar. Os comandos vêm do `scripts/requeue_dead.py` e do `deploy/alerts.yaml`. Dois pontos que o código mostra e que o plantão precisa saber:

- **Sem registro de erro:** o worker captura toda exceção e republica a mensagem sem registrar o erro, então o log não mostra por que o pedido falhou. O runbook lista as quatro etapas que podem falhar: gerar o CSV, criptografar, gravar no S3 e enviar o e-mail pelo SES.
- **E-mail duplicado:** se a falha foi no envio do e-mail, o arquivo já está no bucket. Reenfileirar gera um arquivo novo e outro e-mail, e o runbook avisa isso antes do passo.

**O que ficou como `TODO` no documento**, porque o repositório não diz e eu não quis inventar:
1. Quem escalar: time dono do `exporter`, ordem de acionamento e canal (Slack, telefone ou ferramenta de plantão). Esse é o buraco que mais atrapalha na madrugada.
2. Link do painel do RabbitMQ ou Prometheus.
3. Onde ler os logs do worker e como inspecionar o corpo de uma mensagem em `exports.dead`.
4. Como o worker roda e reinicia em produção. O repositório só traz `make run-worker`, de uso local.
5. De onde vem o `QUEUE_URL` de produção, e onde rodar os comandos.
6. A urgência real (SLA, horário comercial ou 24x7).

Se você me passar esses dados, eu preencho os `TODO`. Sem eles, o runbook responde "o que eu faço" até o ponto de escalar, mas não diz para quem.

O `docs/pipeline.md` está em inglês. Escrevi em português porque você pediu, então os docs do repositório agora têm dois idiomas.
