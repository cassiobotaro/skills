workspace "Mercadin" "Loja online Mercadin: app mobile, BFF e microsserviços de catálogo, pedidos e pagamentos." {

    !identifiers hierarchical

    model {
        cliente = person "Cliente" "Compra produtos na loja online pelo app mobile."

        mercadin = softwareSystem "Mercadin" "Loja online: catálogo de produtos, pedidos e pagamentos dos clientes." {
            app = container "App Mobile" "Interface do cliente para navegar no catálogo, fazer pedidos e pagar." "React Native" {
                tags "Mobile"
            }

            bff = container "BFF" "Agrega as respostas dos três serviços, aplica regras de autorização por perfil de cliente e monta o payload para o app." "Node.js"

            group "Catálogo" {
                catalogoApi = container "Serviço de Catálogo" "Mantém os produtos e informações do catálogo." "Java / Spring Boot"
                catalogoDb = container "Schema Catálogo" "Dados do catálogo de produtos." "PostgreSQL (schema)" {
                    tags "Database"
                }
                catalogoApi -> catalogoDb "Lê e grava dados do catálogo em" "SQL/JDBC"
            }

            group "Pedidos" {
                pedidosApi = container "Serviço de Pedidos" "Gerencia o ciclo de vida dos pedidos dos clientes." "Java / Spring Boot"
                pedidosDb = container "Schema Pedidos" "Dados dos pedidos." "PostgreSQL (schema)" {
                    tags "Database"
                }
                pedidosApi -> pedidosDb "Lê e grava pedidos em" "SQL/JDBC"
            }

            group "Pagamentos" {
                pagamentosApi = container "Serviço de Pagamentos" "Processa os pagamentos dos pedidos por meio da Adyen." "Java / Spring Boot"
                pagamentosDb = container "Schema Pagamentos" "Dados de pagamentos e transações." "PostgreSQL (schema)" {
                    tags "Database"
                }
                pagamentosApi -> pagamentosDb "Lê e grava pagamentos em" "SQL/JDBC"
            }
        }

        adyen = softwareSystem "Adyen" "Provedor de pagamentos (PSP) que processa as cobranças." {
            tags "External"
        }

        cliente -> mercadin.app "Navega no catálogo, faz pedidos e paga usando"
        mercadin.app -> mercadin.bff "Consome a API agregada do app via" "JSON/HTTPS"
        mercadin.bff -> mercadin.catalogoApi "Consulta produtos do catálogo em" "JSON/HTTP"
        mercadin.bff -> mercadin.pedidosApi "Cria e consulta pedidos em" "JSON/HTTP"
        mercadin.bff -> mercadin.pagamentosApi "Solicita e consulta pagamentos em" "JSON/HTTP"
        mercadin.pagamentosApi -> adyen "Envia cobranças para" "HTTPS"

        producao = deploymentEnvironment "Produção" {
            deploymentNode "Smartphone do cliente" "" "iOS / Android" {
                instanceOf mercadin.app
            }

            aws = deploymentNode "Amazon Web Services" "" "AWS" {
                tags "Amazon Web Services - Cloud"

                alb = infrastructureNode "ALB" "Recebe o tráfego HTTPS e roteia para os serviços no ECS." "Application Load Balancer" {
                    tags "Amazon Web Services - Elastic Load Balancing"
                }

                ecs = deploymentNode "Amazon ECS" "" "AWS Fargate" {
                    tags "Amazon Web Services - Elastic Container Service"

                    deploymentNode "Task BFF" "" "Docker Container" {
                        instanceOf mercadin.bff
                    }
                    deploymentNode "Task Catálogo" "" "Docker Container" {
                        instanceOf mercadin.catalogoApi
                    }
                    deploymentNode "Task Pedidos" "" "Docker Container" {
                        instanceOf mercadin.pedidosApi
                    }
                    deploymentNode "Task Pagamentos" "" "Docker Container" {
                        instanceOf mercadin.pagamentosApi
                    }
                }

                deploymentNode "PostgreSQL" "Instância Postgres com um schema por serviço." "PostgreSQL" {
                    instanceOf mercadin.catalogoDb
                    instanceOf mercadin.pedidosDb
                    instanceOf mercadin.pagamentosDb
                }
            }

            mercadin.app -/> mercadin.bff {
                mercadin.app -> aws.alb "Consome a API agregada do app via" "JSON/HTTPS"
                aws.alb -> mercadin.bff "Encaminha as requisições do app para" "JSON/HTTP"
            }
            mercadin.bff -/> mercadin.catalogoApi {
                mercadin.bff -> aws.alb "Chama os serviços via" "JSON/HTTPS"
                aws.alb -> mercadin.catalogoApi "Encaminha as requisições de catálogo para" "JSON/HTTP"
            }
            mercadin.bff -/> mercadin.pedidosApi {
                aws.alb -> mercadin.pedidosApi "Encaminha as requisições de pedidos para" "JSON/HTTP"
            }
            mercadin.bff -/> mercadin.pagamentosApi {
                aws.alb -> mercadin.pagamentosApi "Encaminha as requisições de pagamentos para" "JSON/HTTP"
            }
        }
    }

    views {
        systemContext mercadin "SystemContext" {
            include *
            autoLayout
        }

        container mercadin "Containers" {
            include *
            autoLayout
        }

        deployment mercadin producao "Deployment-Producao" {
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
            element "Mobile" {
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
