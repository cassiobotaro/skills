workspace "Faturamento" "Sistema de faturamento da empresa." {

    !identifiers hierarchical

    !adrs docs/adr

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
            aws = deploymentNode "Amazon Web Services" {
                tags "Amazon Web Services - Cloud"
                region = deploymentNode "sa-east-1" {
                    tags "Amazon Web Services - Region"

                    alb = infrastructureNode "Application Load Balancer" "Distribui requisições para a API." "AWS Application Load Balancer" {
                        tags "Amazon Web Services - Elastic Load Balancing"
                    }

                    deploymentNode "ECS Fargate - Portal" "" "AWS ECS Fargate" {
                        deploymentNode "Tarefa do Portal" "" "Docker Container" {
                            instanceOf faturamento.portal
                        }
                    }

                    deploymentNode "ECS Fargate - API" "" "AWS ECS Fargate" {
                        deploymentNode "Tarefa da API" "" "Docker Container" {
                            instances 2
                            instanceOf faturamento.api
                        }
                    }

                    deploymentNode "ECS Fargate - Worker" "" "AWS ECS Fargate" {
                        deploymentNode "Tarefa do Worker" "" "Docker Container" {
                            instanceOf faturamento.worker
                        }
                    }

                    deploymentNode "Amazon RDS" "" "Amazon RDS" {
                        tags "Amazon Web Services - RDS"
                        deploymentNode "PostgreSQL" "" "Amazon RDS PostgreSQL" {
                            tags "Amazon Web Services - RDS PostgreSQL instance"
                            instanceOf faturamento.banco
                        }
                    }
                }
            }

            faturamento.portal -/> faturamento.api {
                faturamento.portal -> aws.region.alb "Chama" "JSON/HTTPS"
                aws.region.alb -> faturamento.api "Encaminha requisições para" "JSON/HTTPS"
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
            faturamento.portal -> faturamento.api "Chama"
            faturamento.api -> faturamento.banco "Grava a fatura em"
            faturamento.api -> faturamento.fila "Publica a fatura emitida em"
            faturamento.worker -> faturamento.fila "Consome a fatura de"
            faturamento.worker -> erp "Envia a fatura para o"
            autoLayout lr
        }

        deployment faturamento producao "Deployment-Producao" {
            include *
            autoLayout lr
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

        theme amazon-web-services-2025.07
    }
}
