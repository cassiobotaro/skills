workspace "OrderFlow" "API serverless de pedidos: funções Lambda em Python atrás do Amazon API Gateway, com persistência em DynamoDB." {

    !identifiers hierarchical

    model {
        cliente = person "Cliente" "Faz e consulta pedidos pelo app mobile."

        // O app mobile foi modelado como um sistema à parte porque o OrderFlow foi
        // descrito como "a API". Se o mesmo time é dono do app, mova-o para dentro
        // do OrderFlow como um container (veja a resposta que acompanha este arquivo).
        appMobile = softwareSystem "App Mobile" "Aplicativo dos clientes para fazer e consultar pedidos." {
            tags "Mobile App"
        }

        orderflow = softwareSystem "OrderFlow" "API serverless de pedidos." {
            criarPedido = container "criar-pedido" "Recebe um novo pedido e o registra." "Python, AWS Lambda" {
                tags "Lambda"
            }
            listarPedidos = container "listar-pedidos" "Retorna os pedidos existentes." "Python, AWS Lambda" {
                tags "Lambda"
            }
            webhookPagamento = container "webhook-pagamento" "Recebe as notificações de pagamento do Stripe e atualiza o pedido correspondente." "Python, AWS Lambda" {
                tags "Lambda"
            }
            orders = container "orders" "Tabela que armazena os pedidos." "Amazon DynamoDB" {
                tags "Database"
            }
        }

        stripe = softwareSystem "Stripe" "Provedor de pagamentos (SaaS)." {
            tags "External"
        }

        cliente -> appMobile "Faz e consulta pedidos usando"

        appMobile -> orderflow.criarPedido "Envia novos pedidos para" "HTTPS"
        appMobile -> orderflow.listarPedidos "Consulta os pedidos em" "HTTPS"
        stripe -> orderflow.webhookPagamento "Notifica eventos de pagamento para" "HTTPS"

        orderflow.criarPedido -> orderflow.orders "Lê e grava pedidos em" "AWS SDK"
        orderflow.listarPedidos -> orderflow.orders "Lê e grava pedidos em" "AWS SDK"
        orderflow.webhookPagamento -> orderflow.orders "Lê e grava pedidos em" "AWS SDK"

        // ---------------------------------------------------------------
        // Desenvolvimento: cada dev roda a stack inteira no laptop, com o
        // LocalStack emulando os serviços da AWS.
        // ---------------------------------------------------------------
        dev = deploymentEnvironment "Desenvolvimento" {
            laptop = deploymentNode "Laptop do desenvolvedor" "Máquina local de cada desenvolvedor." {
                localstack = deploymentNode "LocalStack" "Emula os serviços da AWS usados pelo OrderFlow." "LocalStack" {
                    apigw = infrastructureNode "API Gateway (emulado)" "Roteamento e autenticação por API key." "Amazon API Gateway (LocalStack)"
                    deploymentNode "Lambda (emulado)" "Runtime das funções." "AWS Lambda (LocalStack)" {
                        containerInstance orderflow.criarPedido
                        containerInstance orderflow.listarPedidos
                        containerInstance orderflow.webhookPagamento
                    }
                    deploymentNode "DynamoDB (emulado)" "Armazenamento local da tabela." "Amazon DynamoDB (LocalStack)" {
                        containerInstance orderflow.orders
                    }
                }
            }

            laptop.localstack.apigw -> orderflow.criarPedido "Encaminha requisições para" "HTTPS"
            laptop.localstack.apigw -> orderflow.listarPedidos "Encaminha requisições para" "HTTPS"
            laptop.localstack.apigw -> orderflow.webhookPagamento "Encaminha requisições para" "HTTPS"
        }

        // ---------------------------------------------------------------
        // Produção: AWS, região us-east-1.
        // ---------------------------------------------------------------
        prod = deploymentEnvironment "Produção" {
            celular = deploymentNode "Smartphone do cliente" "Dispositivo onde o app mobile roda." {
                softwareSystemInstance appMobile
            }

            stripeSaas = deploymentNode "Stripe" "Plataforma do provedor de pagamentos." "SaaS" {
                softwareSystemInstance stripe
            }

            aws = deploymentNode "Amazon Web Services" "" "AWS" {
                tags "Amazon Web Services - AWS Cloud"
                region = deploymentNode "us-east-1" "" "Região AWS" {
                    tags "Amazon Web Services - Region"

                    apigw = infrastructureNode "Amazon API Gateway" "Roteamento e autenticação por API key; sem lógica custom." "Amazon API Gateway" {
                        tags "Amazon Web Services - API Gateway"
                    }

                    deploymentNode "AWS Lambda" "Runtime das funções." "AWS Lambda" {
                        tags "Amazon Web Services - Lambda"
                        containerInstance orderflow.criarPedido
                        containerInstance orderflow.listarPedidos
                        containerInstance orderflow.webhookPagamento
                    }

                    deploymentNode "Amazon DynamoDB" "Serviço gerenciado de banco de dados." "Amazon DynamoDB" {
                        tags "Amazon Web Services - DynamoDB"
                        containerInstance orderflow.orders
                    }
                }
            }

            // As chamadas ao OrderFlow passam pelo API Gateway em produção.
            appMobile -/> orderflow.criarPedido {
                appMobile -> aws.region.apigw "Chama a API de pedidos em" "HTTPS"
                aws.region.apigw -> orderflow.criarPedido "Encaminha requisições para" "HTTPS"
            }
            appMobile -/> orderflow.listarPedidos {
                aws.region.apigw -> orderflow.listarPedidos "Encaminha requisições para" "HTTPS"
            }
            stripe -/> orderflow.webhookPagamento {
                stripe -> aws.region.apigw "Envia webhooks de pagamento para" "HTTPS"
                aws.region.apigw -> orderflow.webhookPagamento "Encaminha requisições para" "HTTPS"
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
            element "Mobile App" {
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
