Escrevi o runbook em português: `docs/runbooks/exports-dead-letter-high.md`. Não executei nenhum comando, nem o `--dry-run`.

Eu o escrevi para a pessoa de plantão que não conhece o `exporter`. Os passos são: confirmar o tamanho da fila `exports.dead`, achar a causa, corrigir, recolocar as mensagens na fila (primeiro um lote de 10, depois o resto) e escalar. O limiar (>10 por 5 min), a severidade `page` e os comandos de requeue vêm de `deploy/alerts.yaml` e `scripts/requeue_dead.py`.

**O que o runbook avisa.** O worker captura qualquer exceção e não registra o erro em log, então o log dele não mostra a causa. Por isso o passo 2 lista hipóteses tiradas do código: S3, SES, `EXPORT_KEY` e o formato do payload. Todas estão marcadas como não confirmadas. O runbook também diz para não recolocar mensagens na fila antes de achar a causa, porque cada uma falharia mais três vezes. O fim do documento sugere registrar a exceção em `exporter/worker.py`.

**Pontos que ficaram como `TODO` no documento, porque o repositório não responde:**
- Quem é o dono do serviço, o canal de escalonamento e o contato de segunda linha.
- O SLA de resposta para o alerta.
- Quais são os ambientes e como acessá-los.
- Onde ficam o painel do RabbitMQ e os comandos para checar S3, SES e variáveis do deploy.
- Como fazer o deploy de uma correção e como disparar uma exportação de teste.

Se você me passar essas respostas, eu preencho os `TODO`.

O português segue o seu pedido. O resto de `docs/` está em inglês.
