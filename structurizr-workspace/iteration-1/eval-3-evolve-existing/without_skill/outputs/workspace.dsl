workspace "Faturamento" "Sistema de faturamento da empresa." {

    !identifiers hierarchical

    model {
        atendente = person "Atendente" "Equipe financeira que emite e acompanha faturas."

        faturamento = softwareSystem "Faturamento" "Emite, processa e concilia faturas." {
            portal = container "Portal Web" "Interface para emissão e acompanhamento de faturas." "React"
            api = container "API de Faturamento" "Regras de negócio e orquestração de faturas." "Go"
            worker = container "Worker de Processamento" "Processa faturas de forma assíncrona." "Go"
            fila = container "Fila de Faturas" "Buffer de faturas a processar." "RabbitMQ" {
                tags "Queue"
            }
            banco = container "Banco de Dados" "Armazena faturas, clientes e itens." "PostgreSQL" {
                tags "Database"
            }
        }

        erp = softwareSystem "ERP" "Sistema corporativo de gestão (mantido por terceiro)." {
            tags "External"
        }

        atendente -> faturamento.portal "Emite e consulta faturas usando"
        faturamento.portal -> faturamento.api "Chama" "JSON/HTTPS"
        faturamento.api -> faturamento.banco "Lê e grava dados em" "SQL/TCP"
        faturamento.api -> faturamento.fila "Publica faturas emitidas em"
        faturamento.worker -> faturamento.fila "Consome faturas de"
        faturamento.worker -> faturamento.banco "Atualiza status em" "SQL/TCP"
        faturamento.worker -> erp "Envia faturas processadas para" "HTTPS"

        producao = deploymentEnvironment "Produção" {
            aws = deploymentNode "Amazon Web Services" "" "AWS" {
                regiao = deploymentNode "us-east-1" "" "AWS Region" {

                    portalNode = deploymentNode "ECS Fargate (Portal)" "Serviço gerenciado de contêineres." "Amazon ECS / Fargate" {
                        portalInstance = containerInstance faturamento.portal
                    }

                    alb = infrastructureNode "Application Load Balancer" "Balanceia o tráfego HTTPS para a API." "Elastic Load Balancing"

                    apiNode = deploymentNode "ECS Fargate (API)" "Serviço gerenciado de contêineres (2 instâncias)." "Amazon ECS / Fargate" "" 2 {
                        apiInstance = containerInstance faturamento.api
                    }

                    workerNode = deploymentNode "ECS Fargate (Worker)" "Serviço gerenciado de contêineres." "Amazon ECS / Fargate" {
                        workerInstance = containerInstance faturamento.worker
                    }

                    filaNode = deploymentNode "Amazon MQ (RabbitMQ)" "Broker de mensageria gerenciado." "Amazon MQ" {
                        filaInstance = containerInstance faturamento.fila
                    }

                    rds = deploymentNode "Amazon RDS" "Banco de dados relacional gerenciado." "Amazon RDS" {
                        bancoNode = deploymentNode "PostgreSQL" "" "PostgreSQL" {
                            bancoInstance = containerInstance faturamento.banco
                        }
                    }

                    portalInstance -> alb "Encaminha chamadas via" "JSON/HTTPS"
                    alb -> apiInstance "Encaminha requisições para" "JSON/HTTPS"
                }
            }
        }
    }

    views {
        systemContext faturamento "Contexto" {
            include *
            autoLayout
        }

        container faturamento "Containers" {
            include *
            autoLayout
        }

        dynamic faturamento "EmissaoDeFatura" "Fluxo de emissão de uma fatura." {
            atendente -> faturamento.portal "Emite a fatura pelo"
            faturamento.portal -> faturamento.api "Envia a solicitação de emissão para"
            faturamento.api -> faturamento.banco "Grava a fatura em"
            faturamento.api -> faturamento.fila "Publica a fatura emitida em"
            faturamento.worker -> faturamento.fila "Consome a fatura de"
            faturamento.worker -> erp "Envia a fatura para o"
            autoLayout
        }

        deployment faturamento producao "Producao" "Implantação de produção na AWS." {
            include *
            autoLayout
        }

        styles {
            element "Person" {
                shape person
            }
            element "Database" {
                shape cylinder
            }
            element "Queue" {
                shape pipe
            }
            element "External" {
                background #999999
                color #ffffff
            }
        }
    }

    !adrs docs/adr
}
