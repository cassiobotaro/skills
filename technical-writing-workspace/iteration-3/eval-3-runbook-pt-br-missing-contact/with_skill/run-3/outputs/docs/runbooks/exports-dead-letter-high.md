# Runbook: ExportsDeadLetterHigh

Use este runbook quando o alerta `ExportsDeadLetterHigh` disparar. Ele diz como confirmar o alerta, como achar a causa das falhas e como recolocar na fila as exportações que falharam. Ele não explica o pipeline de exportação: para isso, leia [pipeline.md](../pipeline.md).

Quem lê: a pessoa de plantão, que pode não conhecer o `exporter`.

## O alerta

`deploy/alerts.yaml` define a regra. O alerta dispara quando `rabbitmq_queue_messages{queue="exports.dead"}` fica acima de 10 por 5 minutos. A severidade é `page`, e o resumo é "More than 10 exports failed three times".

## Impacto

Cada mensagem em `exports.dead` é uma exportação que falhou três vezes. O worker não envia o e-mail com o link de download para essas exportações, então o cliente que pediu o CSV não recebe o arquivo. O worker publica a mensagem de novo em `exports` ou em `exports.dead` antes de confirmá-la, e o script de requeue permite recuperá-la.

TODO: o prazo de resposta (SLA) para esse alerta não está no repositório. Preencha com o prazo combinado com o negócio.

## Antes de começar

- Acesso ao ambiente em que o alerta disparou. TODO: o repositório não diz quais são os ambientes nem como acessá-los.
- A variável `QUEUE_URL` definida com a URL do RabbitMQ desse ambiente. O script de requeue lê essa variável.
- O repositório clonado, com `make setup` já executado.

## 1. Confirme o tamanho da fila

Conte as mensagens sem mover nenhuma:

```bash
uv run python scripts/requeue_dead.py --dry-run --limit 1000
```

A saída esperada tem este formato, com o número de mensagens em `exports.dead` (até o limite):

```text
would move 37 message(s)
```

Se o número for 10 ou menos, o alerta já deve resolver sozinho. Se for maior, siga para o passo 2.

O `--dry-run` devolve cada mensagem à fila com `nack`, o que pode mudar a ordem delas em `exports.dead`. Isso não afeta o processamento.

## 2. Ache a causa antes de recolocar mensagens na fila

Não execute o requeue ainda. Se a causa continuar ativa, cada mensagem recolocada falha mais três vezes e volta para `exports.dead`.

O worker (`exporter/worker.py`) captura qualquer exceção do processamento e **não registra o erro em log**. Por isso, o log do worker não mostra a causa. Descubra qual etapa falha pelos serviços de que o worker depende. Em cada exportação, o worker faz estas quatro coisas, nesta ordem:

1. Gera o CSV a partir do payload.
2. Criptografa o CSV com a chave de `EXPORT_KEY`.
3. Grava o arquivo no bucket S3 de `EXPORT_BUCKET`.
4. Envia o e-mail com o link pelo SES, usando o remetente de `MAIL_FROM`.

Verifique cada dependência, da mais provável à menos provável. O código permite estas hipóteses; nenhuma está confirmada:

| Hipótese | O que verificar |
|---|---|
| O S3 recusa a gravação (permissão, bucket inexistente ou indisponível) | O estado do bucket `EXPORT_BUCKET` e as permissões do worker |
| O SES recusa o envio (remetente `MAIL_FROM` não verificado, cota esgotada) | O estado do SES na conta |
| `EXPORT_KEY` ausente ou inválida | A variável no deploy do worker. O Fernet exige uma chave de 32 bytes em base64 |
| O payload tem um formato que o worker não trata | O conteúdo das mensagens em `exports.dead` |

TODO: o repositório não traz os comandos nem os painéis para verificar S3, SES e variáveis do deploy, nem o local dos logs e do painel do RabbitMQ. Preencha com os links e comandos da sua infraestrutura.

Se a causa estiver fora do seu alcance, vá direto para "Quando escalar".

## 3. Corrija a causa

Corrija o que o passo 2 apontou (permissão, chave, remetente, indisponibilidade). Se a correção exigir mudança de código ou de variável de ambiente, o deploy aplica a mudança. TODO: o repositório não descreve o processo de deploy.

Depois da correção, espere uma exportação nova terminar. TODO: o repositório não traz um comando para disparar uma exportação de teste. Se a fila `exports.dead` parar de crescer, a causa foi resolvida.

## 4. Recoloque as mensagens na fila `exports`

Execute o requeue em lotes pequenos para ver se as mensagens voltam a falhar. O script move as mensagens de `exports.dead` para `exports`:

```bash
uv run python scripts/requeue_dead.py --limit 10
```

A saída esperada:

```text
moved 10 message(s)
```

Espere alguns minutos e confira se `exports.dead` não recebeu essas mensagens de volta (repita o comando do passo 1). Se as mensagens voltaram, a causa continua ativa: volte ao passo 2.

Se o lote funcionou, recoloque o restante. O limite padrão do script é 100 mensagens por execução, então repita o comando ou aumente `--limit`:

```bash
uv run python scripts/requeue_dead.py --limit 500
```

Um requeue republica o corpo da mensagem sem o cabeçalho `x-attempts`. O worker conta, então, as três tentativas desde o início.

**Atenção:** o worker grava o arquivo no S3 antes de enviar o e-mail. Se uma tentativa falhou no e-mail, o arquivo dela já está no bucket, e cada nova tentativa grava outro arquivo com outra chave. O bucket acumula arquivos que nenhum e-mail referencia. Como o e-mail é a última etapa, o cliente não recebe e-mail duplicado.

## Como desfazer

O requeue não tem comando de desfazer. Uma mensagem recolocada que falha de novo volta sozinha para `exports.dead` depois de três tentativas. Por isso, o passo 4 começa com um lote de 10.

## Quando escalar

Escale quando uma destas situações acontecer:

- Você não achou a causa no passo 2.
- As mensagens voltaram para `exports.dead` depois do requeue.
- A causa está em um serviço que você não administra (S3, SES, RabbitMQ).

TODO: o repositório não diz quem é o dono do `exporter`, qual é o canal de escalonamento nem como acionar a pessoa responsável. Preencha com o nome da equipe, o canal e o contato de segunda linha.

## Depois do incidente

Registre a causa. Como o worker não loga o erro, a próxima pessoa de plantão ficará às cegas de novo. Abra uma tarefa para o worker registrar a exceção em `exporter/worker.py`, no bloco `except Exception`.
