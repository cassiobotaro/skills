Escrevi o runbook em português: `docs/runbook-exports-dead-letter-high.md`. Ele deixa três pontos marcados como `TODO`, porque nada no repositório os responde.

A regra do alerta, o resumo do pager e os comandos vêm de `deploy/alerts.yaml` e de `scripts/requeue_dead.py`. Os passos são: confirmar com `--dry-run`, achar a causa, devolver os jobs aos poucos e confirmar a recuperação. O runbook avisa que o `requeue_dead.py` não tem como ser desfeito e que zera as tentativas de cada job.

**Leitor assumido:** a pessoa de plantão, que pode não conhecer o serviço `exporter`.

**Perguntas em aberto** (cada uma é um `TODO` no documento):
1. **Contato e escalação.** Quem é o dono do `exporter`, qual canal ou escala de plantão chamar, e em quanto tempo escalar? Não inventei nome nem canal.
2. **Acessos.** Onde o plantão pega o `QUEUE_URL` e o acesso ao RabbitMQ, ao dashboard e aos logs?
3. **Logs do worker.** `exporter/worker.py` captura qualquer exceção e não registra o erro. A mensagem em `exports.dead` também não traz o motivo. Por isso o passo "achar a causa" lista só as dependências que o código chama: `EXPORT_KEY`, o bucket S3, o SES e os dados do job. Recomendo o worker passar a registrar o erro, mas isso é uma mudança de código e eu não a fiz.

**Não executei nenhum comando.** Nem o `--dry-run` rodei, porque ele precisa de acesso ao RabbitMQ real. Também não incluí comandos de `rabbitmqctl`, S3 ou SES, já que nenhum aparece no repositório.
