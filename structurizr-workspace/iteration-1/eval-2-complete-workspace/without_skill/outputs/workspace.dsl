workspace "Encurtaí" "Encurtador de URLs interno da empresa." {

    !identifiers hierarchical

    model {
        // Pessoas / atores
        usuario = person "Usuário interno" "Colaborador da empresa que encurta e acessa links curtos."

        // Sistema externo
        googleWorkspace = softwareSystem "Google Workspace" "Provedor de identidade usado para autenticação SSO dos usuários." {
            tags "Sistema Externo"
        }

        // Sistema do nosso time
        encurtai = softwareSystem "Encurtaí" "Encurtador de URLs interno: cria links curtos e redireciona, registrando métricas de clique." {

            spa = container "SPA" "Interface web para criar e gerenciar links curtos." "React (servido por nginx)" {
                tags "Web Browser"
            }

            api = container "API" "Cria/lê links, resolve redirecionamentos e publica eventos de clique. Faz autenticação SSO." "Go (Gin)"

            worker = container "Worker de Métricas" "Consome eventos de clique da fila e grava métricas agregadas." "Go"

            cache = container "Cache de Redirecionamentos" "Cacheia o mapeamento de link curto -> URL de destino." "Redis 7" {
                tags "Cache"
            }

            fila = container "Fila de Eventos de Clique" "Transporta os eventos de clique entre a API e o worker." "RabbitMQ" {
                tags "Fila"
            }

            db = container "Banco de Dados" "Armazena links, usuários e métricas agregadas de clique." "PostgreSQL 16" {
                tags "Banco de Dados"
            }
        }

        // Relacionamentos - nível de contexto
        usuario -> encurtai "Encurta e acessa links curtos usando"
        encurtai -> googleWorkspace "Autentica usuários (SSO) via"

        // Relacionamentos - nível de container
        usuario -> encurtai.spa "Acessa via navegador" "HTTPS"
        encurtai.spa -> encurtai.api "Faz chamadas à API" "JSON/HTTPS"
        usuario -> encurtai.api "Acessa links curtos (redirecionamento)" "HTTPS"

        encurtai.api -> encurtai.cache "Lê/escreve mapeamento de redirecionamento" "RESP"
        encurtai.api -> encurtai.db "Lê e grava links e usuários" "SQL/TCP"
        encurtai.api -> encurtai.fila "Publica eventos de clique" "AMQP"
        encurtai.api -> googleWorkspace "Autentica usuários (SSO) via" "OAuth 2.0 / OIDC"

        encurtai.worker -> encurtai.fila "Consome eventos de clique de" "AMQP"
        encurtai.worker -> encurtai.db "Grava métricas agregadas em" "SQL/TCP"
    }

    views {
        systemContext encurtai "Contexto" "Diagrama de contexto do sistema Encurtaí." {
            include *
            autolayout lr
        }

        container encurtai "Containers" "Diagrama de containers do sistema Encurtaí." {
            include *
            autolayout lr
        }

        dynamic encurtai "Redirecionamento" "Fluxo de redirecionamento de um link curto." {
            usuario -> encurtai.api "Acessa o link curto"
            encurtai.api -> encurtai.cache "Consulta o destino no cache"
            encurtai.api -> encurtai.db "Em caso de miss, busca o destino no banco"
            encurtai.api -> encurtai.fila "Publica o evento de clique"
            autolayout lr
        }

        styles {
            element "Element" {
                shape RoundedBox
                background #1168bd
                color #ffffff
            }
            element "Person" {
                shape Person
                background #08427b
                color #ffffff
            }
            element "Software System" {
                background #1168bd
                color #ffffff
            }
            element "Container" {
                background #438dd5
                color #ffffff
            }
            element "Web Browser" {
                shape WebBrowser
            }
            element "Sistema Externo" {
                background #999999
                color #ffffff
            }
            element "Banco de Dados" {
                shape Cylinder
                background #b8551b
                color #ffffff
            }
            element "Cache" {
                shape Cylinder
                background #d4751b
                color #ffffff
            }
            element "Fila" {
                shape Pipe
                background #7b4f9d
                color #ffffff
            }
        }

        theme default
    }
}
