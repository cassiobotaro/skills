workspace "Encurtaí" "Encurtador de URLs interno da empresa." {

    !identifiers hierarchical

    model {
        funcionario = person "Funcionário" "Usa links curtos internos e gerencia os seus próprios links."

        encurtai = softwareSystem "Encurtaí" "Encurtador de URLs interno: cria, gerencia e redireciona links curtos." {
            spa = container "SPA" "Interface web para criar e gerenciar links curtos." "React (servido por nginx)" {
                tags "Browser"
            }
            api = container "API" "Cria, lê e redireciona links curtos; publica eventos de clique." "Go (Gin)"
            db = container "Banco de Dados" "Armazena os links e as métricas agregadas de clique." "PostgreSQL 16" {
                tags "Database"
            }
            cache = container "Cache" "Cache de redirecionamentos de links curtos." "Redis 7" {
                tags "Database"
            }
            fila = container "Fila de Eventos de Clique" "Buffer dos eventos de clique a serem agregados." "RabbitMQ" {
                tags "Queue"
            }
            worker = container "Worker de Métricas" "Consome eventos de clique e grava métricas agregadas." "Go"

            spa -> api "Faz chamadas a" "JSON/HTTPS"
            api -> cache "Lê e grava redirecionamentos em" "RESP/TCP"
            api -> db "Lê e grava links em" "SQL/TCP"
            api -> fila "Publica eventos de clique em" "AMQP"
            fila -> worker "Entrega eventos de clique para" "AMQP"
            worker -> db "Grava métricas agregadas em" "SQL/TCP"
        }

        googleWorkspace = softwareSystem "Google Workspace" "Provedor de identidade para autenticação SSO dos usuários." {
            tags "External"
        }

        funcionario -> encurtai.spa "Cria e gerencia links usando" "HTTPS"
        funcionario -> encurtai.api "Acessa links curtos em" "HTTPS"
        encurtai.api -> googleWorkspace "Autentica usuários via SSO usando" "OIDC/HTTPS"
    }

    views {
        systemContext encurtai "SystemContext" {
            include *
            autoLayout
        }

        container encurtai "Containers" {
            include *
            autoLayout
        }

        dynamic encurtai "Redirecionamento" "Fluxo de redirecionamento de um link curto." {
            funcionario -> encurtai.api "Acessa um link curto em"
            encurtai.api -> encurtai.cache "Consulta o redirecionamento no"
            encurtai.api -> encurtai.db "Em caso de miss no cache, busca o link no"
            encurtai.api -> encurtai.fila "Publica o evento de clique em"
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
            element "Browser" {
                shape WebBrowser
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

    configuration {
        scope softwaresystem
    }
}
