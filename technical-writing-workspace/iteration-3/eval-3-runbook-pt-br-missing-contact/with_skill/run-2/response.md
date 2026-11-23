Escrevi o runbook em `docs/runbooks/exports-dead-letter-high.md`. Ele não está pronto para o plantão usar: faltam os contatos e alguns dados que o repositório não tem. Não rodei nenhum comando, nem o `--dry-run`. Os comandos e as saídas vêm de `scripts/requeue_dead.py` e do `Makefile`.

**Leitor:** assumi que quem lê é a pessoa de plantão, possivelmente nova no serviço.

**O que o runbook cobre:**
- **Alerta e impacto:** o alerta e o impacto vêm de `deploy/alerts.yaml` e do código. O cliente não recebe o e-mail e não é avisado da falha.
- **Passo 1:** confirma o alerta com `requeue_dead.py --dry-run`. O script só conta até 100 mensagens.
- **Passo 2, causa:** o worker engole a exceção sem registrar nada, então o log não mostra a causa. O runbook lista as dependências que o worker usa (`EXPORT_KEY`, S3, SES) para o plantão checar. Isso também pede uma mudança no código: o runbook propõe que o worker passe a registrar o erro.
- **Passo 5, reenfileirar:** o script não preserva `x-attempts`, então cada mensagem reenfileirada ganha mais 3 tentativas. Por isso o runbook manda corrigir a causa antes e reenfileirar um lote de 5 primeiro.

**O que ficou como `TODO` no texto e preciso que você responda:**
1. **Contatos:** quem é o plantão ou o time dono do `exporter`, qual é o canal de incidentes e como acionar o plantão de plataforma (RabbitMQ/AWS).
2. **Ambiente e prazo:** em qual ambiente e host os comandos rodam, e qual é o prazo de resposta (SLA) do alerta.
3. **Observabilidade:** onde ficam os logs do worker e os painéis de S3, SES e RabbitMQ, e como inspecionar o conteúdo de uma mensagem em `exports.dead`.
4. **Quem corrige:** quem corrige cada dependência e como.
5. **Teste de export:** como disparar um export de teste depois da correção.
6. **Prazo de escalação:** o prazo de 30 minutos para escalar é sugestão minha, não vem do repositório. Confirme ou troque.

O `docs/pipeline.md` existente está em inglês. Escrevi o runbook em português porque você pediu.
