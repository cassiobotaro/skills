workspace "OrderFlow" "API serverless de pedidos: três funções Lambda em Python sobre uma tabela DynamoDB, expostas pelo Amazon API Gateway." {

    !identifiers hierarchical

    model {
        archetypes {
            lambda = container {
                technology "AWS Lambda (Python)"
                tags "Lambda" "Amazon Web Services - Lambda"
            }
        }

        cliente = person "Cliente" "Faz pedidos pelo app mobile."

        app = softwareSystem "App Mobile" "Aplicativo dos clientes; chama a API do OrderFlow." {
            tags "External" "Mobile App"
        }

        orderflow = softwareSystem "OrderFlow" "API serverless de pedidos." {
            criarPedido = lambda "criar-pedido" "Cria um novo pedido."
            listarPedidos = lambda "listar-pedidos" "Lista os pedidos."
            webhookPagamento = lambda "webhook-pagamento" "Recebe os eventos de pagamento enviados pelo Stripe."
            orders = container "orders" "Tabela com os pedidos." "Amazon DynamoDB" {
                tags "Database" "Amazon Web Services - DynamoDB"
            }
        }

        stripe = softwareSystem "Stripe" "Provedor de pagamentos; chama o webhook de pagamento." {
            tags "External"
        }

        cliente -> app "Faz pedidos usando"
        app -> orderflow.criarPedido "Cria pedidos chamando" "JSON/HTTPS"
        app -> orderflow.listarPedidos "Lista pedidos chamando" "JSON/HTTPS"
        stripe -> orderflow.webhookPagamento "Notifica eventos de pagamento para" "Webhook JSON/HTTPS"
        orderflow.criarPedido -> orderflow.orders "Lê e grava pedidos em" "DynamoDB API/HTTPS"
        orderflow.listarPedidos -> orderflow.orders "Lê e grava pedidos em" "DynamoDB API/HTTPS"
        orderflow.webhookPagamento -> orderflow.orders "Lê e grava pedidos em" "DynamoDB API/HTTPS"

        dev = deploymentEnvironment "Desenvolvimento" {
            laptop = deploymentNode "Laptop do desenvolvedor" "Cada dev roda o ambiente completo localmente." {
                localstack = deploymentNode "LocalStack" "Emulação local dos serviços AWS." "LocalStack" {
                    apigw = infrastructureNode "API Gateway (emulado)" "Roteamento e autenticação por API key, sem lógica custom." "LocalStack API Gateway"
                    lambda = deploymentNode "Lambda (emulado)" "" "LocalStack Lambda" {
                        criar = instanceOf orderflow.criarPedido
                        listar = instanceOf orderflow.listarPedidos
                        webhook = instanceOf orderflow.webhookPagamento
                    }
                    dynamodb = deploymentNode "DynamoDB (emulado)" "" "LocalStack DynamoDB" {
                        instanceOf orderflow.orders
                    }
                }
            }

            laptop.localstack.apigw -> laptop.localstack.lambda.criar "Encaminha requisições para" "JSON/HTTPS"
            laptop.localstack.apigw -> laptop.localstack.lambda.listar "Encaminha requisições para" "JSON/HTTPS"
            laptop.localstack.apigw -> laptop.localstack.lambda.webhook "Encaminha o webhook para" "JSON/HTTPS"
        }

        prod = deploymentEnvironment "Produção" {
            dispositivo = deploymentNode "Dispositivo móvel do cliente" {
                instanceOf app
            }

            stripeCloud = deploymentNode "Stripe" {
                instanceOf stripe
            }

            aws = deploymentNode "Amazon Web Services" {
                tags "Amazon Web Services - Cloud"
                region = deploymentNode "us-east-1" {
                    tags "Amazon Web Services - Region"
                    apigw = infrastructureNode "Amazon API Gateway" "Roteamento e autenticação por API key, sem lógica custom." "Amazon API Gateway" {
                        tags "Amazon Web Services - API Gateway"
                    }
                    lambda = deploymentNode "AWS Lambda" "" "AWS Lambda" {
                        tags "Amazon Web Services - Lambda"
                        instanceOf orderflow.criarPedido
                        instanceOf orderflow.listarPedidos
                        instanceOf orderflow.webhookPagamento
                    }
                    dynamodb = deploymentNode "Amazon DynamoDB" "" "Amazon DynamoDB" {
                        tags "Amazon Web Services - DynamoDB"
                        instanceOf orderflow.orders
                    }
                }
            }

            app -/> orderflow.criarPedido {
                app -> aws.region.apigw "Chama a API (autenticado por API key) via" "JSON/HTTPS"
                aws.region.apigw -> orderflow.criarPedido "Encaminha requisições para" "JSON/HTTPS"
            }
            app -/> orderflow.listarPedidos {
                aws.region.apigw -> orderflow.listarPedidos "Encaminha requisições para" "JSON/HTTPS"
            }
            stripe -/> orderflow.webhookPagamento {
                stripe -> aws.region.apigw "Envia eventos de pagamento para" "Webhook JSON/HTTPS"
                aws.region.apigw -> orderflow.webhookPagamento "Encaminha o webhook para" "JSON/HTTPS"
            }
        }
    }

    views {
        systemContext orderflow "SystemContext" {
            include *
            include cliente
            autoLayout lr
        }

        container orderflow "Containers" {
            include *
            include cliente
            autoLayout lr
        }

        deployment orderflow dev "Deployment-Dev" {
            include *
            autoLayout lr
        }

        deployment orderflow prod "Deployment-Prod" {
            include *
            autoLayout lr
        }

        styles {
            element "Element" {
                background #1168bd
                color #ffffff
            }
            element "Person" {
                shape person
            }
            element "Database" {
                shape cylinder
            }
            element "External" {
                background #999999
                color #ffffff
            }
            element "Mobile App" {
                shape mobileDevicePortrait
            }
            element "Infrastructure Node" {
                shape ellipse
            }
        }

        theme amazon-web-services-2025.07
    }

    configuration {
        scope softwaresystem
    }
}
