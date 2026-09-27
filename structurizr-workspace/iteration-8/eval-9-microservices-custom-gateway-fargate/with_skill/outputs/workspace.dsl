workspace "Mercadin" "Loja online Mercadin: contexto, containers e deployment de produção." {

    !identifiers hierarchical

    model {
        cliente = person "Cliente" "Compra na loja online Mercadin pelo app mobile."

        mercadin = softwareSystem "Mercadin" "Loja online: catálogo de produtos, pedidos e pagamentos dos clientes." {
            app = container "App Mobile" "App dos clientes. Fala apenas com o BFF." "React Native" {
                tags "Mobile"
            }
            bff = container "BFF" "Agrega respostas dos três microsserviços, aplica regras de autorização por perfil de cliente e monta o payload para o app." "Node.js"

            group "Serviço de Catálogo" {
                catalogoApi = container "Catálogo API" "Microsserviço de catálogo de produtos." "Java / Spring Boot"
                catalogoDb = container "Schema catalogo" "Schema do serviço de catálogo no Postgres." "PostgreSQL" {
                    tags "Database"
                }
                catalogoApi -> catalogoDb "Lê e grava em" "JDBC"
            }

            group "Serviço de Pedidos" {
                pedidosApi = container "Pedidos API" "Microsserviço de pedidos." "Java / Spring Boot"
                pedidosDb = container "Schema pedidos" "Schema do serviço de pedidos no Postgres." "PostgreSQL" {
                    tags "Database"
                }
                pedidosApi -> pedidosDb "Lê e grava em" "JDBC"
            }

            group "Serviço de Pagamentos" {
                pagamentosApi = container "Pagamentos API" "Microsserviço de pagamentos; integra com a Adyen." "Java / Spring Boot"
                pagamentosDb = container "Schema pagamentos" "Schema do serviço de pagamentos no Postgres." "PostgreSQL" {
                    tags "Database"
                }
                pagamentosApi -> pagamentosDb "Lê e grava em" "JDBC"
            }
        }

        adyen = softwareSystem "Adyen" "Provedor de pagamentos (terceiro)." {
            tags "External"
        }

        cliente -> mercadin.app "Compra na loja usando"
        mercadin.app -> mercadin.bff "Faz chamadas de API para" "HTTPS"
        mercadin.bff -> mercadin.catalogoApi "Consulta e agrega respostas de"
        mercadin.bff -> mercadin.pedidosApi "Consulta e agrega respostas de"
        mercadin.bff -> mercadin.pagamentosApi "Consulta e agrega respostas de"
        mercadin.pagamentosApi -> adyen "Processa pagamentos via" "HTTPS"

        producao = deploymentEnvironment "Produção" {
            deploymentNode "Dispositivo do cliente" "Smartphone do cliente." "iOS / Android" {
                instanceOf mercadin.app
            }

            aws = deploymentNode "Amazon Web Services" "" "AWS" {
                tags "Amazon Web Services - Cloud"

                alb = infrastructureNode "ALB" "Recebe o tráfego do app e encaminha para o BFF." "Application Load Balancer" {
                    tags "Amazon Web Services - Elastic Load Balancing"
                }

                ecs = deploymentNode "Amazon ECS" "Cluster ECS onde rodam o BFF e os três microsserviços." "AWS Fargate" {
                    tags "Amazon Web Services - Elastic Container Service"

                    deploymentNode "Task do BFF" "" "Docker Container" {
                        instanceOf mercadin.bff
                    }
                    deploymentNode "Task do Catálogo" "" "Docker Container" {
                        instanceOf mercadin.catalogoApi
                    }
                    deploymentNode "Task de Pedidos" "" "Docker Container" {
                        instanceOf mercadin.pedidosApi
                    }
                    deploymentNode "Task de Pagamentos" "" "Docker Container" {
                        instanceOf mercadin.pagamentosApi
                    }
                }

                deploymentNode "PostgreSQL" "Instância Postgres com os três schemas. Hospedagem (RDS, Aurora, ...) a confirmar." "PostgreSQL" {
                    instanceOf mercadin.catalogoDb
                    instanceOf mercadin.pedidosDb
                    instanceOf mercadin.pagamentosDb
                }
            }

            mercadin.app -/> mercadin.bff {
                mercadin.app -> aws.alb "Faz chamadas de API para" "HTTPS"
                aws.alb -> mercadin.bff "Encaminha requisições para"
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
                shape MobileDevicePortrait
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
