workspace "OrderFlow" "API serverless de pedidos." {

    !identifiers hierarchical

    model {
        cliente = person "Cliente" "Faz e acompanha pedidos pelo app mobile."

        orderflow = softwareSystem "OrderFlow" "API serverless de pedidos: criação, listagem e confirmação de pagamento." {
            app = container "App Mobile" "App dos clientes para criar e consultar pedidos." "Flutter" {
                tags "Mobile"
            }
            criarPedido = container "criar-pedido" "Função que cria um novo pedido." "Python, AWS Lambda" {
                tags "Lambda"
            }
            listarPedidos = container "listar-pedidos" "Função que lista os pedidos." "Python, AWS Lambda" {
                tags "Lambda"
            }
            webhookPagamento = container "webhook-pagamento" "Função que recebe as notificações de pagamento da Stripe." "Python, AWS Lambda" {
                tags "Lambda"
            }
            orders = container "Tabela orders" "Armazena os pedidos." "Amazon DynamoDB" {
                tags "Database"
            }
        }

        stripe = softwareSystem "Stripe" "Provedor de pagamentos (terceiro)." {
            tags "External"
        }

        cliente -> orderflow.app "Cria e consulta pedidos usando"
        orderflow.app -> orderflow.criarPedido "Envia novos pedidos para" "HTTPS"
        orderflow.app -> orderflow.listarPedidos "Consulta pedidos em" "HTTPS"
        stripe -> orderflow.webhookPagamento "Envia eventos de pagamento para" "Webhook/HTTPS"
        orderflow.criarPedido -> orderflow.orders "Lê e grava pedidos em" "AWS SDK/HTTPS"
        orderflow.listarPedidos -> orderflow.orders "Lê e grava pedidos em" "AWS SDK/HTTPS"
        orderflow.webhookPagamento -> orderflow.orders "Lê e grava pedidos em" "AWS SDK/HTTPS"

        dev = deploymentEnvironment "Desenvolvimento" {
            laptop = deploymentNode "Laptop do desenvolvedor" "Cada dev roda o ambiente completo localmente." {
                instanceOf orderflow.app

                localstack = deploymentNode "LocalStack" "Emula os serviços AWS localmente." "LocalStack" {
                    apigw = infrastructureNode "API Gateway" "Roteia as requisições e valida a API key." "Amazon API Gateway (emulado)" {
                        tags "Amazon Web Services - API Gateway"
                    }
                    deploymentNode "Lambda" "Executa as funções." "AWS Lambda (emulado)" {
                        tags "Amazon Web Services - Lambda"
                        instanceOf orderflow.criarPedido
                        instanceOf orderflow.listarPedidos
                        instanceOf orderflow.webhookPagamento
                    }
                    deploymentNode "DynamoDB" "Hospeda a tabela." "Amazon DynamoDB (emulado)" {
                        tags "Amazon Web Services - DynamoDB"
                        instanceOf orderflow.orders
                    }
                }
            }

            orderflow.app -/> orderflow.criarPedido {
                orderflow.app -> laptop.localstack.apigw "Envia requisições para" "HTTPS"
                laptop.localstack.apigw -> orderflow.criarPedido "Invoca" "AWS Lambda"
            }
            orderflow.app -/> orderflow.listarPedidos {
                laptop.localstack.apigw -> orderflow.listarPedidos "Invoca" "AWS Lambda"
            }
        }

        prod = deploymentEnvironment "Produção" {
            dispositivo = deploymentNode "Smartphone do cliente" "Dispositivo onde o app roda." {
                instanceOf orderflow.app
            }

            stripeInfra = deploymentNode "Stripe" "Infraestrutura da Stripe (terceiro)." {
                tags "External"
                instanceOf stripe
            }

            aws = deploymentNode "Amazon Web Services" "Conta AWS de produção." {
                region = deploymentNode "us-east-1" "Região de produção." {
                    tags "Amazon Web Services - Region"
                    apigw = infrastructureNode "API Gateway" "Roteia as requisições e valida a API key." "Amazon API Gateway" {
                        tags "Amazon Web Services - API Gateway"
                    }
                    deploymentNode "AWS Lambda" "Executa as funções." {
                        tags "Amazon Web Services - Lambda"
                        instanceOf orderflow.criarPedido
                        instanceOf orderflow.listarPedidos
                        instanceOf orderflow.webhookPagamento
                    }
                    deploymentNode "Amazon DynamoDB" "Hospeda a tabela." {
                        tags "Amazon Web Services - DynamoDB"
                        instanceOf orderflow.orders
                    }
                }
            }

            orderflow.app -/> orderflow.criarPedido {
                orderflow.app -> aws.region.apigw "Envia requisições para" "HTTPS"
                aws.region.apigw -> orderflow.criarPedido "Invoca" "AWS Lambda"
            }
            orderflow.app -/> orderflow.listarPedidos {
                aws.region.apigw -> orderflow.listarPedidos "Invoca" "AWS Lambda"
            }
            stripe -/> orderflow.webhookPagamento {
                stripe -> aws.region.apigw "Envia eventos de pagamento para" "Webhook/HTTPS"
                aws.region.apigw -> orderflow.webhookPagamento "Invoca" "AWS Lambda"
            }
        }
    }

    views {
        systemContext orderflow "SystemContext" {
            include *
            autoLayout
        }

        container orderflow "Containers" {
            include *
            autoLayout
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
            element "Mobile" {
                shape mobileDevicePortrait
            }
            element "Database" {
                shape cylinder
            }
            element "External" {
                background #999999
                color #ffffff
            }
        }

        theme amazon-web-services-2025.07
    }

    configuration {
        scope softwaresystem
    }
}
