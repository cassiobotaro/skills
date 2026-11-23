Escrevi o runbook em português em `docs/runbooks/exports-dead-letter-high.md`. Ele tem lacunas marcadas com `TODO`, porque o repositório não traz algumas informações e eu não quis inventá-las.

Escrevi para o plantonista que pode ser novo no serviço. O runbook segue esta ordem:
1. Confirmar o alerta.
2. Checar o worker.
3. Achar a causa.
4. Corrigir a causa.
5. Reenfileirar com `scripts/requeue_dead.py`.

Ele também diz como desfazer o reenfileiramento e quando escalar.

**Lacunas (cada uma é um `TODO` no texto):**
- **Escalonamento:** não há contato, canal nem rotação de segundo nível no repositório. Isso é o que mais faz falta, então me passe esses dados.
- **Urgência:** não achei prazo nem clientes críticos para medir o impacto.
- **Worker em produção:** o repositório não diz como ele roda, como ver o estado dele nem como reiniciá-lo.
- **Logs do worker:** o repositório não diz onde ficam.
- **`QUEUE_URL`:** não sei de onde o plantonista pega a URL do broker de produção.
- **Registro do incidente:** não sei onde registrar.

**Pontos para você conferir:**
- O `worker.py` captura qualquer exceção e não a registra em log. O runbook diz isso e lista as causas possíveis (`EXPORT_KEY`, bucket, SES, payload) a partir do código. São suspeitas, não causas confirmadas. Vale registrar a exceção no worker.
- O `--dry-run` do script devolve cada mensagem à fila com `nack`. Pelo código, ele pode contar a mesma mensagem várias vezes. O runbook manda confirmar o total pela métrica.
- O script publica sem o cabeçalho `x-attempts`, então cada mensagem reenfileirada ganha mais três tentativas. O runbook avisa disso antes do passo.

Não rodei nenhum comando: nem o script, nem as consultas do Prometheus.
