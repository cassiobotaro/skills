workspace "Encurtaí" "Encurtador de URLs interno da empresa." {

    !identifiers hierarchical

    model {
        colaborador = person "Colaborador" "Funcionário da empresa que encurta links e acessa links curtos."

        encurtai = softwareSystem "Encurtaí" "Encurta URLs internas e registra métricas de cliques." {
            spa = container "SPA" "Interface web para criar e consultar links curtos." "React (servido por nginx)"
            api = container "API" "Cria links, resolve redirecionamentos e publica eventos de clique." "Go (Gin)"
            worker = container "Worker de Métricas" "Consome eventos de clique e grava métricas agregadas." "Go"
            banco = container "Banco de Dados" "Armazena os links e as métricas agregadas de clique." "PostgreSQL 16" {
                tags "Database"
            }
            cache = container "Cache" "Guarda os redirecionamentos mais acessados." "Redis 7" {
                tags "Database"
            }
            fila = container "Fila de Eventos de Clique" "Transporta os eventos de clique da API até o worker." "RabbitMQ" {
                tags "Queue"
            }
        }

        googleWorkspace = softwareSystem "Google Workspace" "Provedor de identidade corporativo usado para SSO." {
            tags "External"
        }

        colaborador -> encurtai.spa "Cria e consulta links curtos usando" "HTTPS"
        colaborador -> encurtai.api "Acessa links curtos em" "HTTPS"

        encurtai.spa -> encurtai.api "Faz chamadas REST para" "JSON/HTTPS"
        encurtai.api -> encurtai.cache "Lê e grava redirecionamentos em cache no" "RESP/TCP"
        encurtai.api -> encurtai.banco "Lê e grava links no" "SQL/TCP"
        encurtai.api -> encurtai.fila "Publica eventos de clique na" "AMQP"
        encurtai.api -> googleWorkspace "Autentica usuários por SSO usando" "HTTPS"

        encurtai.worker -> encurtai.fila "Consome eventos de clique da" "AMQP"
        encurtai.worker -> encurtai.banco "Grava métricas agregadas no" "SQL/TCP"
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
            colaborador -> encurtai.api "Acessa o link curto"
            encurtai.api -> encurtai.cache "Consulta o destino no cache"
            encurtai.api -> encurtai.banco "Em caso de miss no cache, busca o link"
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
