workspace "OrderFlow" "API serverless de pedidos: criação, listagem e confirmação de pagamento via Stripe." {

    !identifiers hierarchical

    model {
        cliente = person "Cliente" "Cria e acompanha seus pedidos pelo app mobile."

        orderflow = softwareSystem "OrderFlow" "API serverless que recebe, armazena e atualiza pedidos, integrada ao Stripe para pagamento." {
            app = container "App Mobile" "Interface dos clientes para criar e acompanhar pedidos." "Flutter" {
                tags "Mobile"
            }
            criarPedido = container "criar-pedido" "Função que registra um novo pedido." "Python, AWS Lambda" {
                tags "Lambda"
            }
            listarPedidos = container "listar-pedidos" "Função que retorna os pedidos do cliente." "Python, AWS Lambda" {
                tags "Lambda"
            }
            webhookPagamento = container "webhook-pagamento" "Função que recebe os eventos de pagamento do Stripe e atualiza o pedido correspondente." "Python, AWS Lambda" {
                tags "Lambda"
            }
            orders = container "Tabela orders" "Armazena os pedidos e seu estado de pagamento." "Amazon DynamoDB" {
                tags "Database"
            }
        }

        stripe = softwareSystem "Stripe" "Provedor de pagamentos; notifica o OrderFlow sobre eventos de pagamento." {
            tags "External"
        }

        cliente -> orderflow.app "Cria e acompanha pedidos usando"
        orderflow.app -> orderflow.criarPedido "Envia novos pedidos para" "JSON/HTTPS"
        orderflow.app -> orderflow.listarPedidos "Consulta os pedidos em" "JSON/HTTPS"
        stripe -> orderflow.webhookPagamento "Envia eventos de pagamento para" "JSON/HTTPS"
        orderflow.criarPedido -> orderflow.orders "Lê e grava pedidos em" "DynamoDB API/HTTPS"
        orderflow.listarPedidos -> orderflow.orders "Lê e grava pedidos em" "DynamoDB API/HTTPS"
        orderflow.webhookPagamento -> orderflow.orders "Lê e grava pedidos em" "DynamoDB API/HTTPS"

        dev = deploymentEnvironment "Desenvolvimento" {
            laptop = deploymentNode "Laptop do desenvolvedor" "Ambiente local de cada dev." {
                deploymentNode "App Mobile (execução local)" "" "Flutter" {
                    instanceOf orderflow.app
                }
                localstack = deploymentNode "LocalStack" "Emula os serviços AWS usados pelo OrderFlow." "LocalStack" {
                    apigw = infrastructureNode "API Gateway (emulado)" "Roteia as requisições e valida a API key." "Amazon API Gateway (emulado)" {
                        tags "Gateway"
                    }
                    deploymentNode "Lambda (emulado)" "" "AWS Lambda (emulado)" {
                        instanceOf orderflow.criarPedido
                        instanceOf orderflow.listarPedidos
                        instanceOf orderflow.webhookPagamento
                    }
                    deploymentNode "DynamoDB (emulado)" "" "Amazon DynamoDB (emulado)" {
                        instanceOf orderflow.orders
                    }
                }
            }

            orderflow.app -/> orderflow.criarPedido {
                orderflow.app -> laptop.localstack.apigw "Envia novos pedidos e consultas para" "JSON/HTTPS"
                laptop.localstack.apigw -> orderflow.criarPedido "Encaminha a criação de pedidos para" "JSON/HTTPS"
            }
            orderflow.app -/> orderflow.listarPedidos {
                laptop.localstack.apigw -> orderflow.listarPedidos "Encaminha a listagem de pedidos para" "JSON/HTTPS"
            }
        }

        prod = deploymentEnvironment "Produção" {
            deploymentNode "Smartphone do cliente" "Dispositivo do cliente com o app instalado." {
                instanceOf orderflow.app
            }

            deploymentNode "Stripe" "" "SaaS" {
                instanceOf stripe
            }

            aws = deploymentNode "Amazon Web Services" {
                tags "Amazon Web Services - AWS Cloud"
                region = deploymentNode "us-east-1" {
                    tags "Amazon Web Services - Region"
                    apigw = infrastructureNode "API Gateway" "Roteia as requisições e valida a API key; sem lógica customizada." "Amazon API Gateway" {
                        tags "Gateway" "Amazon Web Services - API Gateway"
                    }
                    deploymentNode "AWS Lambda" "" "AWS Lambda" {
                        tags "Amazon Web Services - Lambda"
                        instanceOf orderflow.criarPedido
                        instanceOf orderflow.listarPedidos
                        instanceOf orderflow.webhookPagamento
                    }
                    deploymentNode "Amazon DynamoDB" "" "Amazon DynamoDB" {
                        tags "Amazon Web Services - DynamoDB"
                        instanceOf orderflow.orders
                    }
                }
            }

            orderflow.app -/> orderflow.criarPedido {
                orderflow.app -> aws.region.apigw "Envia novos pedidos e consultas para" "JSON/HTTPS"
                aws.region.apigw -> orderflow.criarPedido "Encaminha a criação de pedidos para" "JSON/HTTPS"
            }
            orderflow.app -/> orderflow.listarPedidos {
                aws.region.apigw -> orderflow.listarPedidos "Encaminha a listagem de pedidos para" "JSON/HTTPS"
            }
            stripe -/> orderflow.webhookPagamento {
                stripe -> aws.region.apigw "Envia eventos de pagamento para" "JSON/HTTPS"
                aws.region.apigw -> orderflow.webhookPagamento "Encaminha o webhook de pagamento para" "JSON/HTTPS"
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

        deployment orderflow prod "Deployment-Production" {
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
            element "Gateway" {
                shape hexagon
            }
        }

        theme amazon-web-services-2025.07
    }

    configuration {
        scope softwaresystem
    }
}
