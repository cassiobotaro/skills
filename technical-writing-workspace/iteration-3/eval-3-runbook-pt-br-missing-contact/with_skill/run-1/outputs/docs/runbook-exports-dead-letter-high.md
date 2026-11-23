# Runbook: `ExportsDeadLetterHigh`

Este runbook é para quem está de plantão quando o alerta `ExportsDeadLetterHigh` dispara. Ele diz como confirmar o problema, como reduzir o impacto e quando chamar ajuda. Ele não explica o pipeline inteiro: para isso, leia [`docs/pipeline.md`](pipeline.md).

## O alerta

- **Nome:** `ExportsDeadLetterHigh`, severidade `page` (definido em `deploy/alerts.yaml`).
- **Resumo no pager:** "More than 10 exports failed three times".
- **Condição:** `rabbitmq_queue_messages{queue="exports.dead"} > 10`, durante 5 minutos seguidos.

A fila `exports.dead` guarda os pedidos de exportação que o worker (`exporter/worker.py`) tentou processar três vezes sem sucesso. O alerta dispara quando passam de 10 pedidos nessa fila.

## Impacto

Cada mensagem em `exports.dead` é um cliente que pediu uma exportação e não recebeu o e-mail com o link de download. O gateway já respondeu `202` a esse cliente, então ele espera o arquivo e não sabe que o pedido falhou. O alerta não indica que a API está fora: o gateway continua aceitando pedidos.

TODO: definir a urgência real (SLA da exportação, horário comercial ou 24x7). Nada no repositório diz isso.

## Antes de começar

- Você precisa da variável `QUEUE_URL` (a URL do RabbitMQ) no seu terminal e do `uv` instalado. O `Makefile` roda `uv sync` no alvo `setup`.
- Rode os comandos a partir da raiz do repositório.

TODO: dizer onde o plantão consegue o `QUEUE_URL` de produção e onde o repositório deve estar clonado (host, bastion, pod).

## 1. Confirme o alerta

1. Conte as mensagens em `exports.dead` sem mover nenhuma:

   ```bash
   uv run python scripts/requeue_dead.py --dry-run --limit 1000
   ```

   Saída esperada, com o alerta ativo:

   ```text
   would move 11 message(s)
   ```

   Um número acima de 10 confirma o alerta. O comando devolve cada mensagem à fila, então não altera nada. Sem `--limit`, ele conta no máximo 100 mensagens.

2. Se o número for 10 ou menos, o alerta já se resolveu ou o painel está atrasado. Espere 5 minutos e rode o comando de novo antes de encerrar o chamado.

TODO: link do painel do RabbitMQ/Prometheus onde o plantão vê `rabbitmq_queue_messages{queue="exports.dead"}` ao longo do tempo.

## 2. Descubra a causa antes de reenfileirar

Reenfileirar sem corrigir a causa só devolve as mensagens à `exports.dead`: o worker tenta cada uma mais três vezes e falha de novo.

O worker captura qualquer exceção e republica a mensagem **sem registrar o erro** (`except Exception` em `exporter/worker.py`). Por isso, o log do worker não mostra a causa, e a mensagem na fila também não a guarda. Em uma tentativa, o worker executa estes passos em ordem, e qualquer um deles pode ser o que falha:

1. Gera o CSV a partir do pedido (`build_csv`).
2. Criptografa o CSV com a chave da variável `EXPORT_KEY`.
3. Grava o arquivo no bucket definido em `EXPORT_BUCKET` (S3, `put_object`).
4. Envia o e-mail com o link, pelo SES, usando `MAIL_FROM` (`exporter/notifier.py`).

Use esta ordem para investigar:

1. Verifique se o worker está rodando e se consome a fila `exports`. Um worker parado deixa a fila `exports` crescer, mas não enche `exports.dead` sozinho.
2. Verifique as quatro dependências do worker: `EXPORT_KEY` definida e válida, acesso de escrita ao bucket `EXPORT_BUCKET`, e permissão do SES para enviar de `MAIL_FROM`. Uma falha comum a todas as mensagens (todas as mensagens falham da mesma forma) aponta para uma dessas configurações ou para uma queda do S3 ou do SES.
3. Se só alguns pedidos falham, o problema está no conteúdo desses pedidos.

TODO: onde o plantão lê os logs e as métricas do worker, e como inspecionar o corpo de uma mensagem em `exports.dead` (console do RabbitMQ ou outro). Nada no repositório descreve isso.

TODO: como o worker é executado em produção (serviço, container, cluster) e como reiniciá-lo. O repositório só traz `make run-worker` para uso local.

## 3. Reenfileire as mensagens

Faça isso só depois de corrigir a causa. Enquanto a causa existir, pare aqui e escale (seção 4).

> **Atenção: possível e-mail duplicado.** Se a falha ocorreu no envio do e-mail (passo 4 do worker), o arquivo já está no bucket. O worker grava um arquivo novo a cada tentativa e envia outro e-mail ao reprocessar, então o cliente pode receber mais de um e-mail.

1. Reenfileire um lote pequeno para testar:

   ```bash
   uv run python scripts/requeue_dead.py --limit 5
   ```

   Saída esperada:

   ```text
   moved 5 message(s)
   ```

2. Espere o worker processar o lote e confirme que `exports.dead` não voltou a crescer (repita o comando `--dry-run` da seção 1). Se as 5 mensagens voltaram à fila, a causa continua ativa: pare e escale.
3. Reenfileire o restante em lotes:

   ```bash
   uv run python scripts/requeue_dead.py --limit 50
   ```

   Repita até o comando imprimir `moved 0 message(s)`.

O script publica cada mensagem em `exports` sem o cabeçalho `x-attempts`, então o worker conta as tentativas do zero: cada mensagem ganha mais três tentativas.

## Como desfazer

O script não tem comando de desfazer. Uma mensagem reenfileirada que falha de novo volta sozinha a `exports.dead` depois de três tentativas. Não há outra forma de recolocar uma mensagem em `exports.dead`.

## 4. Escale

Escale quando:

- o `--dry-run` ainda mostra mensagens depois de você corrigir a causa e reenfileirar um lote de teste;
- você não consegue identificar a causa na seção 2;
- o número de mensagens em `exports.dead` continua crescendo.

TODO: nome do time dono do serviço `exporter`, política de escalonamento (quem acionar primeiro, quem em seguida) e canal de comunicação (Slack, telefone, ferramenta de plantão). O repositório não traz nenhum desses dados, e este runbook não os inventa.

## Depois do incidente

Reenfileirar resolve as mensagens atuais, mas não registra a causa. Anote a causa e a correção no canal do incidente. Como o worker não registra o erro, quem investigou é a única fonte dessa informação.
