workspace "Encurtaí" "Encurtador de URLs interno da empresa." {

    !identifiers hierarchical

    model {
        usuario = person "Usuário" "Funcionário da empresa que encurta e acessa links."

        encurtai = softwareSystem "Encurtaí" "Encurtador de URLs interno: cria links curtos e os redireciona." {
            spa = container "SPA" "Interface web para criar e gerenciar links curtos." "React (servido por nginx)"
            api = container "API" "Cria e resolve links, publica eventos de clique e autentica usuários." "Go (Gin)"
            db = container "Banco de Dados" "Armazena links e métricas agregadas de clique." "PostgreSQL 16" {
                tags "Database"
            }
            cache = container "Cache" "Cache de redirecionamentos para resolver links curtos rapidamente." "Redis 7" {
                tags "Database"
            }
            fila = container "Fila de Eventos de Clique" "Buffer dos eventos de clique entre API e worker." "RabbitMQ" {
                tags "Queue"
            }
            worker = container "Worker de Métricas" "Consome eventos de clique e grava métricas agregadas." "Go"

            spa -> api "Faz chamadas à API REST" "HTTPS/JSON"
            api -> cache "Lê e grava redirecionamentos no" "Redis protocol"
            api -> db "Lê e grava links no" "SQL/TCP"
            api -> fila "Publica eventos de clique na" "AMQP"
            fila -> worker "Entrega eventos de clique ao" "AMQP"
            worker -> db "Grava métricas agregadas no" "SQL/TCP"
        }

        googleWorkspace = softwareSystem "Google Workspace" "Provedor de identidade para autenticação SSO." {
            tags "External"
        }

        usuario -> encurtai.spa "Cria e acessa links curtos usando" "HTTPS"
        encurtai.api -> googleWorkspace "Autentica usuários via SSO usando" "HTTPS/OIDC"
    }

    views {
        systemContext encurtai "SystemContext" {
            include *
            autoLayout lr
        }

        container encurtai "Containers" {
            include *
            autoLayout lr
        }

        dynamic encurtai "RedirectFlow" "Fluxo de redirecionamento ao acessar um link curto." {
            title "Redirecionamento de link curto"
            usuario -> encurtai.spa "Acessa o link curto"
            encurtai.spa -> encurtai.api "Encaminha a resolução do link para"
            encurtai.api -> encurtai.cache "Consulta o redirecionamento no"
            encurtai.api -> encurtai.db "Em caso de cache miss, busca o link no"
            encurtai.api -> encurtai.fila "Publica o evento de clique na"
            autoLayout lr
        }

        styles {
            element "Element" {
                background #1168bd
                color #ffffff
            }
            element "Person" {
                shape person
                background #08427b
                color #ffffff
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
