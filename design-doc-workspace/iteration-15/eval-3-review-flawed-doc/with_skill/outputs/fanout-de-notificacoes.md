# Fanout de notificações

| | |
|---|---|
| **Estado** | Em revisão |
| **Autor** | Time de Mensageria |
| **Criado em** | 2026-01-28 |
| **Última atualização** | 2026-08-07 |

## Glossário

- **CDC** (*change data capture*) — captura das alterações gravadas numa base de dados e sua publicação como eventos para outros componentes consumirem.
- **DLQ** (*dead letter queue*) — fila para onde a mensagem é desviada quando o consumo falha, para inspeção ou reprocessamento posterior.
- **Exchange** — ponto onde o dispatcher publica os eventos e a partir do qual eles são distribuídos para as filas.
- **Fanout** — publicação de um mesmo evento para várias filas, consumidas em paralelo.
- **In-app** — canal de notificação exibido dentro do próprio produto.
- **Provider** — serviço externo responsável pela entrega final da notificação de um canal.
- **SLA** (*service level agreement*) — nível de serviço acordado; aqui, o prazo de entrega das notificações.
- **TPS** (*transactions per second*) — taxa de requisições por segundo enviadas a um provider.

## Visão geral

O envio de notificações acontece hoje de forma sequencial dentro do serviço de mensageria e, com o crescimento da base, começou a apresentar lentidão. Este documento propõe substituir esse processamento por um fanout baseado em filas, em que um worker por canal consome e envia em paralelo.

## Escopo e contexto

Hoje o serviço de mensageria processa os envios dentro do próprio serviço: um cron roda a cada minuto, lê a tabela `notifications`, monta o payload de cada canal (push, e-mail e in-app) e chama os providers um a um. Com o crescimento da base, esse modelo começou a apresentar lentidão.

## Objetivos

- Melhorar a performance dos envios
- Tornar o sistema escalável
- Garantir o SLA

## Fora de escopo

- O sistema não deve ser lento
- O sistema não deve perder notificações

## Solução

Adotaremos o fanout com filas por canal:

![Diagrama de contêineres — fanout de notificações](diagrams/fanout-de-notificacoes.svg)

*Imagem a gerar a partir do DSL abaixo na passada manual.*

<details>
<summary>Fonte do diagrama (Structurizr DSL)</summary>

```
workspace {

    !identifiers hierarchical

    model {
        notificacoes = softwareSystem "Serviço de notificações" {
            cdc = container "CDC" "Captura os eventos de domínio"
            dispatcher = container "Dispatcher" "Publica os eventos na exchange"
            exchange = container "Exchange" "Distribui cada evento para as filas de canal"

            filaPush = container "Fila push" "Enfileira os eventos do canal push" "" "Queue"
            filaEmail = container "Fila e-mail" "Enfileira os eventos do canal e-mail" "" "Queue"
            filaInApp = container "Fila in-app" "Enfileira os eventos do canal in-app" "" "Queue"

            workerPush = container "Worker push" "Consome a fila de push e envia as notificações do canal"
            workerEmail = container "Worker e-mail" "Consome a fila de e-mail e envia as notificações do canal"
            workerInApp = container "Worker in-app" "Consome a fila de in-app e envia as notificações do canal"

            dlqPush = container "DLQ push" "Recebe as mensagens de push que o worker não conseguiu processar" "" "Queue"
            dlqEmail = container "DLQ e-mail" "Recebe as mensagens de e-mail que o worker não conseguiu processar" "" "Queue"

            cdc -> dispatcher "Entrega os eventos de domínio a"
            dispatcher -> exchange "Publica os eventos de notificação em"

            exchange -> filaPush "Encaminha os eventos do canal push para"
            exchange -> filaEmail "Encaminha os eventos do canal e-mail para"
            exchange -> filaInApp "Encaminha os eventos do canal in-app para"

            filaPush -> workerPush "É consumida por"
            filaEmail -> workerEmail "É consumida por"
            filaInApp -> workerInApp "É consumida por"

            workerPush -> dlqPush "Desvia as mensagens que falharam para"
            workerEmail -> dlqEmail "Desvia as mensagens que falharam para"
        }
    }

    views {
        container notificacoes "Containers" {
            include *
            autoLayout lr
        }

        styles {
            element "Queue" {
                shape Pipe
            }
        }
    }
}
```

</details>

O CDC lê os eventos de domínio e os entrega ao dispatcher, que publica cada evento na exchange. A exchange encaminha o evento para uma fila por canal — push, e-mail e in-app — e cada canal tem o seu próprio worker, que consome a sua fila em paralelo com os demais e envia a notificação ao provider do canal, respeitando um controle de TPS por provider. As mensagens que um worker não consegue processar são desviadas para a DLQ daquele canal.

## Plano

1. Criar exchange e filas
2. Migrar o canal de e-mail
3. Migrar push e in-app
4. Desligar o cron
