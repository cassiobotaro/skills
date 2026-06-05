workspace "OrderHub" "Sistema de pedidos e seus sistemas vizinhos." {

    !identifiers hierarchical

    model {
        cliente = person "Cliente" "Faz pedidos e recebe notificações sobre eles."

        orderHub = softwareSystem "OrderHub" "Sistema principal de pedidos." {
            app = container "Aplicação de Pedidos" "Gerencia o ciclo de vida dos pedidos." "Aplicação"
            cache = container "Cache" "Armazena dados de pedidos em memória para acesso rápido." "Redis" {
                tags "Database"
            }
            conciliacaoJob = container "Job de Conciliação de Notas Fiscais" "Roda de madrugada para conciliar as notas fiscais dos pedidos." "Job agendado (cron)"
        }

        pagamentos = softwareSystem "Sistema de Pagamentos" "Processa pagamentos. Mantido por outro time." {
            tags "External"
        }

        notificacoes = softwareSystem "Plataforma de Notificações" "Envia e-mail e push para os clientes." {
            tags "External"
        }

        cliente -> orderHub.app "Faz e acompanha pedidos usando" "HTTPS"

        orderHub.app -> orderHub.cache "Lê e escreve dados de pedidos em" "Redis"
        orderHub.app -> pagamentos "Solicita o processamento de pagamentos ao" "HTTPS"
        orderHub.app -> notificacoes "Solicita o envio de notificações à" "HTTPS"

        orderHub.conciliacaoJob -> orderHub.cache "Lê dados de pedidos de" "Redis"
        orderHub.conciliacaoJob -> pagamentos "Concilia notas fiscais contra o" "HTTPS"

        notificacoes -> cliente "Envia e-mail e push para"
    }

    views {
        systemContext orderHub "SystemContext" {
            include *
            autoLayout
        }

        container orderHub "Containers" {
            include *
            autoLayout
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
