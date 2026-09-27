workspace "OrderFlow" "API serverless de pedidos: três funções Lambda em Python sobre uma tabela DynamoDB, expostas pelo Amazon API Gateway." {

    !identifiers hierarchical

    model {
        cliente = person "Cliente" "Faz e acompanha pedidos pelo app mobile."

        // Fronteira: OrderFlow é a API serverless de pedidos (as três Lambdas + a tabela).
        // O app mobile foi modelado como um sistema à parte, que consome a API — ver nota na resposta.
        app = softwareSystem "App Mobile" "App dos clientes (Flutter) para criar e consultar pedidos; consome a API do OrderFlow."

        orderflow = softwareSystem "OrderFlow" "API serverless de pedidos: cria e lista pedidos e recebe as confirmações de pagamento." {
            criarPedido = container "criar-pedido" "Cria um novo pedido." "AWS Lambda, Python" {
                tags "Lambda"
            }
            listarPedidos = container "listar-pedidos" "Lista os pedidos existentes." "AWS Lambda, Python" {
                tags "Lambda"
            }
            webhookPagamento = container "webhook-pagamento" "Recebe os eventos de pagamento enviados pelo Stripe e atualiza o pedido correspondente." "AWS Lambda, Python" {
                tags "Lambda"
            }
            orders = container "orders" "Tabela que armazena os pedidos." "Amazon DynamoDB" {
                tags "Database"
            }
        }

        stripe = softwareSystem "Stripe" "Plataforma de pagamentos (terceiro); chama o webhook de pagamento do OrderFlow." {
            tags "External"
        }

        cliente -> app "Faz e acompanha pedidos usando"
        app -> orderflow.criarPedido "Cria pedidos chamando" "JSON/HTTPS"
        app -> orderflow.listarPedidos "Consulta pedidos chamando" "JSON/HTTPS"
        stripe -> orderflow.webhookPagamento "Envia eventos de pagamento para" "JSON/HTTPS (webhook)"

        orderflow.criarPedido -> orderflow.orders "Lê e grava pedidos em" "AWS SDK/HTTPS"
        orderflow.listarPedidos -> orderflow.orders "Lê e grava pedidos em" "AWS SDK/HTTPS"
        orderflow.webhookPagamento -> orderflow.orders "Lê e grava pedidos em" "AWS SDK/HTTPS"

        // ---------------------------------------------------------------
        // Desenvolvimento: cada dev roda tudo no laptop com LocalStack.
        // ---------------------------------------------------------------
        dev = deploymentEnvironment "Desenvolvimento" {
            laptop = deploymentNode "Laptop do desenvolvedor" "Ambiente local de cada dev." {
                localstack = deploymentNode "LocalStack" "Emulação local dos serviços AWS usados pelo OrderFlow." "LocalStack" {
                    apigw = infrastructureNode "API Gateway (emulado)" "Roteamento e autenticação por API key, emulados pelo LocalStack." "Amazon API Gateway (LocalStack)" {
                        tags "Amazon Web Services - API Gateway"
                    }
                    deploymentNode "Lambda (emulado)" "Execução local das funções." "AWS Lambda (LocalStack)" {
                        tags "Amazon Web Services - Lambda"
                        instanceOf orderflow.criarPedido
                        instanceOf orderflow.listarPedidos
                        instanceOf orderflow.webhookPagamento
                    }
                    deploymentNode "DynamoDB (emulado)" "Tabela local." "Amazon DynamoDB (LocalStack)" {
                        tags "Amazon Web Services - DynamoDB"
                        instanceOf orderflow.orders
                    }
                }
            }

            laptop.localstack.apigw -> orderflow.criarPedido "Encaminha requisições para" "JSON/HTTPS"
            laptop.localstack.apigw -> orderflow.listarPedidos "Encaminha requisições para" "JSON/HTTPS"
            laptop.localstack.apigw -> orderflow.webhookPagamento "Encaminha requisições para" "JSON/HTTPS"
        }

        // ---------------------------------------------------------------
        // Produção: AWS, us-east-1.
        // ---------------------------------------------------------------
        producao = deploymentEnvironment "Produção" {
            smartphone = deploymentNode "Smartphone do cliente" "Dispositivo do cliente com o app instalado." {
                instanceOf app
            }

            stripeCloud = deploymentNode "Stripe" "Infraestrutura do Stripe (terceiro)." {
                tags "External"
                instanceOf stripe
            }

            aws = deploymentNode "Amazon Web Services" "" "AWS" {
                tags "Amazon Web Services - AWS Cloud"
                regiao = deploymentNode "us-east-1" "" "Região AWS" {
                    tags "Amazon Web Services - Region"
                    apigw = infrastructureNode "Amazon API Gateway" "Roteamento e autenticação por API key; sem lógica customizada." "Amazon API Gateway" {
                        tags "Amazon Web Services - API Gateway"
                    }
                    deploymentNode "AWS Lambda" "Execução das funções." "AWS Lambda" {
                        tags "Amazon Web Services - Lambda"
                        instanceOf orderflow.criarPedido
                        instanceOf orderflow.listarPedidos
                        instanceOf orderflow.webhookPagamento
                    }
                    deploymentNode "Amazon DynamoDB" "Serviço gerenciado que hospeda a tabela." "Amazon DynamoDB" {
                        tags "Amazon Web Services - DynamoDB"
                        instanceOf orderflow.orders
                    }
                }
            }

            // As chamadas passam pelo API Gateway; o gateway não é um container, é infraestrutura.
            app -/> orderflow.criarPedido {
                app -> aws.regiao.apigw "Chama a API do OrderFlow via" "JSON/HTTPS"
                aws.regiao.apigw -> orderflow.criarPedido "Encaminha requisições para" "JSON/HTTPS"
            }
            app -/> orderflow.listarPedidos {
                aws.regiao.apigw -> orderflow.listarPedidos "Encaminha requisições para" "JSON/HTTPS"
            }
            stripe -/> orderflow.webhookPagamento {
                stripe -> aws.regiao.apigw "Envia eventos de pagamento para" "JSON/HTTPS (webhook)"
                aws.regiao.apigw -> orderflow.webhookPagamento "Encaminha requisições para" "JSON/HTTPS"
            }
        }
    }

    views {
        systemContext orderflow "SystemContext" "Quem usa o OrderFlow e com quais sistemas ele conversa." {
            include *
            autoLayout lr
        }

        container orderflow "Containers" "As funções Lambda e a tabela DynamoDB que formam o OrderFlow." {
            include *
            autoLayout lr
        }

        deployment orderflow dev "Deployment-Dev" "Ambiente local de desenvolvimento (LocalStack no laptop)." {
            include *
            autoLayout lr
        }

        deployment orderflow producao "Deployment-Producao" "Produção na AWS, us-east-1." {
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
