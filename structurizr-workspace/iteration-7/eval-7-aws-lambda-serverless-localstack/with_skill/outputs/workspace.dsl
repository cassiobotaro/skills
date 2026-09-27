workspace "OrderFlow" "API serverless de pedidos: criação e listagem de pedidos pelo app mobile e confirmação de pagamento via webhook do Stripe." {

    !identifiers hierarchical

    model {
        cliente = person "Cliente" "Faz e acompanha pedidos pelo app mobile."

        appMobile = softwareSystem "App Mobile" "Aplicativo dos clientes para criar e consultar pedidos." {
            tags "External"
        }

        stripe = softwareSystem "Stripe" "Provedor de pagamentos; notifica o OrderFlow sobre eventos de pagamento via webhook." {
            tags "External"
        }

        orderflow = softwareSystem "OrderFlow" "API serverless de pedidos: recebe, armazena e lista pedidos e registra o resultado do pagamento." {
            criarPedido = container "criar-pedido" "Recebe um novo pedido e o grava na tabela orders." "AWS Lambda / Python" {
                tags "Lambda" "Amazon Web Services - Lambda"
            }
            listarPedidos = container "listar-pedidos" "Lê os pedidos da tabela orders e os devolve ao chamador." "AWS Lambda / Python" {
                tags "Lambda" "Amazon Web Services - Lambda"
            }
            webhookPagamento = container "webhook-pagamento" "Recebe os eventos de pagamento do Stripe e atualiza o pedido correspondente na tabela orders." "AWS Lambda / Python" {
                tags "Lambda" "Amazon Web Services - Lambda"
            }
            orders = container "Tabela orders" "Armazena os pedidos e o estado do seu pagamento." "Amazon DynamoDB" {
                tags "Database" "Amazon Web Services - DynamoDB"
            }
        }

        cliente -> appMobile "Cria e consulta pedidos usando"
        appMobile -> orderflow.criarPedido "Envia novos pedidos para" "JSON/HTTPS"
        appMobile -> orderflow.listarPedidos "Consulta os pedidos do cliente em" "JSON/HTTPS"
        stripe -> orderflow.webhookPagamento "Envia eventos de pagamento para" "Webhook JSON/HTTPS"

        orderflow.criarPedido -> orderflow.orders "Grava e lê pedidos em" "DynamoDB API/HTTPS"
        orderflow.listarPedidos -> orderflow.orders "Lê e grava pedidos em" "DynamoDB API/HTTPS"
        orderflow.webhookPagamento -> orderflow.orders "Lê e atualiza pedidos em" "DynamoDB API/HTTPS"

        // ---------------------------------------------------------------
        // Desenvolvimento: tudo roda no laptop de cada dev, via LocalStack
        // ---------------------------------------------------------------
        dev = deploymentEnvironment "Desenvolvimento" {
            laptop = deploymentNode "Laptop do desenvolvedor" "Ambiente local de cada desenvolvedor." {
                localstack = deploymentNode "LocalStack" "Emula os serviços AWS usados pelo OrderFlow." "LocalStack" {
                    apigw = infrastructureNode "Amazon API Gateway (emulado)" "Roteia as requisições HTTP para as funções e valida a API key; sem lógica custom." "Amazon API Gateway" {
                        tags "Amazon Web Services - API Gateway"
                    }
                    lambda = deploymentNode "AWS Lambda (emulado)" "" "AWS Lambda" {
                        tags "Amazon Web Services - Lambda"
                        criarPedido = containerInstance orderflow.criarPedido
                        listarPedidos = containerInstance orderflow.listarPedidos
                        webhookPagamento = containerInstance orderflow.webhookPagamento
                    }
                    dynamodb = deploymentNode "Amazon DynamoDB (emulado)" "" "Amazon DynamoDB" {
                        tags "Amazon Web Services - DynamoDB"
                        containerInstance orderflow.orders
                    }
                }
            }

            laptop.localstack.apigw -> laptop.localstack.lambda.criarPedido "Invoca" "AWS Lambda"
            laptop.localstack.apigw -> laptop.localstack.lambda.listarPedidos "Invoca" "AWS Lambda"
            laptop.localstack.apigw -> laptop.localstack.lambda.webhookPagamento "Invoca" "AWS Lambda"
        }

        // ---------------------------------------------------------------
        // Produção: AWS, região us-east-1
        // ---------------------------------------------------------------
        prod = deploymentEnvironment "Produção" {
            deploymentNode "Smartphone do cliente" "" "iOS / Android" {
                softwareSystemInstance appMobile
            }

            deploymentNode "Stripe" "Infraestrutura do provedor de pagamentos." {
                softwareSystemInstance stripe
            }

            aws = deploymentNode "Amazon Web Services" "" "AWS" {
                region = deploymentNode "us-east-1" "" "AWS Region" {
                    tags "Amazon Web Services - Region"
                    apigw = infrastructureNode "Amazon API Gateway" "Roteia as requisições HTTP para as funções e valida a API key; sem lógica custom." "Amazon API Gateway" {
                        tags "Amazon Web Services - API Gateway"
                    }
                    deploymentNode "AWS Lambda" "" "AWS Lambda" {
                        tags "Amazon Web Services - Lambda"
                        containerInstance orderflow.criarPedido
                        containerInstance orderflow.listarPedidos
                        containerInstance orderflow.webhookPagamento
                    }
                    deploymentNode "Amazon DynamoDB" "" "Amazon DynamoDB" {
                        tags "Amazon Web Services - DynamoDB"
                        containerInstance orderflow.orders
                    }
                }
            }

            appMobile -/> orderflow.criarPedido {
                appMobile -> aws.region.apigw "Chama a API usando" "JSON/HTTPS + API key"
                aws.region.apigw -> orderflow.criarPedido "Invoca" "AWS Lambda"
            }
            appMobile -/> orderflow.listarPedidos {
                aws.region.apigw -> orderflow.listarPedidos "Invoca" "AWS Lambda"
            }
            stripe -/> orderflow.webhookPagamento {
                stripe -> aws.region.apigw "Envia eventos de pagamento para" "Webhook JSON/HTTPS"
                aws.region.apigw -> orderflow.webhookPagamento "Invoca" "AWS Lambda"
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
        }

        theme amazon-web-services-2025.07
    }

    configuration {
        scope softwaresystem
    }
}
