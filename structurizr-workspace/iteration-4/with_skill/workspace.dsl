workspace "Encurtaí" "Encurtador de URLs interno da empresa." {

    !identifiers hierarchical

    model {
        usuario = person "Usuário da empresa" "Colaborador que encurta links e acessa links curtos."

        encurtai = softwareSystem "Encurtaí" "Encurta URLs internas, redireciona links curtos e registra métricas de clique." {

            spa = container "SPA" "Interface web onde o usuário cria e consulta seus links curtos." "React (servido por nginx)" {
                tags "Browser"
            }

            api = container "API" "Cria e consulta links, resolve redirecionamentos e publica eventos de clique." "Go (Gin)"

            worker = container "Worker de Métricas" "Consome eventos de clique e grava métricas agregadas." "Go"

            fila = container "Fila de Eventos de Clique" "Buffer dos eventos de clique entre a API e o worker." "RabbitMQ" {
                tags "Queue"
            }

            cache = container "Cache de Redirecionamentos" "Guarda o destino dos links curtos para responder redirecionamentos sem ir ao banco." "Redis 7" {
                tags "Database" "Cache"
            }

            banco = container "Banco de Dados" "Armazena os links curtos e as métricas agregadas de clique." "PostgreSQL 16" {
                tags "Database"
            }
        }

        googleWorkspace = softwareSystem "Google Workspace" "Provedor de identidade corporativo usado para o SSO dos usuários." {
            tags "External"
        }

        usuario -> encurtai.spa "Cria e consulta links curtos usando" "HTTPS"
        usuario -> encurtai.api "Acessa links curtos em" "HTTPS"

        encurtai.spa -> encurtai.api "Chama para criar e listar links" "JSON/HTTPS"
        encurtai.api -> encurtai.banco "Lê e grava links em" "SQL/TCP"
        encurtai.api -> encurtai.cache "Lê e grava destinos de redirecionamento em" "RESP/TCP"
        encurtai.api -> encurtai.fila "Publica eventos de clique em" "AMQP"
        encurtai.api -> googleWorkspace "Autentica os usuários via SSO em" "OAuth 2.0/HTTPS"

        encurtai.fila -> encurtai.worker "Entrega eventos de clique para" "AMQP"
        encurtai.worker -> encurtai.banco "Grava métricas agregadas em" "SQL/TCP"
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
            usuario -> encurtai.api "Acessa o link curto"
            encurtai.api -> encurtai.cache "Consulta o destino do link no cache"
            encurtai.api -> encurtai.banco "Busca o destino no banco (cache miss)"
            encurtai.api -> encurtai.fila "Publica o evento de clique"
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
                shape webbrowser
            }
            element "Database" {
                shape cylinder
            }
            element "Cache" {
                background #4b8fd1
            }
            element "Queue" {
                shape pipe
                background #7a5cb0
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
