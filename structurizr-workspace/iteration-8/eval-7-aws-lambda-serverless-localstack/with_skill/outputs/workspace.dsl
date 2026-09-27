workspace "OrderFlow" "API serverless de pedidos: três funções Lambda em Python sobre uma tabela DynamoDB, expostas pelo Amazon API Gateway." {

    !identifiers hierarchical

    model {
        archetypes {
            lambda = container {
                technology "AWS Lambda (Python)"
                tag "Lambda"
            }
        }

        cliente = person "Cliente" "Faz e acompanha pedidos pelo app mobile."

        app = softwareSystem "App Mobile" "App dos clientes que cria e consulta pedidos chamando a API do OrderFlow." {
            tags "Mobile"
        }

        orderflow = softwareSystem "OrderFlow" "API serverless de pedidos: cria, lista e atualiza pedidos conforme os pagamentos são confirmados." {
            criarPedido = lambda "criar-pedido" "Recebe um novo pedido e o grava na tabela de pedidos."
            listarPedidos = lambda "listar-pedidos" "Consulta os pedidos na tabela de pedidos e os devolve ao chamador."
            webhookPagamento = lambda "webhook-pagamento" "Recebe os eventos de pagamento do Stripe e atualiza o pedido correspondente."
            orders = container "Tabela orders" "Armazena os pedidos e seu estado." "Amazon DynamoDB" {
                tags "Database"
            }

            criarPedido -> orders "Lê e grava pedidos em" "DynamoDB API/HTTPS"
            listarPedidos -> orders "Lê e grava pedidos em" "DynamoDB API/HTTPS"
            webhookPagamento -> orders "Lê e grava pedidos em" "DynamoDB API/HTTPS"
        }

        stripe = softwareSystem "Stripe" "Provedor de pagamentos; notifica o OrderFlow sobre eventos de pagamento." {
            tags "External"
        }

        cliente -> app "Cria e acompanha pedidos usando"
        app -> orderflow.criarPedido "Cria pedidos chamando" "JSON/HTTPS"
        app -> orderflow.listarPedidos "Lista pedidos chamando" "JSON/HTTPS"
        stripe -> orderflow.webhookPagamento "Envia eventos de pagamento para" "Webhook JSON/HTTPS"

        // Dev: cada dev roda o OrderFlow inteiro no laptop, emulado pelo LocalStack.
        dev = deploymentEnvironment "Desenvolvimento" {
            laptop = deploymentNode "Laptop do dev" "Estação de trabalho de cada desenvolvedor." {
                localstack = deploymentNode "LocalStack" "Emulação local dos serviços AWS." "LocalStack" {
                    apigw = infrastructureNode "API Gateway" "Roteamento e autenticação por API key (emulado)." "Amazon API Gateway (LocalStack)"
                    deploymentNode "Lambda" "" "AWS Lambda (LocalStack)" {
                        instanceOf orderflow.criarPedido
                        instanceOf orderflow.listarPedidos
                        instanceOf orderflow.webhookPagamento
                    }
                    deploymentNode "DynamoDB" "" "Amazon DynamoDB (LocalStack)" {
                        instanceOf orderflow.orders
                    }
                }
            }
        }

        // Produção: AWS, região us-east-1.
        prod = deploymentEnvironment "Produção" {
            smartphone = deploymentNode "Smartphone do cliente" "Dispositivo onde o app mobile roda." {
                instanceOf app
            }

            stripeCloud = deploymentNode "Stripe" "Infraestrutura do Stripe." {
                instanceOf stripe
            }

            aws = deploymentNode "Amazon Web Services" {
                tags "Amazon Web Services - AWS Cloud"
                region = deploymentNode "us-east-1" {
                    tags "Amazon Web Services - Region"
                    apigw = infrastructureNode "API Gateway" "Roteamento e autenticação por API key; sem lógica custom." "Amazon API Gateway" {
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

            // Em produção toda chamada externa entra pelo API Gateway.
            app -/> orderflow.criarPedido {
                app -> aws.region.apigw "Chama a API do OrderFlow via" "JSON/HTTPS"
                aws.region.apigw -> orderflow.criarPedido "Encaminha requisições de criação de pedido para" "JSON/HTTPS"
            }
            app -/> orderflow.listarPedidos {
                aws.region.apigw -> orderflow.listarPedidos "Encaminha requisições de listagem de pedidos para" "JSON/HTTPS"
            }
            stripe -/> orderflow.webhookPagamento {
                stripe -> aws.region.apigw "Envia eventos de pagamento para" "Webhook JSON/HTTPS"
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

        deployment orderflow dev "Deployment-Desenvolvimento" {
            include *
            autoLayout lr
        }

        deployment orderflow prod "Deployment-Producao" {
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
            element "Mobile" {
                shape mobileDevicePortrait
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
