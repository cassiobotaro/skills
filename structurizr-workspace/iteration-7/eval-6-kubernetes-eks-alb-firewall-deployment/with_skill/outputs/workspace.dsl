workspace "Agenda+" "Sistema de agendamento de consultas." {

    !identifiers hierarchical

    model {
        paciente = person "Paciente" "Pessoa que agenda consultas pelo Agenda+."

        agenda = softwareSystem "Agenda+" "Permite que pacientes agendem consultas." {
            spa = container "SPA" "Interface web usada pelos pacientes para agendar consultas." "React" {
                tags "WebBrowser"
            }
            api = container "API" "Expõe as operações de agendamento de consultas." "Kotlin, Spring Boot"
            db = container "Banco de Dados" "Armazena os dados de agendamento de consultas." "PostgreSQL" {
                tags "Database"
            }
        }

        paciente -> agenda.spa "Agenda consultas usando" "HTTPS"
        agenda.spa -> agenda.api "Faz chamadas de API para" "JSON/HTTPS"
        agenda.api -> agenda.db "Lê e grava dados de agendamento em" "SQL/TCP"

        producao = deploymentEnvironment "Produção" {
            deploymentNode "Computador do Paciente" "" "" {
                deploymentNode "Navegador Web" "" "" {
                    instanceOf agenda.spa
                }
            }

            aws = deploymentNode "Amazon Web Services" "" "AWS" {
                tags "Amazon Web Services - AWS Cloud"

                waf = infrastructureNode "AWS WAF" "Firewall de aplicação web na frente do ALB." "AWS WAF" {
                    tags "Amazon Web Services - WAF"
                }

                alb = infrastructureNode "Application Load Balancer" "Distribui as requisições para os pods da API." "AWS Application Load Balancer" {
                    tags "Amazon Web Services - Load Balancing"
                }

                eks = deploymentNode "plataforma" "Cluster Kubernetes onde a API roda." "Amazon EKS" {
                    tags "Amazon Web Services - Elastic Kubernetes Service"

                    pod = deploymentNode "Pod da API" "" "Kubernetes Pod" {
                        tags "Kubernetes - pod"
                        instances 3
                        instanceOf agenda.api
                    }
                }

                rds = deploymentNode "Amazon RDS" "" "Amazon RDS" {
                    tags "Amazon Web Services - RDS"

                    deploymentNode "PostgreSQL" "" "PostgreSQL" {
                        instanceOf agenda.db
                    }
                }
            }

            agenda.spa -/> agenda.api {
                agenda.spa -> aws.waf "Faz chamadas de API para" "JSON/HTTPS"
                aws.waf -> aws.alb "Encaminha o tráfego filtrado para" "HTTPS"
                aws.alb -> agenda.api "Distribui as requisições para" "JSON/HTTPS"
            }
        }
    }

    views {
        systemContext agenda "SystemContext" {
            include *
            autoLayout
        }

        container agenda "Containers" {
            include *
            autoLayout
        }

        deployment agenda producao "Deployment-Producao" {
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
            element "WebBrowser" {
                shape webbrowser
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
        theme kubernetes
    }

    configuration {
        scope softwaresystem
    }
}
