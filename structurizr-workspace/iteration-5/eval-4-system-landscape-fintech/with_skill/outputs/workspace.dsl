workspace "Fintech de Crédito" "Visão geral (system landscape) dos sistemas da empresa." {

    !identifiers hierarchical

    model {
        cliente = person "Cliente" "Contrata e acompanha seu crédito pelo Portal do Cliente."
        analista = person "Analista de Crédito" "Analisa e decide propostas no backoffice do Motor de Crédito."
        operadorCobranca = person "Time de Cobrança" "Opera a régua de cobrança dos contratos inadimplentes."

        group "Fintech" {
            portal = softwareSystem "Portal do Cliente" "Canal digital (web e app) onde o cliente solicita crédito e acompanha seus contratos."

            motorCredito = softwareSystem "Motor de Crédito" "Avalia as propostas de crédito e inclui o backoffice usado pelos analistas."

            cobranca = softwareSystem "Cobrança" "Conduz a cobrança dos contratos."

            dataLake = softwareSystem "Data Lake" "Repositório analítico do time de dados, alimentado por eventos dos sistemas internos."
        }

        coreBancario = softwareSystem "Core Bancário" "Produto terceirizado da Matera que mantém os contratos." {
            tags "External"
        }

        cliente -> portal "Solicita e acompanha crédito no"
        analista -> motorCredito "Analisa e decide propostas no backoffice do"
        operadorCobranca -> cobranca "Acompanha e opera a cobrança no"

        motorCredito -> coreBancario "Cria contratos, a partir de propostas aprovadas, no"
        cobranca -> coreBancario "Lê os contratos do"

        portal -> dataLake "Envia eventos para o"
        motorCredito -> dataLake "Envia eventos para o"
        cobranca -> dataLake "Envia eventos para o"
    }

    views {
        systemLandscape "SystemLandscape" "Panorama dos sistemas da fintech." {
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
