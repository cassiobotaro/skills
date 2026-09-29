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
            aws = deploymentNode "Amazon Web Services" "Conta AWS de produção." "AWS" {
                tags "Amazon Web Services - AWS Cloud"

                alb = infrastructureNode "Application Load Balancer" "Distribui as requisições entre as instâncias da API." "AWS Application Load Balancer" {
                    tags "Amazon Web Services - Load Balancing"
                }

                ecs = deploymentNode "Amazon ECS" "Cluster ECS que executa os serviços do sistema." "AWS Fargate" {
                    tags "Amazon Web Services - Elastic Container Service"

                    deploymentNode "Task do Portal" "Serviço ECS do portal." "Docker Container" {
                        instanceOf faturamento.portal
                    }
                    deploymentNode "Task da API" "Serviço ECS da API." "Docker Container" {
                        instances 2
                        instanceOf faturamento.api
                    }
                    deploymentNode "Task do Worker" "Serviço ECS do worker." "Docker Container" {
                        instanceOf faturamento.worker
                    }
                }

                rds = deploymentNode "Amazon RDS" "Banco de dados gerenciado." "AWS RDS" {
                    tags "Amazon Web Services - RDS"

                    deploymentNode "PostgreSQL" "Instância PostgreSQL do RDS." "PostgreSQL" {
                        instanceOf faturamento.banco
                    }
                }
            }

            faturamento.portal -/> faturamento.api {
                faturamento.portal -> aws.alb "Chama" "JSON/HTTPS"
                aws.alb -> faturamento.api "Encaminha requisições para" "JSON/HTTPS"
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

        dynamic faturamento "EmissaoFatura" {
            title "Emissão de fatura"
            atendente -> faturamento.portal "Emite a fatura em"
            faturamento.portal -> faturamento.api "Envia a fatura emitida para"
            faturamento.api -> faturamento.banco "Grava a fatura em"
            faturamento.api -> faturamento.fila "Publica a fatura emitida em"
            faturamento.worker -> faturamento.fila "Consome a fatura de"
            faturamento.worker -> erp "Envia a fatura para"
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
            element "Infrastructure Node" {
                shape ellipse
            }
        }

        theme amazon-web-services-2025.07
    }
}
