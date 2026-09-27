workspace "OrderFlow" "API serverless de pedidos: três funções Lambda em Python sobre uma tabela DynamoDB, expostas pelo Amazon API Gateway." {

    !identifiers hierarchical

    model {
        cliente = person "Cliente" "Faz e acompanha pedidos pelo app mobile."

        // Classificação provisória: o app está fora da fronteira do OrderFlow porque o sistema
        // foi descrito como "a API". Se o mesmo time mantém o app Flutter, ele passa a ser um
        // container dentro de `orderflow` (ver resposta).
        app = softwareSystem "App Mobile" "App dos clientes para fazer e acompanhar pedidos." "Flutter" {
            tags "External"
        }

        stripe = softwareSystem "Stripe" "Plataforma de pagamentos; notifica o OrderFlow sobre eventos de pagamento." {
            tags "External"
        }

        orderflow = softwareSystem "OrderFlow" "API serverless que recebe, lista e atualiza pedidos dos clientes." {
            criarPedido = container "criar-pedido" "Recebe um novo pedido e o registra na tabela orders." "Python, AWS Lambda" {
                tags "Lambda"
            }
            listarPedidos = container "listar-pedidos" "Retorna os pedidos registrados na tabela orders." "Python, AWS Lambda" {
                tags "Lambda"
            }
            webhookPagamento = container "webhook-pagamento" "Recebe eventos de pagamento do Stripe e atualiza o pedido correspondente." "Python, AWS Lambda" {
                tags "Lambda"
            }
            orders = container "Tabela orders" "Armazena os pedidos e seu estado de pagamento." "Amazon DynamoDB" {
                tags "Database"
            }
        }

        cliente -> app "Faz e acompanha pedidos usando"
        app -> orderflow.criarPedido "Envia novos pedidos para" "JSON/HTTPS"
        app -> orderflow.listarPedidos "Consulta pedidos em" "JSON/HTTPS"
        stripe -> orderflow.webhookPagamento "Notifica eventos de pagamento para" "JSON/HTTPS (webhook)"

        orderflow.criarPedido -> orderflow.orders "Lê e grava pedidos em" "AWS SDK/HTTPS"
        orderflow.listarPedidos -> orderflow.orders "Lê e grava pedidos em" "AWS SDK/HTTPS"
        orderflow.webhookPagamento -> orderflow.orders "Lê e grava pedidos em" "AWS SDK/HTTPS"

        dev = deploymentEnvironment "Desenvolvimento" {
            laptop = deploymentNode "Laptop do desenvolvedor" "Cada dev roda a stack completa localmente." {
                localstack = deploymentNode "LocalStack" "Emula os serviços AWS usados pelo OrderFlow." "LocalStack" {
                    gw = infrastructureNode "API Gateway (emulado)" "Roteia as requisições para as funções e autentica por API key." "Amazon API Gateway (LocalStack)" {
                        tags "Gateway"
                    }
                    lambda = deploymentNode "Lambda (emulado)" "" "AWS Lambda (LocalStack)" {
                        instanceOf orderflow.criarPedido
                        instanceOf orderflow.listarPedidos
                        instanceOf orderflow.webhookPagamento
                    }
                    dynamodb = deploymentNode "DynamoDB (emulado)" "" "Amazon DynamoDB (LocalStack)" {
                        instanceOf orderflow.orders
                    }
                }
            }

            laptop.localstack.gw -> orderflow.criarPedido "Encaminha requisições para" "JSON/HTTPS"
            laptop.localstack.gw -> orderflow.listarPedidos "Encaminha requisições para" "JSON/HTTPS"
            laptop.localstack.gw -> orderflow.webhookPagamento "Encaminha requisições para" "JSON/HTTPS"
        }

        prod = deploymentEnvironment "Produção" {
            smartphone = deploymentNode "Smartphone do cliente" {
                softwareSystemInstance app
            }

            stripeCloud = deploymentNode "Stripe" "Serviço operado pela Stripe." {
                softwareSystemInstance stripe
            }

            aws = deploymentNode "Amazon Web Services" {
                tags "Amazon Web Services - Cloud"
                region = deploymentNode "us-east-1" {
                    tags "Amazon Web Services - Region"
                    gw = infrastructureNode "API Gateway" "Roteia as requisições para as funções e autentica por API key; sem lógica customizada." "Amazon API Gateway" {
                        tags "Gateway" "Amazon Web Services - API Gateway"
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
                app -> aws.region.gw "Chama a API por" "JSON/HTTPS"
                aws.region.gw -> orderflow.criarPedido "Encaminha requisições para" "JSON/HTTPS"
            }
            app -/> orderflow.listarPedidos {
                aws.region.gw -> orderflow.listarPedidos "Encaminha requisições para" "JSON/HTTPS"
            }
            stripe -/> orderflow.webhookPagamento {
                stripe -> aws.region.gw "Envia eventos de pagamento para" "JSON/HTTPS (webhook)"
                aws.region.gw -> orderflow.webhookPagamento "Encaminha requisições para" "JSON/HTTPS"
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

        deployment orderflow dev "Deployment-Development" {
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
