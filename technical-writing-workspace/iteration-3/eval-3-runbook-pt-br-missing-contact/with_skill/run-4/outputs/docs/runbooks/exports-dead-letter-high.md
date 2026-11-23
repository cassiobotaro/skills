# Runbook: ExportsDeadLetterHigh

Este runbook diz o que fazer quando o alerta `ExportsDeadLetterHigh` dispara: mais de 10 exports falharam três vezes e estão parados na fila `exports.dead`. Quem está de plantão lê este documento. Ele cobre confirmar o alerta, achar a causa e reenfileirar os exports. Ele não cobre o fluxo normal do pipeline (veja `docs/pipeline.md`).

## O alerta

- **Nome:** `ExportsDeadLetterHigh`, severidade `page`.
- **Condição** (`deploy/alerts.yaml`): `rabbitmq_queue_messages{queue="exports.dead"} > 10` por 5 minutos.
- **Resumo no pager:** "More than 10 exports failed three times".

## Impacto

Cada mensagem em `exports.dead` é um export que o worker tentou três vezes e não concluiu. O cliente dono do export não recebe o e-mail com o link de download. O worker não tenta de novo sozinho: as mensagens ficam na fila até alguém reenfileirá-las.

TODO: a urgência (prazo para o cliente receber o export, contrato, clientes críticos) não está no repositório. Preencher com quem é dono do serviço.

## Como o export chega a `exports.dead`

O worker (`exporter/worker.py`) executa quatro passos para cada job: gera o CSV, criptografa com a chave `EXPORT_KEY`, grava o arquivo no bucket `EXPORT_BUCKET` e chama `notify`, que gera o link e envia o e-mail pelo SES. Qualquer exceção em um desses passos conta como uma falha. Na terceira falha, o worker publica a mensagem em `exports.dead`.

O worker não registra a exceção em log nem guarda o motivo da falha na mensagem. A causa precisa ser achada fora da fila (passo 3).

## Passos

### 1. Confirme o alerta

Rode a consulta no Prometheus:

```
rabbitmq_queue_messages{queue="exports.dead"}
```

Você deve ver um valor acima de 10. Rode também `rabbitmq_queue_messages{queue="exports"}` e compare os dois valores com os de 10 minutos atrás:

- `exports.dead` cresce, ou `exports` cresce: a falha continua. Siga para o passo 2 e não reenfileire nada antes de corrigir a causa.
- `exports.dead` está estável e `exports` está perto de zero: a falha parou. Siga para o passo 2 para achar a causa e depois para o passo 4.

### 2. Verifique se o worker está rodando

Se nenhum worker consome `exports`, a fila `exports` cresce sem passar por `exports.dead`. Isso é outro problema. O worker sobe com `make run-worker` (`uv run python -m exporter.worker`).

TODO: como o worker roda em produção (serviço, contêiner, orquestrador), como ver o estado dele e como reiniciá-lo. O repositório não diz.

### 3. Ache a causa

TODO: onde ficam os logs do worker e o comando para lê-los. O repositório não diz. Sem log de exceção no código (veja acima), procure no log do worker os erros do `boto3` e do `cryptography` no horário em que o alerta começou.

Teste as dependências que o worker usa, uma por vez. Cada item é uma causa possível, tirada do código, não uma causa confirmada:

| Dependência | Variável | Sintoma a procurar |
|---|---|---|
| Chave de criptografia | `EXPORT_KEY` | Erro do `Fernet` ao criptografar: chave ausente ou inválida depois de um deploy ou rotação |
| Bucket S3 | `EXPORT_BUCKET` | Erro do `boto3` em `put_object`: bucket inexistente, permissão negada, credencial expirada |
| Link de download | `EXPORT_BUCKET` | Erro do `boto3` em `generate_presigned_url` |
| E-mail | `MAIL_FROM` | Erro do SES em `send_email`: remetente não verificado, cota de envio atingida |
| Dados do job | `account_id`, `rows` | Falha só em alguns jobs: payload com campo faltando |

Se a falha atinge todos os jobs, a causa é uma dependência ou uma variável de ambiente. Se atinge poucos, a causa está no payload desses jobs. Deploy recente é o primeiro suspeito: confira o que mudou nas variáveis acima.

### 4. Corrija a causa

Corrija a dependência que o passo 3 apontou (restaure a variável, a permissão ou a cota). Depois confirme que `exports` volta a ser consumida sem novas mensagens em `exports.dead`: o valor de `rabbitmq_queue_messages{queue="exports.dead"}` deve parar de crescer.

Se a causa está no payload de alguns jobs, esses jobs vão falhar de novo depois do reenfileiramento. Não os reenfileire; escale (seção abaixo).

### 5. Reenfileire os exports

> **Atenção:** `scripts/requeue_dead.py` move mensagens de `exports.dead` para `exports` e apaga o original em `exports.dead`. O script publica a mensagem sem o cabeçalho `x-attempts`, então cada mensagem ganha mais três tentativas. Reenfileire só depois de corrigir a causa, senão as mensagens voltam para `exports.dead` e o alerta dispara de novo.

1. Defina `QUEUE_URL` com a URL do broker de produção.

   TODO: de onde o plantonista pega essa URL. O repositório não diz.

2. Conte as mensagens sem mover nenhuma:

   ```
   uv run python scripts/requeue_dead.py --dry-run
   ```

   O script imprime `would move <N> message(s)`. O `--dry-run` devolve cada mensagem para a fila com `nack`. Nós não rodamos o script: o valor de `<N>` pode contar a mesma mensagem mais de uma vez, então confirme o total real em `rabbitmq_queue_messages{queue="exports.dead"}`.

3. Mova um lote pequeno primeiro:

   ```
   uv run python scripts/requeue_dead.py --limit 10
   ```

   O script imprime `moved 10 message(s)`. Espere alguns minutos e confirme que essas mensagens não voltaram para `exports.dead`.

4. Mova o resto, em lotes. O padrão de `--limit` é 100:

   ```
   uv run python scripts/requeue_dead.py --limit 100
   ```

   Repita até `rabbitmq_queue_messages{queue="exports.dead"}` chegar a 0.

### Como desfazer

O reenfileiramento não tem comando de desfazer. Se a causa não estava corrigida, o worker tenta cada mensagem três vezes e a devolve a `exports.dead` sozinho. Se isso acontecer, pare de reenfileirar e volte ao passo 3.

## Quando escalar

Escale se uma destas situações ocorrer:

- A causa não está nas dependências do passo 3.
- Mensagens reenfileiradas voltam para `exports.dead`.
- O problema exige mudar código ou infraestrutura que você não controla.

TODO: para quem escalar, por qual canal e como contatar (time dono do serviço, pessoa ou rotação de segundo nível, canal de incidente). O repositório não traz nenhum contato; não invente um.

## Depois do incidente

TODO: onde registrar o incidente. Registre também o que o passo 3 encontrou: o worker não guarda a causa, e o próximo plantonista precisa dela.
