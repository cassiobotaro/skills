workspace "Encurtaí" "Encurtador de URLs interno da empresa." {

    !identifiers hierarchical

    model {
        usuario = person "Usuário interno" "Colaborador da empresa que cria links curtos e acessa links encurtados."

        encurtai = softwareSystem "Encurtaí" "Encurta URLs para uso interno, redireciona acessos a links curtos e agrega métricas de cliques." {
            spa = container "Aplicação Web" "SPA para criar e gerenciar links curtos." "React, servido por nginx" {
                tags "WebBrowser"
            }
            api = container "API" "API REST que gerencia links, resolve redirecionamentos, autentica usuários via SSO e publica eventos de clique." "Go (Gin)"
            worker = container "Worker de Métricas" "Consome eventos de clique da fila e grava métricas agregadas." "Go"
            db = container "Banco de Dados" "Armazena os links e as métricas agregadas de cliques." "PostgreSQL 16" {
                tags "Database"
            }
            cache = container "Cache de Redirecionamentos" "Cache dos destinos dos links curtos para acelerar o redirecionamento." "Redis 7" {
                tags "Database"
            }
            fila = container "Fila de Eventos de Clique" "Fila de eventos de clique publicados pela API e consumidos pelo worker." "RabbitMQ" {
                tags "Queue"
            }
        }

        googleWorkspace = softwareSystem "Google Workspace" "Provedor de identidade da empresa, usado para autenticação SSO." {
            tags "External"
        }

        // Pessoas
        usuario -> encurtai.spa "Cria e gerencia links curtos usando" "HTTPS"
        usuario -> encurtai.api "Acessa links curtos e é redirecionado por" "HTTPS"

        // Dentro do Encurtaí
        encurtai.spa -> encurtai.api "Chama" "JSON/HTTPS"
        encurtai.api -> encurtai.db "Grava e lê links em" "SQL/TCP"
        encurtai.api -> encurtai.cache "Consulta o destino dos links curtos em" "Redis/TCP"
        encurtai.api -> encurtai.fila "Publica eventos de clique em" "AMQP"
        encurtai.fila -> encurtai.worker "Entrega eventos de clique para" "AMQP"
        encurtai.worker -> encurtai.db "Grava métricas agregadas em" "SQL/TCP"

        // Sistemas externos
        encurtai.api -> googleWorkspace "Autentica usuários via SSO usando" "HTTPS"
    }

    views {
        systemContext encurtai "SystemContext" "Quem usa o Encurtaí e de que sistema externo ele depende." {
            include *
            autoLayout
        }

        container encurtai "Containers" "Os containers do Encurtaí e como se comunicam." {
            include *
            autoLayout
        }

        dynamic encurtai "Redirecionamento" "Fluxo de redirecionamento de um link curto." {
            title "Redirecionamento de um link curto"
            usuario -> encurtai.api "Acessa o link curto"
            encurtai.api -> encurtai.cache "Consulta o destino do link no cache"
            encurtai.api -> encurtai.db "Em caso de cache miss, consulta o destino do link"
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
            element "WebBrowser" {
                shape webBrowser
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
