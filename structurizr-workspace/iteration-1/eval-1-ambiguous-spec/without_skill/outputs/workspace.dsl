workspace "Sistema de Pedidos" "Documentação da arquitetura do OrderHub e sistemas relacionados." {

    model {
        # Pessoas / Atores
        cliente = person "Cliente" "Realiza pedidos e recebe notificações (email e push)."
        timePagamentos = person "Time de Pagamentos" "Equipe interna que mantém o sistema de pagamentos."

        # Sistema principal
        orderHub = softwareSystem "OrderHub" "Sistema principal de gestão de pedidos." {
            api = container "API de Pedidos" "Recebe e processa pedidos dos clientes." "Aplicação (ex.: Java/Spring, Node, etc.)"
            cache = container "Cache" "Armazena dados temporários / sessões / dados de alta leitura." "Redis" {
                tags "Database"
            }
            jobConciliacao = container "Job de Conciliação de Notas Fiscais" "Roda de madrugada para conciliar as notas fiscais." "Job agendado (batch)"
        }

        # Sistemas externos (outros times)
        pagamentos = softwareSystem "Sistema de Pagamentos" "Processa pagamentos. Mantido por outro time interno." {
            tags "Time Interno"
        }

        notificacoes = softwareSystem "Plataforma de Notificações" "Envia email e push para os clientes." {
            tags "Time Interno"
        }

        # Relacionamentos - nível de contexto
        cliente -> orderHub "Faz pedidos / consulta status" "HTTPS"
        orderHub -> pagamentos "Solicita processamento de pagamentos" "HTTPS/API"
        orderHub -> notificacoes "Dispara notificações (email/push)" "HTTPS/API"
        notificacoes -> cliente "Envia email e push"
        timePagamentos -> pagamentos "Mantém"

        # Relacionamentos - nível de container
        cliente -> api "Faz pedidos / consulta status" "HTTPS/JSON"
        api -> cache "Lê e grava dados" "Redis protocol"
        api -> pagamentos "Solicita processamento de pagamentos" "HTTPS/API"
        api -> notificacoes "Dispara notificações" "HTTPS/API"
        jobConciliacao -> cache "Lê dados para conciliação" "Redis protocol"
        jobConciliacao -> pagamentos "Concilia notas fiscais com pagamentos" "HTTPS/API"
    }

    views {
        systemContext orderHub "Contexto" {
            include *
            autolayout lr
        }

        container orderHub "Containers" {
            include *
            autolayout lr
        }

        styles {
            element "Person" {
                shape Person
                background #08427b
                color #ffffff
            }
            element "Software System" {
                background #1168bd
                color #ffffff
            }
            element "Time Interno" {
                background #6b6b6b
                color #ffffff
            }
            element "Container" {
                background #438dd5
                color #ffffff
            }
            element "Database" {
                shape Cylinder
                background #438dd5
                color #ffffff
            }
        }
    }
}
