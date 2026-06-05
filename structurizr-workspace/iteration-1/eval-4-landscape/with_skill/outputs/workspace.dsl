workspace "Fintech de Crédito" "Visão de landscape dos sistemas da empresa." {

    !identifiers hierarchical

    model {
        cliente = person "Cliente" "Solicita e acompanha crédito."
        analista = person "Analista de Crédito" "Avalia propostas no backoffice."
        cobrador = person "Time de Cobrança" "Gerencia a cobrança de contratos."

        portal = softwareSystem "Portal do Cliente" "Canal web e aplicativo para os clientes."
        motor = softwareSystem "Motor de Crédito" "Avalia as propostas de crédito; inclui o backoffice dos analistas."
        cobranca = softwareSystem "Cobrança" "Gerencia a cobrança dos contratos."
        dataLake = softwareSystem "Data Lake" "Plataforma de dados que consolida eventos dos sistemas internos."

        core = softwareSystem "Core Bancário" "Produto terceirizado da Matera; registra os contratos." {
            tags "External"
        }

        cliente -> portal "Solicita e acompanha crédito no"
        analista -> motor "Avalia propostas no backoffice do"
        cobrador -> cobranca "Gerencia a cobrança no"

        motor -> core "Cria contratos a partir de propostas aprovadas no" "HTTPS"
        cobranca -> core "Lê os contratos do" "HTTPS"

        portal -> dataLake "Envia eventos para o"
        motor -> dataLake "Envia eventos para o"
        cobranca -> dataLake "Envia eventos para o"
    }

    views {
        systemLandscape "Landscape" {
            include *
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
            element "External" {
                background #999999
                color #ffffff
            }
        }
    }

    configuration {
        scope landscape
    }
}
