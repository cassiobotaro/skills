workspace "Encurtaí" "Encurtador de URLs interno da empresa." {

    !identifiers hierarchical

    model {
        usuario = person "Usuário da empresa" "Colaborador que cria links curtos e acessa links encurtados."

        encurtai = softwareSystem "Encurtaí" "Encurta URLs e redireciona links curtos para seus destinos, registrando métricas de clique." {
            spa = container "Aplicação Web" "Interface para criar e gerenciar links curtos." "React (SPA servido por nginx)" {
                tags "WebApp"
            }
            api = container "API" "Cria e resolve links curtos, autentica usuários via SSO e publica eventos de clique." "Go (Gin), REST"
            db = container "Banco de Dados" "Armazena os links e as métricas agregadas de clique." "PostgreSQL 16" {
                tags "Database"
            }
            cache = container "Cache de Redirecionamentos" "Cache dos destinos dos links curtos, consultado antes do banco." "Redis 7" {
                tags "Database"
            }
            fila = container "Fila de Eventos de Clique" "Eventos de clique publicados pela API e consumidos pelo worker." "RabbitMQ" {
                tags "Queue"
            }
            worker = container "Worker de Métricas" "Consome eventos de clique e grava métricas agregadas." "Go"
        }

        google = softwareSystem "Google Workspace" "Provedor de identidade da empresa, usado para autenticação SSO dos usuários." {
            tags "External"
        }

        // Relacionamento no nível de sistema (resume os dois acessos do usuário abaixo)
        usuario -> encurtai "Cria, gerencia e acessa links curtos usando"

        usuario -> encurtai.spa "Cria e gerencia links curtos usando" "HTTPS"
        usuario -> encurtai.api "Acessa links curtos para ser redirecionado por" "HTTPS"
        encurtai.spa -> encurtai.api "Chama para criar e consultar links" "JSON/HTTPS"
        encurtai.api -> google "Autentica usuários via SSO em" "HTTPS"
        encurtai.api -> encurtai.db "Grava e lê links em" "SQL/TCP"
        encurtai.api -> encurtai.cache "Consulta e armazena redirecionamentos em" "RESP/TCP"
        encurtai.api -> encurtai.fila "Publica eventos de clique em" "AMQP"
        encurtai.fila -> encurtai.worker "Entrega eventos de clique para" "AMQP"
        encurtai.worker -> encurtai.db "Grava métricas agregadas em" "SQL/TCP"
    }

    views {
        systemContext encurtai "SystemContext" "Encurtaí, quem o usa e o sistema externo do qual depende." {
            include *
            autoLayout
        }

        container encurtai "Containers" "Containers do Encurtaí e como se comunicam." {
            include *
            autoLayout
        }

        dynamic encurtai "RedirecionamentoLink" "Fluxo de redirecionamento de um link curto." {
            title "Redirecionamento de um link curto"
            usuario -> encurtai.api "Acessa o link curto"
            encurtai.api -> encurtai.cache "Consulta o destino do link curto em"
            encurtai.api -> encurtai.db "Em caso de cache miss, consulta o destino do link em"
            encurtai.api -> encurtai.fila "Publica o evento de clique em"
            encurtai.api -> usuario "Redireciona para a URL de destino"
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
            element "Container" {
                background #438dd5
            }
            element "WebApp" {
                shape webBrowser
            }
            element "Database" {
                shape cylinder
            }
            element "Queue" {
                shape pipe
                background #f5a623
                color #000000
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
