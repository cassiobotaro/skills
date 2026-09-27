workspace "OrderFlow" "API serverless de pedidos." {

    !identifiers hierarchical

    model {
        archetypes {
            lambda = container {
                technology "AWS Lambda - Python"
                tags "Lambda"
            }
        }

        stripe = softwareSystem "Stripe" "Provedor de pagamentos. Notifica o OrderFlow sobre eventos de pagamento por webhook." {
            tags "External"
        }

        orderflow = softwareSystem "OrderFlow" "API serverless de pedidos." {
            criarPedido = lambda "criar-pedido" "Cria um novo pedido."
            listarPedidos = lambda "listar-pedidos" "Lista os pedidos existentes."
            webhookPagamento = lambda "webhook-pagamento" "Recebe os eventos de pagamento enviados pelo Stripe e atualiza o pedido correspondente."
            orders = container "orders" "Tabela de pedidos." "Amazon DynamoDB" {
                tags "Database"
            }

            criarPedido -> orders "Lê e grava pedidos em" "DynamoDB API/HTTPS"
            listarPedidos -> orders "Lê e grava pedidos em" "DynamoDB API/HTTPS"
            webhookPagamento -> orders "Lê e grava pedidos em" "DynamoDB API/HTTPS"
        }

        stripe -> orderflow.webhookPagamento "Envia eventos de pagamento para" "JSON/HTTPS"

        dev = deploymentEnvironment "Desenvolvimento" {
            laptop = deploymentNode "Laptop do desenvolvedor" "Cada dev roda o ambiente completo localmente." {
                localstack = deploymentNode "LocalStack" "Emulação local dos serviços AWS." "LocalStack" {
                    apigw = infrastructureNode "API Gateway" "Roteamento e autenticação por API key (emulado)." "Amazon API Gateway (LocalStack)"
                    deploymentNode "Lambda" "" "LocalStack Lambda" {
                        instanceOf orderflow.criarPedido
                        instanceOf orderflow.listarPedidos
                        instanceOf orderflow.webhookPagamento
                    }
                    deploymentNode "DynamoDB" "" "LocalStack DynamoDB" {
                        instanceOf orderflow.orders
                    }
                }
            }
        }

        prod = deploymentEnvironment "Produção" {
            deploymentNode "Stripe" "Infraestrutura do Stripe (externa)." {
                instanceOf stripe
            }
            aws = deploymentNode "Amazon Web Services" {
                tags "Amazon Web Services - AWS Cloud"
                region = deploymentNode "us-east-1" {
                    tags "Amazon Web Services - Region"
                    apigw = infrastructureNode "API Gateway" "Roteamento e autenticação por API key." "Amazon API Gateway" {
                        tags "Amazon Web Services - API Gateway"
                    }
                    deploymentNode "AWS Lambda" {
                        tags "Amazon Web Services - Lambda"
                        instanceOf orderflow.criarPedido
                        instanceOf orderflow.listarPedidos
                        instanceOf orderflow.webhookPagamento
                    }
                    deploymentNode "Amazon DynamoDB" {
                        tags "Amazon Web Services - DynamoDB"
                        instanceOf orderflow.orders
                    }
                }
            }

            stripe -/> orderflow.webhookPagamento {
                stripe -> aws.region.apigw "Envia eventos de pagamento para" "JSON/HTTPS"
                aws.region.apigw -> orderflow.webhookPagamento "Encaminha eventos de pagamento para" "JSON/HTTPS"
            }
        }
    }

    views {
        systemContext orderflow "SystemContext" {
            include *
            autoLayout lr
        }

        container orderflow "Containers" {
            include *
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
