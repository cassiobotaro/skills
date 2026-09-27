workspace "OrderFlow" "API serverless de pedidos: três funções Lambda em Python sobre uma tabela DynamoDB, atrás do Amazon API Gateway." {

    !identifiers hierarchical

    model {
        // PENDENTE: o app mobile (Flutter) dos clientes ainda não está no modelo.
        // Se o mesmo time constrói o app, ele entra como container dentro de `orderflow`;
        // se outro time (ou parceiro) constrói, entra como softwareSystem separado.
        // Veja as duas opções na resposta que acompanha este arquivo.

        orderflow = softwareSystem "OrderFlow" "API serverless de pedidos: cria, lista e recebe confirmações de pagamento dos pedidos." {
            createOrder = container "criar-pedido" "Cria um novo pedido." "AWS Lambda - Python" {
                tags "Lambda"
            }
            listOrders = container "listar-pedidos" "Lista os pedidos." "AWS Lambda - Python" {
                tags "Lambda"
            }
            paymentWebhook = container "webhook-pagamento" "Recebe as notificações de pagamento enviadas pelo Stripe." "AWS Lambda - Python" {
                tags "Lambda"
            }
            orders = container "Tabela orders" "Armazena os pedidos." "Amazon DynamoDB" {
                tags "Database"
            }
        }

        stripe = softwareSystem "Stripe" "Provedor de pagamentos (SaaS). Notifica o OrderFlow sobre eventos de pagamento por webhook." {
            tags "External"
        }

        orderflow.createOrder -> orderflow.orders "Lê e grava pedidos em" "DynamoDB API/HTTPS"
        orderflow.listOrders -> orderflow.orders "Lê e grava pedidos em" "DynamoDB API/HTTPS"
        orderflow.paymentWebhook -> orderflow.orders "Lê e grava pedidos em" "DynamoDB API/HTTPS"
        stripe -> orderflow.paymentWebhook "Envia eventos de pagamento para" "Webhook JSON/HTTPS"

        // Desenvolvimento: cada dev roda tudo no laptop com LocalStack.
        dev = deploymentEnvironment "Desenvolvimento" {
            laptop = deploymentNode "Laptop do desenvolvedor" "Ambiente local de cada desenvolvedor." {
                localstack = deploymentNode "LocalStack" "Emula os serviços AWS localmente." "LocalStack" {
                    apigw = infrastructureNode "API Gateway" "Roteamento e autenticação por API key (emulado)." "Amazon API Gateway (LocalStack)" {
                        tags "Amazon Web Services - API Gateway"
                    }
                    lambda = deploymentNode "Lambda" "Serviço Lambda emulado pelo LocalStack." "AWS Lambda (LocalStack)" {
                        tags "Amazon Web Services - Lambda"
                        createOrder = instanceOf orderflow.createOrder
                        listOrders = instanceOf orderflow.listOrders
                        paymentWebhook = instanceOf orderflow.paymentWebhook
                    }
                    dynamodb = deploymentNode "DynamoDB" "Serviço DynamoDB emulado pelo LocalStack." "Amazon DynamoDB (LocalStack)" {
                        tags "Amazon Web Services - DynamoDB"
                        instanceOf orderflow.orders
                    }
                }
            }

            laptop.localstack.apigw -> laptop.localstack.lambda.createOrder "Roteia requisições para" "Invocação Lambda"
            laptop.localstack.apigw -> laptop.localstack.lambda.listOrders "Roteia requisições para" "Invocação Lambda"
            laptop.localstack.apigw -> laptop.localstack.lambda.paymentWebhook "Roteia requisições para" "Invocação Lambda"
        }

        // Produção: AWS, região us-east-1.
        prod = deploymentEnvironment "Produção" {
            aws = deploymentNode "Amazon Web Services" "Conta AWS de produção." "AWS" {
                tags "Amazon Web Services - AWS Cloud"
                region = deploymentNode "us-east-1" "Região onde o OrderFlow roda em produção." "Região AWS" {
                    tags "Amazon Web Services - Region"
                    apigw = infrastructureNode "API Gateway" "Roteamento e autenticação por API key; sem lógica custom." "Amazon API Gateway" {
                        tags "Amazon Web Services - API Gateway"
                    }
                    lambda = deploymentNode "AWS Lambda" "Serviço gerenciado que executa as funções." "AWS Lambda" {
                        tags "Amazon Web Services - Lambda"
                        createOrder = instanceOf orderflow.createOrder
                        listOrders = instanceOf orderflow.listOrders
                        paymentWebhook = instanceOf orderflow.paymentWebhook
                    }
                    dynamodb = deploymentNode "Amazon DynamoDB" "Serviço gerenciado que hospeda a tabela orders." "Amazon DynamoDB" {
                        tags "Amazon Web Services - DynamoDB"
                        instanceOf orderflow.orders
                    }
                }
            }

            stripeCloud = deploymentNode "Stripe" "Infraestrutura do Stripe." {
                instanceOf stripe
            }

            aws.region.apigw -> aws.region.lambda.createOrder "Roteia requisições para" "Invocação Lambda"
            aws.region.apigw -> aws.region.lambda.listOrders "Roteia requisições para" "Invocação Lambda"

            // O webhook do Stripe entra pelo API Gateway, não direto na Lambda.
            stripe -/> orderflow.paymentWebhook {
                stripe -> aws.region.apigw "Envia eventos de pagamento para" "Webhook JSON/HTTPS"
                aws.region.apigw -> orderflow.paymentWebhook "Roteia o webhook para" "Invocação Lambda"
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
