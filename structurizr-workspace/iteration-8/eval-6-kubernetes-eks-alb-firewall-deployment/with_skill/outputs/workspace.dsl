workspace "Agenda+" "Sistema de agendamento de consultas." {

    !identifiers hierarchical

    model {
        paciente = person "Paciente" "Agenda e acompanha suas consultas."

        agenda = softwareSystem "Agenda+" "Permite que pacientes agendem consultas." {
            spa = container "SPA" "Interface web usada pelos pacientes para agendar consultas." "React" {
                tags "WebBrowser"
            }
            api = container "API" "Expõe as operações de agendamento e aplica as regras de negócio." "Kotlin, Spring Boot"
            db = container "Banco de Dados" "Armazena pacientes, agendas e consultas." "PostgreSQL" {
                tags "Database"
            }
        }

        paciente -> agenda.spa "Agenda consultas usando" "HTTPS"
        agenda.spa -> agenda.api "Faz chamadas de API para" "JSON/HTTPS"
        agenda.api -> agenda.db "Lê e grava dados em" "JDBC/SQL"

        producao = deploymentEnvironment "Produção" {
            deploymentNode "Computador do paciente" "" "" {
                deploymentNode "Navegador web" "" "" {
                    instanceOf agenda.spa
                }
            }

            aws = deploymentNode "Amazon Web Services" "" "" {
                tags "Amazon Web Services - Cloud"

                waf = infrastructureNode "Firewall" "Filtra o tráfego antes de chegar ao load balancer." "AWS WAF" {
                    tags "Amazon Web Services - WAF"
                }

                alb = infrastructureNode "Load Balancer" "Distribui as requisições entre as réplicas da API." "Application Load Balancer" {
                    tags "Amazon Web Services - Elastic Load Balancing"
                }

                eks = deploymentNode "Elastic Kubernetes Service" "" "Amazon EKS" {
                    tags "Amazon Web Services - Elastic Kubernetes Service"
                    cluster = deploymentNode "plataforma" "" "Kubernetes Cluster" {
                        pod = deploymentNode "Pod da API" "" "Kubernetes Pod" {
                            instances 3
                            deploymentNode "Contêiner da API" "" "Docker Container" {
                                instanceOf agenda.api
                            }
                        }
                    }
                }

                rds = deploymentNode "Amazon RDS" "" "" {
                    tags "Amazon Web Services - RDS"
                    deploymentNode "PostgreSQL" "" "RDS for PostgreSQL" {
                        instanceOf agenda.db
                    }
                }
            }

            agenda.spa -/> agenda.api {
                agenda.spa -> aws.waf "Faz chamadas de API para" "JSON/HTTPS"
                aws.waf -> aws.alb "Encaminha o tráfego permitido para" "JSON/HTTPS"
                aws.alb -> agenda.api "Encaminha as requisições para" "JSON/HTTPS"
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
