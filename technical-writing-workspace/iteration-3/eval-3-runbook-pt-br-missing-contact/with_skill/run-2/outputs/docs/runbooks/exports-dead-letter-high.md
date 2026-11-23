# Runbook: ExportsDeadLetterHigh

Use este runbook quando o alerta `ExportsDeadLetterHigh` chegar ao seu pager. Ele diz como confirmar o alerta, descobrir por que os exports falharam, reenfileirar as mensagens e escalar se o problema continuar. Ele não explica o pipeline inteiro: para isso, leia [`docs/pipeline.md`](../pipeline.md) (em inglês).

## O alerta

- **Nome:** `ExportsDeadLetterHigh`, severidade `page` (definido em `deploy/alerts.yaml`).
- **Resumo no pager:** "More than 10 exports failed three times".
- **Condição:** `rabbitmq_queue_messages{queue="exports.dead"} > 10` por 5 minutos seguidos.

## Impacto

Cada mensagem em `exports.dead` é um export que o worker tentou 3 vezes e não conseguiu entregar. O cliente que pediu esse export não recebe o e-mail com o link de download, e o código não avisa o cliente da falha. O cliente só descobre quando abre um chamado.

A fila não cresce sozinha depois que a causa some: o worker não reprocessa mensagens de `exports.dead`. Quem as move de volta é você, com o script do passo 5.

- **Urgência:** TODO: definir o prazo de resposta esperado (SLA) para este alerta. O repositório não o registra.

## Antes de começar

- Acesso ao ambiente onde o worker roda, com a variável `QUEUE_URL` apontando para o RabbitMQ.
- O repositório `exporter` clonado e `make setup` executado (instala as dependências com `uv sync`).
- TODO: informar em qual ambiente (produção, staging) e em qual host ou cluster o alerta dispara e onde você roda os comandos. O repositório não diz.

## 1. Confirmar que o alerta é real

Conte as mensagens em `exports.dead` sem mover nenhuma:

```bash
uv run python scripts/requeue_dead.py --dry-run
```

Saída esperada, com N maior que 10:

```
would move N message(s)
```

O script lê no máximo 100 mensagens (`--limit` tem padrão 100), então a contagem para em 100 mesmo que a fila tenha mais.

Se N for 10 ou menos, o alerta já está resolvendo. Acompanhe por 10 minutos e, se ele não voltar, feche o incidente.

## 2. Descobrir a causa

O worker captura toda exceção em `exporter/worker.py` e republica a mensagem sem registrar o erro. O código não grava a causa em nenhum log. Por isso a causa vem de fora do worker: verifique, nesta ordem, as quatro dependências que o worker usa a cada export.

| Dependência | O que o worker faz com ela | Variável de ambiente |
|---|---|---|
| Chave de criptografia | Cifra o CSV com Fernet | `EXPORT_KEY` |
| Bucket S3 | Grava o CSV cifrado com `put_object` | `EXPORT_BUCKET` |
| S3 (link) | Gera o link de download, que vale 24 horas | `EXPORT_BUCKET` |
| SES | Envia o e-mail com o link | `MAIL_FROM` |

Pergunte, para cada uma: houve mudança, queda ou expiração de credencial nas últimas horas? Compare o horário da mudança com o horário em que o alerta começou.

- TODO: informar onde ficam os logs do worker e os painéis da AWS (S3, SES) e do RabbitMQ. O repositório não os cita.
- TODO: informar como inspecionar o conteúdo de uma mensagem em `exports.dead`. O repositório não traz um script para isso, e `requeue_dead.py --dry-run` só conta.

Se todas as mensagens falharam depois de um deploy, a causa provável é o deploy. Essa é uma hipótese a confirmar, não um fato que o código garante.

## 3. Corrigir a causa

Corrija a dependência que falhou (restaure a credencial, a chave, o acesso ao bucket ou a configuração do SES) antes de reenfileirar. Se você reenfileirar com a causa ainda ativa, o worker falha as mensagens de novo e elas voltam para `exports.dead`.

- TODO: informar quem corrige cada dependência e como (por exemplo, quem rotaciona credenciais AWS). O repositório não diz.

## 4. Verificar que o worker processa de novo

Depois da correção, confirme que um export novo termina. TODO: informar como disparar um export de teste e onde ver o resultado. O endpoint é `POST /exports` no gateway, e o payload exige `account_id` (o código não aceita mais de 100000 linhas em `rows`).

## 5. Reenfileirar as mensagens

Reenfileirar move mensagens de `exports.dead` para `exports`, e o worker as processa de novo. O script não preserva o contador `x-attempts`: cada mensagem reenfileirada ganha mais 3 tentativas. Mensagens que falharem de novo voltam para `exports.dead` depois dessas 3 tentativas.

Comece com um lote pequeno:

```bash
uv run python scripts/requeue_dead.py --limit 5
```

Saída esperada:

```
moved 5 message(s)
```

Espere cerca de 1 minuto e confira que `exports.dead` não recebeu mensagens novas, executando de novo o passo 1. Se a contagem não subiu, reenfileire o resto, em lotes de até 100:

```bash
uv run python scripts/requeue_dead.py --limit 100
```

Repita até o script imprimir `moved 0 message(s)`.

## 6. Desfazer

Reenfileirar não tem comando de desfazer. Se as mensagens falharem de novo, elas voltam sozinhas para `exports.dead` depois de 3 tentativas, e você retoma do passo 2. Não apague mensagens de `exports.dead`: cada uma é um export que um cliente ainda espera.

## 7. Quando escalar

Escale se uma destas situações acontecer:

- Você não identifica a causa em 30 minutos. (Esse prazo é uma sugestão: TODO: confirmar com o time.)
- Você reenfileirou as mensagens e `exports.dead` voltou a passar de 10.
- O alerta dispara de novo em menos de 1 hora depois de fechado.

Contatos:

- **Pessoa ou time responsável pelo `exporter`:** TODO: informar nome ou rotação de plantão.
- **Canal de incidentes:** TODO: informar o canal.
- **Como acionar o plantão da plataforma (RabbitMQ, AWS):** TODO: informar.

## Depois do incidente

Registre a causa e o número de exports reenfileirados. Se o worker continuar sem registrar a causa das falhas, proponha ao time que `exporter/worker.py` grave a exceção antes de republicar a mensagem: hoje a investigação do passo 2 depende disso.
