Escrevi o runbook em `docs/runbooks/exports-dead-letter-high.md`, em português. Ele tem quatro lacunas que só você consegue preencher, marcadas no texto como `TODO`.

A ordem do texto é alerta, impacto, confirmar com `requeue_dead.py --dry-run`, achar a causa, corrigir e recolocar as mensagens em lotes. O fim diz quando chamar outra pessoa.

**Perguntas em aberto (cada uma é um `TODO` no arquivo):**
1. **Contato:** quem é a equipe dona do `exporter`, qual canal ou escala de plantão chamar e em quanto tempo escalar? Não há nenhum contato no repositório, e não inventei um.
2. **Logs e painéis:** onde o plantão lê os logs do worker e o painel do RabbitMQ?
3. **`QUEUE_URL`:** de onde o plantão pega esse valor para rodar o script?
4. **Reiniciar o worker em produção:** como se faz? O `Makefile` só tem `make run-worker`, que serve para desenvolvimento.

**Dois pontos do código que o runbook trata de forma explícita:**
- O worker captura qualquer exceção e não registra o erro em log nem na mensagem. Por isso o passo "descubra a causa" lista só as dependências que o código chama (`EXPORT_KEY`, `EXPORT_BUCKET`, `MAIL_FROM`, `QUEUE_URL`). Ele deixa claro que essa lista mostra onde a falha pode nascer, e não a causa atual. A última seção sugere registrar a exceção em `exporter/worker.py`.
- `requeue_dead.py` publica a mensagem sem o contador `x-attempts`. Cada mensagem recolocada ganha três tentativas novas, e o runbook avisa isso antes do passo. Por isso ele manda corrigir a causa antes de recolocar e começar com `--limit 5`.

**Leitor assumido:** o engenheiro de plantão, possivelmente novo no serviço.

**Comandos:** não rodei nenhum. O script precisa de um RabbitMQ real. Copiei as flags `--dry-run` e `--limit` do código do script. Não usei o `unslop`, porque não está instalado nesta sessão.
