# Serviço de entrega de webhooks

| | |
|---|---|
| **Documento** | DESIGN-DOC |
| **Estado** | Rascunho |
| **Título** | Serviço central de entrega de webhooks |
| **Autores** | Time de Plataforma |
| **Revisores** | SRE (infraestrutura e operação), Segurança (HMAC e segredos) |
| **Criado em** | 2026-06-20 |
| **Atualizado em** | 2026-06-20 |
| **Tags** | webhooks, plataforma, entrega-assíncrona, retry |

## Glossário

| Termo | Definição |
|---|---|
| **Webhook** | Notificação HTTP que avisa um cliente externo sobre um evento ocorrido em nossos sistemas. |
| **HMAC** | *Hash-based Message Authentication Code* — assinatura criptográfica do payload que permite ao cliente verificar a autenticidade e a integridade da mensagem. |
| **Backoff exponencial** | Estratégia de retry em que o intervalo entre tentativas cresce a cada nova falha. |
| **DLQ** | *Dead Letter Queue* — fila para onde vai um evento que esgotou todas as tentativas de entrega. |
| **Assinatura (subscription)** | Configuração de um cliente: o endpoint de destino e o segredo usado para assinar os payloads. |
| **AMQP** | *Advanced Message Queuing Protocol* — protocolo de mensageria usado pelo RabbitMQ. |
| **SRE** | *Site Reliability Engineering* — time responsável por operar e manter a confiabilidade dos serviços. |
| **POST** | Método HTTP usado para enviar o payload do evento ao endpoint do cliente. |
| **SLA** | *Service Level Agreement* — acordo sobre o nível de serviço esperado, aqui em torno do atraso máximo de entrega. |

## Visão geral

Este documento descreve um serviço central de entrega de webhooks que o time de Plataforma vai construir. Hoje cada serviço interno faz o POST direto para o endpoint do cliente, sem retry e sem visibilidade; quando o endpoint do cliente cai, perdemos o evento — o que já ocorreu em produção mais de uma vez. A proposta centraliza a entrega em um serviço que consome eventos de uma fila, faz a entrega assinada com HMAC e, em caso de falha, tenta de novo com backoff exponencial antes de mandar o evento para uma DLQ, registrando todo o histórico para consulta e reenvio manual.

## Escopo e contexto

Hoje a entrega de webhooks é responsabilidade de cada serviço interno individualmente. O fluxo atual é um POST direto, feito de forma inline dentro da request, sem retry e sem registro do que aconteceu. As consequências que motivam este trabalho:

- **Perda de eventos.** Quando o endpoint do cliente está indisponível, o POST falha e o evento é descartado. Já perdemos eventos em produção mais de uma vez por esse motivo.
- **Sem visibilidade.** Não há registro centralizado das entregas, então nem nós nem o cliente conseguem saber o que foi enviado, o que falhou ou o que precisa ser reenviado.
- **Lógica duplicada e inconsistente.** Cada serviço que precisa avisar um cliente externo reimplementa (ou deixa de implementar) a sua própria entrega, gerando comportamento diferente de serviço para serviço.

A infraestrutura que já usamos e na qual a solução se apoia: RabbitMQ para mensageria e PostgreSQL para persistência.

## Objetivos e fora de escopo

### Objetivos

- **Não perder eventos por indisponibilidade do cliente**, retentando a entrega com backoff exponencial por até 5 tentativas antes de enviar o evento para uma DLQ.
- **Dar durabilidade ao evento** publicando-o numa fila do RabbitMQ no momento em que o serviço interno o gera, em vez de depender de um POST inline que some quando falha.
- **Dar visibilidade da entrega** registrando o histórico de cada tentativa no PostgreSQL e expondo-o ao cliente por uma Admin API que também permite o reenvio manual.
- **Centralizar a lógica de entrega** num único serviço, eliminando a duplicação de retry e assinatura espalhada pelos serviços internos.
- **Garantir a autenticidade do payload** assinando cada entrega com HMAC usando um segredo por cliente.

### Fora de escopo

- **Migração dos clientes existentes** para verificarem a assinatura HMAC — depende de coordenação com cada cliente e é tratada separadamente.
- **Transformação ou roteamento por conteúdo do evento** — o serviço entrega o payload publicado pelo serviço interno como está; não há regras de transformação.
- **Garantia de ordenação entre eventos** de uma mesma assinatura — o retry com backoff pode reordenar entregas, e este documento não promete *ordering*.
- **Interface gráfica** para o cliente — a visibilidade é exposta pela Admin API; um portal web fica para outro momento.

## A solução

O coração da solução é desacoplar a geração do evento da sua entrega. Em vez de o serviço interno fazer o POST inline, ele publica o evento numa fila do RabbitMQ e segue seu fluxo. A partir daí, o serviço de webhooks assume a entrega de forma assíncrona, durável e observável.

O serviço tem dois processos em Go:

- **Dispatcher** — consome a fila de eventos, busca no PostgreSQL a configuração da assinatura do cliente (endpoint e segredo), assina o payload com HMAC e faz o POST para o endpoint do cliente. Cada tentativa, com sucesso ou falha, é gravada no histórico. Quando a entrega falha, o evento vai para uma fila de retry com backoff exponencial; depois de 5 tentativas sem sucesso, vai para a DLQ.
- **Admin API** — expõe ao cliente o histórico de entregas e permite o reenvio manual de um evento (que reenfileira o evento para o dispatcher).

O PostgreSQL guarda duas coisas: a configuração das assinaturas (endpoint e segredo de cada cliente) e o histórico de entregas (cada tentativa, com status e timestamp).

A principal troca da solução está aqui: a entrega deixa de ser inline na request e passa a ser **assíncrona**. O cliente pode ver o evento com alguns segundos de atraso. Em troca, ganhamos retry, durabilidade e visibilidade — exatamente o que falta hoje.

### Arquitetura

![Diagrama de containers — Serviço de entrega de webhooks](diagrams/architecture.svg)

<details>
<summary>Fonte do diagrama (Structurizr DSL)</summary>

```
workspace "Serviço de Webhooks" "Entrega central de webhooks com retry, durabilidade e visibilidade" {

    model {
        servicoInterno = softwareSystem "Serviço interno" "Qualquer serviço da plataforma que precisa avisar um cliente externo sobre um evento." "Externo"
        cliente = softwareSystem "Endpoint do cliente" "Endpoint HTTP do cliente externo que recebe os webhooks." "Externo"

        webhooks = softwareSystem "Serviço de Webhooks" "Entrega webhooks de forma assíncrona, com retry, durabilidade e histórico." {
            fila = container "Fila de eventos" "Recebe os eventos publicados pelos serviços internos, além das filas de retry e DLQ." "RabbitMQ" "Fila"
            dispatcher = container "Dispatcher" "Consome a fila, busca a assinatura, assina o payload com HMAC e faz o POST para o cliente; em falha, reenfileira com backoff." "Go"
            adminApi = container "Admin API" "Permite ao cliente consultar o histórico de entregas e reenviar eventos manualmente." "Go"
            banco = container "Banco de dados" "Guarda a configuração das assinaturas dos clientes e o histórico de entregas." "PostgreSQL" "Banco de dados"
        }

        servicoInterno -> fila "Publica evento" "AMQP"
        dispatcher -> fila "Consome eventos e reenfileira em retry/DLQ" "AMQP"
        dispatcher -> banco "Lê a configuração da assinatura e grava o resultado da entrega" "SQL"
        dispatcher -> cliente "Entrega o webhook assinado com HMAC" "HTTPS POST"
        cliente -> adminApi "Consulta histórico e solicita reenvio" "HTTPS"
        adminApi -> banco "Lê o histórico de entregas" "SQL"
        adminApi -> fila "Reenfileira evento para reenvio manual" "AMQP"
    }

    views {
        container webhooks "Containers" {
            include *
            autolayout lr
        }

        styles {
            element "Externo" {
                background "#999999"
                color "#ffffff"
            }
            element "Fila" {
                shape Pipe
            }
            element "Banco de dados" {
                shape Cylinder
            }
        }
    }
}
```

</details>

> A imagem `diagrams/architecture.svg` ainda é um placeholder: o exportador/validador não estava disponível neste ambiente, então a imagem renderizada precisa ser gerada na passagem manual a partir do DSL acima (o DSL é a fonte de verdade da arquitetura).

Os componentes do diagrama e como interagem:

- O **Serviço interno** publica o evento na **Fila de eventos** (RabbitMQ) e segue seu fluxo — não espera a entrega.
- O **Dispatcher** (Go) consome a fila, lê no **Banco de dados** (PostgreSQL) a configuração da assinatura do cliente, assina o payload com HMAC e entrega o webhook ao **Endpoint do cliente** via HTTPS POST. Cada tentativa é gravada de volta no banco. Em caso de falha, o dispatcher reenfileira o evento na fila de retry; após 5 tentativas, o evento vai para a DLQ.
- A **Admin API** (Go) atende ao **Endpoint do cliente**: lê o histórico de entregas no banco e, num reenvio manual, reenfileira o evento na fila para o dispatcher processar de novo.

A mesma infraestrutura de fila do RabbitMQ comporta a fila de eventos, as filas de retry e a DLQ; o diagrama as representa como uma única "Fila de eventos" para manter o nível de container.

### Entrega e retry

1. O serviço interno publica o evento na fila.
2. O dispatcher consome o evento, busca a assinatura e tenta o POST assinado.
3. Se o POST tem sucesso, o dispatcher grava a entrega como bem-sucedida no histórico.
4. Se o POST falha, o dispatcher grava a tentativa e reenfileira o evento na fila de retry com backoff exponencial.
5. Os passos 2–4 se repetem até 5 tentativas. Esgotadas as tentativas, o evento vai para a DLQ e o histórico registra o fracasso final.

### Assinatura HMAC

Cada entrega leva uma assinatura HMAC do payload, calculada com o segredo da assinatura do cliente guardado no PostgreSQL. O cliente recalcula a assinatura com o mesmo segredo e a compara com a que recebeu, confirmando que o payload veio de nós e não foi adulterado. A gestão e a rotação desses segredos é um ponto de revisão para o time de Segurança (ver Aspectos transversais).

## Trade-offs da solução escolhida

- ✓ **Eventos deixam de ser perdidos** por indisponibilidade temporária do cliente: o retry com backoff e a DLQ garantem que nenhum evento simplesmente desaparece.
- ✓ **Durabilidade:** o evento é persistido na fila assim que o serviço interno o gera, em vez de viver apenas dentro de uma request que pode falhar.
- ✓ **Visibilidade:** o histórico no PostgreSQL e a Admin API dão ao cliente (e a nós) a capacidade de ver o que foi entregue, o que falhou e de reenviar.
- ✓ **Lógica centralizada:** retry e assinatura passam a existir em um lugar só, com comportamento consistente para todos os serviços internos.
- ✗ **Entrega assíncrona:** a entrega deixa de ser inline; o cliente pode ver o evento com alguns segundos de atraso. Este é o custo que aceitamos conscientemente.
- ✗ **Mais infraestrutura para operar:** uma nova fila e um novo serviço (dois processos) entram no inventário do SRE.
- ✗ **Sem garantia de ordenação:** o retry com backoff pode entregar eventos de uma mesma assinatura fora da ordem de geração.
- ✗ **Nova superfície de segurança:** segredos por cliente passam a ser armazenados e usados, o que o time de Segurança precisa revisar.

## Alternativas consideradas

| Alternativa | Trade-offs | Decisão |
|---|---|---|
| **Serviço central de webhooks** (esta proposta) | ✓ Retry, durabilidade, visibilidade e lógica única; ✗ entrega assíncrona, mais infra para operar | **Escolhida** |
| Cada serviço com sua própria lógica de retry | ✗ Duplica código em cada serviço; ✗ comportamento inconsistente entre serviços; ✓ entrega segue inline | Rejeitada |
| SaaS de webhooks (ex.: Svix) | ✓ Pronto e mantido por terceiros; ✗ custo recorrente; ✗ manda dado sensível para fora do nosso ambiente | Rejeitada |
| Não fazer nada | ✗ Continuamos perdendo eventos em produção, problema que já ocorreu mais de uma vez | Rejeitada |

**Cada serviço com sua própria lógica de retry** foi rejeitada porque duplica código e produz comportamento inconsistente: cada time implementaria (ou esqueceria) retry, backoff e assinatura de um jeito diferente, e o problema de visibilidade continuaria sem dono.

**Um SaaS tipo Svix** foi rejeitado por dois motivos: o custo recorrente e o fato de mandar dado sensível para fora do nosso ambiente, o que não é aceitável para os payloads que entregamos.

**Não fazer nada** não serve porque já estamos perdendo eventos — o problema que motiva este documento é real e recorrente em produção.

## Aspectos transversais

### Segurança

A solução introduz **segredos por cliente** usados na assinatura HMAC e os armazena no PostgreSQL. O time de Segurança precisa revisar como esses segredos são guardados, acessados pelo dispatcher e rotacionados, além de validar o esquema de assinatura HMAC em si (algoritmo, formato do header, proteção contra replay). Por isso Segurança está nomeada como revisora deste documento.

### Infraestrutura e operação (SRE)

A solução adiciona ao inventário do SRE uma nova fila no RabbitMQ (com suas filas de retry e DLQ) e um novo serviço com dois processos em Go (dispatcher e Admin API). O SRE precisa avaliar capacidade da fila, alarmes para a DLQ crescer, e o ciclo de vida operacional desses processos. Por isso SRE está nomeada como revisora.

## Testabilidade e observabilidade

- **Antes de subir:** testes de integração que exercitam o caminho feliz (publica → consome → entrega) e o caminho de falha (cliente indisponível → retry → DLQ), incluindo a verificação da assinatura HMAC com um endpoint de teste.
- **Em produção:** métricas de eventos publicados, entregues, retentados e enviados à DLQ; alarme quando a DLQ cresce (sinal de cliente persistentemente indisponível ou bug de entrega); latência entre publicação e entrega, para acompanhar o atraso que aceitamos na troca por assincronia.

## Questões em aberto

- Qual é o atraso máximo aceitável entre a publicação e a entrega, agora que a entrega é assíncrona? É preciso um SLA com os clientes?
- Os parâmetros do backoff exponencial (intervalo inicial e fator de crescimento até as 5 tentativas) ainda precisam ser definidos.
- Política de retenção do histórico de entregas no PostgreSQL — por quanto tempo guardamos cada tentativa?
- O que acontece com os eventos que chegam à DLQ — há reprocessamento automático ou apenas reenvio manual via Admin API?
- Mecanismo de rotação dos segredos por cliente — a definir com o time de Segurança.
