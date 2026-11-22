# Runbook: ExportsDeadLetterHigh

Use este runbook quando o alerta `ExportsDeadLetterHigh` disparar. Ele diz como confirmar o alerta, como recolocar na fila as exportações que falharam e quando chamar outra pessoa. Quem lê é o engenheiro de plantão, que pode não conhecer o serviço `exporter`.

## O alerta

O Prometheus dispara `ExportsDeadLetterHigh` (severidade `page`) quando a métrica `rabbitmq_queue_messages{queue="exports.dead"}` fica acima de 10 por 5 minutos. A mensagem do alerta é "More than 10 exports failed three times". A regra está em `deploy/alerts.yaml`.

A fila `exports.dead` guarda os pedidos de exportação que o worker tentou três vezes sem sucesso. O worker (`exporter/worker.py`) gera o CSV, criptografa, envia para o bucket e manda o link por e-mail. Se qualquer um desses passos lançar uma exceção, o worker recoloca o pedido na fila `exports`. Na terceira falha, ele o envia para `exports.dead`.

## Impacto

Cada mensagem em `exports.dead` é um cliente que pediu uma exportação e não recebeu o e-mail com o link. O gateway já respondeu `202` a esse cliente, e nada avisa que o pedido falhou. As mensagens ficam na fila até alguém as mover, então a espera não as perde. Quanto mais tempo o alerta fica aberto, mais clientes esperam por um e-mail que não chega.

## Antes de começar

- Defina `QUEUE_URL` no seu terminal com a URL do RabbitMQ. O script `scripts/requeue_dead.py` lê essa variável.
- Rode os comandos na raiz do repositório, depois de `make setup`.

<!-- TODO: dizer de onde o plantão pega o valor de QUEUE_URL (cofre de segredos, variável do cluster etc.). O repositório não diz. -->

## 1. Confirme o alerta

Conte as mensagens na fila sem mover nenhuma:

```bash
uv run python scripts/requeue_dead.py --dry-run --limit 1000
```

Você deve ver `would move <N> message(s)`. Se `<N>` for 10 ou menos, o alerta já se resolveu ou alguém esvaziou a fila. Confira o estado do alerta e encerre. Se `<N>` for maior que 10, siga para o passo 2.

O `--dry-run` lê cada mensagem e a devolve à fila, então ele não muda nada. Ele conta no máximo o valor de `--limit` (o padrão é 100).

## 2. Descubra a causa

Recolocar as mensagens na fila antes de achar a causa só as faz falhar de novo. Procure primeiro o motivo da falha.

O worker captura qualquer exceção e não escreve nada em log. Ele também não grava o erro na mensagem. Por isso o repositório não traz um jeito de ler a causa de uma falha já ocorrida. Procure nos logs do worker e nos serviços de que ele depende.

<!-- TODO: dizer onde ficam os logs do worker (comando ou painel) e onde está o painel do RabbitMQ. O repositório não diz. -->

O código do worker chama quatro dependências, e uma falha em qualquer uma delas leva o pedido à fila de falhas. Verifique cada uma:

| Dependência | Variável de ambiente do worker | O que verificar |
|---|---|---|
| Criptografia (`Fernet`) | `EXPORT_KEY` | A variável existe e é uma chave Fernet válida. |
| Bucket S3 | `EXPORT_BUCKET` | A variável existe, o bucket existe e o worker tem permissão de escrita. |
| Geração do link e envio de e-mail (SES) | `MAIL_FROM` | A variável existe e o SES aceita o remetente. |
| RabbitMQ | `QUEUE_URL` | O worker alcança o broker. |

Essa lista vem da leitura do código. Ela mostra onde uma falha pode nascer, e não qual falha está acontecendo agora.

Um pedido com mais de 100.000 linhas não chega a `exports.dead`: o gateway o rejeita com `413` antes de enfileirar.

## 3. Corrija a causa

Corrija a dependência que você achou no passo 2. Se a correção for uma variável de ambiente, reinicie o worker para ele ler o novo valor.

<!-- TODO: dizer como o plantão reinicia o worker em produção. O repositório só traz `make run-worker`, que roda o worker em desenvolvimento. -->

Se você não achar a causa, ou se ela estiver fora do seu alcance, vá para "Quando chamar outra pessoa".

## 4. Recoloque as mensagens na fila `exports`

Faça isso só depois de corrigir a causa. Se a causa continuar, cada mensagem recolocada passa por mais três tentativas e volta para `exports.dead`.

> **Atenção.** O script publica a mensagem de volta em `exports` sem o contador de tentativas. Cada mensagem recolocada ganha três tentativas novas. O script não desfaz essa operação: para parar, desligue o worker.

1. Comece com um lote pequeno:

   ```bash
   uv run python scripts/requeue_dead.py --limit 5
   ```

   Você deve ver `moved 5 message(s)`.

2. Espere cerca de um minuto e rode a contagem do passo 1. O número deve ter caído em 5. Se ele subiu de novo, a causa continua. Volte ao passo 2.

3. Se o número caiu e nenhuma mensagem voltou, mova o resto:

   ```bash
   uv run python scripts/requeue_dead.py --limit 100
   ```

   Repita o comando até a contagem chegar a zero. Cada execução move no máximo 100 mensagens.

4. Confirme que o alerta resolveu no Prometheus. Ele resolve quando a métrica fica em 10 ou menos.

## Quando chamar outra pessoa

Chame a equipe dona do `exporter` se:

- você não achou a causa no passo 2;
- a causa está fora do worker (S3, SES ou RabbitMQ) e você não tem acesso para corrigi-la;
- as mensagens voltam para `exports.dead` depois do passo 4.

<!-- TODO: dizer quem é a equipe dona do `exporter`, o canal ou a escala de plantão para chamá-la e o tempo máximo antes de escalar. O repositório não traz nenhum contato. -->

## Depois do incidente

Anote quantas exportações falharam e qual foi a causa. Se o worker continuar sem registrar o erro, a próxima pessoa de plantão enfrentará o mesmo escuro: considere pedir à equipe que registre a exceção em `exporter/worker.py`.
