workspace "Sistema de Agendamento" "Modelo C4 do sistema de agendamento: app mobile, painel web, API e lembretes por SMS." {

    !identifiers hierarchical

    model {
        usuario = person "Usuário" "Cria e consulta agendamentos pelo app mobile ou pelo painel web."

        agendamento = softwareSystem "Sistema de Agendamento" "Registra agendamentos e envia lembretes por SMS." {

            appMobile = container "App Mobile" "Permite ao usuário criar e consultar agendamentos pelo celular." "Flutter"

            painelWeb = container "Painel Web" "Interface web para acompanhar e administrar os agendamentos." "Vue"

            api = container "API" "Expõe as operações de agendamento e dispara os lembretes." "Python (FastAPI)"

            bancoDeDados = container "Banco de Dados" "Armazena os agendamentos." "PostgreSQL 15" {
                tags "Database"
            }
        }

        twilio = softwareSystem "Twilio" "Serviço externo de envio de SMS." {
            tags "External"
        }

        usuario -> agendamento.appMobile "Cria e consulta agendamentos usando"
        usuario -> agendamento.painelWeb "Cria e consulta agendamentos usando"

        agendamento.appMobile -> agendamento.api "Faz chamadas de agendamento para" "JSON/HTTPS"
        agendamento.painelWeb -> agendamento.api "Faz chamadas de agendamento para" "JSON/HTTPS"
        agendamento.api -> agendamento.bancoDeDados "Lê e grava agendamentos em" "SQL/TCP"
        agendamento.api -> twilio "Envia lembretes de agendamento por SMS através da" "API REST/HTTPS"
    }

    views {
        systemContext agendamento "SystemContext" {
            include *
            autoLayout
        }

        container agendamento "Containers" {
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
