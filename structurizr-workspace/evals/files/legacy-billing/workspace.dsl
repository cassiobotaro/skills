workspace "Faturamento" "Sistema de faturamento da empresa." {

    !identifiers hierarchical

    model {
        atendente = person "Atendente" "Equipe financeira que emite e acompanha faturas."

        faturamento = softwareSystem "Faturamento" "Emite, processa e concilia faturas." {
            portal = container "Portal Web" "Interface para emissão e acompanhamento de faturas." "React"
            api = container "API de Faturamento" "Regras de negócio e orquestração de faturas." "Go"
            worker = container "Worker de Processamento" "Processa faturas de forma assíncrona." "Go"
            fila = container "Fila de Faturas" "Buffer de faturas a processar." "RabbitMQ" {
                tags "Queue"
            }
            banco = container "Banco de Dados" "Armazena faturas, clientes e itens." "PostgreSQL" {
                tags "Database"
            }
        }

        erp = softwareSystem "ERP" "Sistema corporativo de gestão (mantido por terceiro)." {
            tags "External"
        }

        atendente -> faturamento.portal "Emite e consulta faturas usando"
        faturamento.portal -> faturamento.api "Chama" "JSON/HTTPS"
        faturamento.api -> faturamento.banco "Lê e grava dados em" "SQL/TCP"
        faturamento.api -> faturamento.fila "Publica faturas emitidas em"
        faturamento.worker -> faturamento.fila "Consome faturas de"
        faturamento.worker -> faturamento.banco "Atualiza status em" "SQL/TCP"
        faturamento.worker -> erp "Envia faturas processadas para" "HTTPS"
    }

    views {
        systemContext faturamento "Contexto" {
            include *
            autoLayout
        }

        container faturamento "Containers" {
            include *
            autoLayout
        }

        styles {
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
}
