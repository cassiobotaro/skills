workspace "Encurtaí" "Encurtador de URLs interno da empresa." {

    !identifiers hierarchical

    model {
        usuario = person "Usuário da empresa" "Funcionário que encurta links e acessa links curtos."

        encurtai = softwareSystem "Encurtaí" "Encurta URLs internas e redireciona os acessos aos links curtos, registrando métricas de clique." {
            spa = container "SPA" "Interface web para criar e consultar links curtos." "React (servido por nginx)"

            api = container "API" "Cria e resolve links curtos, publica eventos de clique e autentica os usuários." "Go (Gin)"

            worker = container "Worker de Métricas" "Consome eventos de clique e grava métricas agregadas." "Go"

            bancoDeDados = container "Banco de Dados" "Armazena os links curtos e as métricas agregadas de clique." "PostgreSQL 16" {
                tags "Database"
            }

            cache = container "Cache de Redirecionamentos" "Mantém em cache o destino dos links curtos." "Redis 7" {
                tags "Database"
            }

            filaDeCliques = container "Fila de Eventos de Clique" "Enfileira os eventos de clique publicados pela API." "RabbitMQ" {
                tags "Queue"
            }
        }

        googleWorkspace = softwareSystem "Google Workspace" "Provedor de identidade corporativo usado para o SSO." {
            tags "External"
        }

        usuario -> encurtai.spa "Cria e consulta links curtos em" "HTTPS"
        usuario -> encurtai.api "Acessa links curtos em" "HTTPS"

        encurtai.spa -> encurtai.api "Faz chamadas REST para" "JSON/HTTPS"

        encurtai.api -> encurtai.bancoDeDados "Lê e grava links em" "SQL/TCP"
        encurtai.api -> encurtai.cache "Lê e grava redirecionamentos em" "RESP/TCP"
        encurtai.api -> encurtai.filaDeCliques "Publica eventos de clique em" "AMQP"
        encurtai.api -> googleWorkspace "Autentica usuários via SSO usando" "HTTPS"

        encurtai.filaDeCliques -> encurtai.worker "Entrega eventos de clique para" "AMQP"
        encurtai.worker -> encurtai.bancoDeDados "Grava métricas agregadas em" "SQL/TCP"
    }

    views {
        systemContext encurtai "SystemContext" "Diagrama de contexto do Encurtaí." {
            include *
            autoLayout
        }

        container encurtai "Containers" "Diagrama de containers do Encurtaí." {
            include *
            autoLayout
        }

        dynamic encurtai "RedirecionamentoDeLink" "Fluxo de redirecionamento de um link curto." {
            usuario -> encurtai.api "Acessa um link curto"
            encurtai.api -> encurtai.cache "Consulta o destino do link no"
            encurtai.api -> encurtai.bancoDeDados "Em caso de cache miss, busca o link no"
            encurtai.api -> encurtai.filaDeCliques "Publica o evento de clique na"
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
                background #2d6a4f
                color #ffffff
            }
            element "Queue" {
                shape pipe
                background #b5651d
                color #ffffff
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
