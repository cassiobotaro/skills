workspace "Encurtaí" "Encurtador de URLs interno da empresa." {

    !identifiers hierarchical

    model {
        usuario = person "Usuário da empresa" "Colaborador que cria links curtos e acessa links encurtados."

        encurtai = softwareSystem "Encurtaí" "Encurta URLs, redireciona acessos a links curtos e agrega métricas de clique." {
            spa = container "Aplicação Web" "Interface para criar e gerenciar links curtos." "React (SPA servido por nginx)" {
                tags "WebBrowser"
            }
            api = container "API" "Cria e resolve links curtos, redireciona acessos, autentica usuários via SSO e publica eventos de clique." "Go (Gin)"
            db = container "Banco de dados" "Armazena os links encurtados e as métricas agregadas de clique." "PostgreSQL 16" {
                tags "Database"
            }
            cache = container "Cache de redirecionamentos" "Cache dos destinos dos links curtos para acelerar o redirecionamento." "Redis 7" {
                tags "Cache"
            }
            fila = container "Fila de eventos de clique" "Buffer dos eventos de clique publicados pela API." "RabbitMQ" {
                tags "Queue"
            }
            worker = container "Worker de métricas" "Consome eventos de clique e grava métricas agregadas." "Go"
        }

        google = softwareSystem "Google Workspace" "Provedor de identidade da empresa, usado para autenticação SSO." {
            tags "External"
        }

        // Relação de nível de sistema (definida primeiro para dar o rótulo do diagrama de contexto)
        usuario -> encurtai "Cria, gerencia e acessa links curtos usando"

        usuario -> encurtai.spa "Cria e gerencia links curtos usando" "HTTPS"
        usuario -> encurtai.api "Acessa links curtos e é redirecionado por" "HTTPS"
        encurtai.spa -> encurtai.api "Chama" "REST/JSON sobre HTTPS"
        encurtai.api -> encurtai.db "Grava e lê links em" "SQL/TCP"
        encurtai.api -> encurtai.cache "Consulta e armazena redirecionamentos em" "Redis/TCP"
        encurtai.api -> encurtai.fila "Publica eventos de clique em" "AMQP"
        encurtai.fila -> encurtai.worker "Entrega eventos de clique para" "AMQP"
        encurtai.worker -> encurtai.db "Grava métricas agregadas em" "SQL/TCP"
        encurtai.api -> google "Autentica usuários via SSO usando" "HTTPS"
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

        dynamic encurtai "Redirecionamento" "Fluxo de redirecionamento de um link curto." {
            title "Redirecionamento de um link curto"
            usuario -> encurtai.api "Acessa o link curto"
            encurtai.api -> encurtai.cache "Consulta o destino do link no cache"
            encurtai.api -> encurtai.db "Em caso de cache miss, consulta o link em"
            encurtai.api -> encurtai.fila "Publica o evento de clique em"
            encurtai.api -> usuario "Responde com o redirecionamento para a URL de destino"
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
            }
            element "WebBrowser" {
                shape webbrowser
            }
            element "Database" {
                shape cylinder
                background #438dd5
            }
            element "Cache" {
                shape cylinder
                background #85bbf0
                color #000000
            }
            element "Queue" {
                shape pipe
                background #438dd5
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
