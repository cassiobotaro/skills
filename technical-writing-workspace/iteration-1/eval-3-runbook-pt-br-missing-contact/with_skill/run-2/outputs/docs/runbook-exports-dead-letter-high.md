# Runbook: ExportsDeadLetterHigh

Este runbook é para quem está de plantão quando o alerta `ExportsDeadLetterHigh` dispara. Ele diz como confirmar o alerta, como devolver os exports que falharam à fila e quando chamar outra pessoa. Ele não descreve o pipeline inteiro: para isso, leia `docs/pipeline.md`.

## O alerta

- **Regra:** `rabbitmq_queue_messages{queue="exports.dead"} > 10` por 5 minutos (`deploy/alerts.yaml`).
- **Severidade:** `page`.
- **Resumo no pager:** "More than 10 exports failed three times".

A fila `exports.dead` guarda os jobs de export que o worker tentou três vezes sem sucesso. O worker só move um job para ela depois da terceira falha, então um job parado na fila `exports` (por exemplo, porque o worker caiu) não conta para este alerta.

## Impacto

Cada mensagem em `exports.dead` é um export que o cliente pediu e não recebeu. O gateway já respondeu `202` a esse cliente, e o cliente não recebe e-mail com o link nem mensagem de erro. Mais de 10 mensagens por 5 minutos indica uma falha que se repete, e não um job isolado com problema.

## Antes de começar

Você precisa de:

- o repositório `exporter` com as dependências instaladas (`make setup`);
- a variável `QUEUE_URL` apontando para o RabbitMQ do ambiente do alerta.

`TODO: dizer onde o plantão obtém QUEUE_URL e o acesso ao RabbitMQ, ao dashboard e aos logs do worker. Nada no repositório informa.`

## 1. Confirmar que o alerta é real

Conte as mensagens de `exports.dead` sem mover nenhuma:

```
uv run python scripts/requeue_dead.py --dry-run
```

O script imprime `would move <N> message(s)`. Ele conta no máximo 100 mensagens (o `--limit` padrão). Se `<N>` for 0, a fila já esvaziou e o alerta deve resolver sozinho. Se `<N>` for maior que 10, siga para o passo 2.

O `--dry-run` devolve cada mensagem à fila com `nack` e `requeue=True`, então não perde nada.

## 2. Achar a causa

O worker (`exporter/worker.py`) captura qualquer exceção e move o job adiante sem registrar o erro. A mensagem em `exports.dead` não contém o motivo da falha. Por isso, procure a causa nas dependências que o worker chama, nesta ordem:

1. **Chave de criptografia.** O worker lê `EXPORT_KEY` e cifra o CSV com Fernet. Uma chave ausente ou inválida faz todo job falhar.
2. **Bucket S3.** O worker grava o arquivo cifrado no bucket de `EXPORT_BUCKET` com `put_object`. Verifique se o bucket existe e se o worker tem permissão de escrita.
3. **Envio do e-mail.** O módulo `exporter/notifier.py` gera o link assinado no S3 e envia o e-mail pelo SES, com remetente `MAIL_FROM`. Verifique se o SES aceita envios.
4. **Dados do job.** Se só alguns jobs falham e os outros passam, o problema está no conteúdo desses jobs, e não numa dependência.

`TODO: dizer onde ficam os logs do worker e como abri-los. O código não grava log, então confirme se algum registro da falha existe (por exemplo, no log do runtime).`

## 3. Corrigir e devolver os jobs à fila

Corrija a causa do passo 2 primeiro. Se você devolver os jobs antes disso, eles falham mais três vezes e voltam para `exports.dead`.

> **Atenção:** o script move mensagens de `exports.dead` para `exports`, e nenhum comando desfaz isso. Os jobs devolvidos recomeçam com zero tentativas (o script publica sem o cabeçalho `x-attempts`), então cada um ganha mais três tentativas.

1. Teste com uma mensagem:

   ```
   uv run python scripts/requeue_dead.py --limit 1
   ```

   O script imprime `moved 1 message(s)`.

2. Espere o worker processar o job. Se o job concluir, o cliente recebe o e-mail com o link e `exports.dead` não ganha a mensagem de volta. Se o job falhar, a mensagem volta para `exports.dead` depois de três tentativas: a causa ainda existe, volte ao passo 2.
3. Devolva o restante em lotes:

   ```
   uv run python scripts/requeue_dead.py --limit 100
   ```

   Repita até o script imprimir `moved 0 message(s)`.

## 4. Confirmar a recuperação

Rode o `--dry-run` do passo 1. O resultado esperado é `would move 0 message(s)`, ou um valor abaixo de 11 que não cresce. O alerta resolve depois que a fila fica em 10 mensagens ou menos.

## Quando escalar

Escale se:

- a causa não aparece depois de verificar os quatro itens do passo 2;
- o job de teste do passo 3 falha de novo depois da sua correção;
- a fila continua crescendo depois de você devolver os jobs.

`TODO: dizer quem é o dono do serviço exporter, como chamá-lo (canal, escala de plantão) e em quanto tempo o plantão deve escalar. Nada no repositório informa.`

## O que o repositório não confirma

Este runbook não traz comandos para o RabbitMQ (`rabbitmqctl` ou a interface de administração), para o S3 ou para o SES, porque nenhum deles aparece no repositório. Quando o time registrar esses comandos, inclua-os nos passos 1 e 2.
