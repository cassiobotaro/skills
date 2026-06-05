workspace "Fintech de Crédito" "Visão geral (landscape) dos sistemas da empresa." {

    model {
        cliente = person "Cliente" "Pessoa física ou jurídica que solicita e acompanha crédito."
        analistaCredito = person "Analista de Crédito" "Avalia e decide sobre propostas de crédito no backoffice."
        timeCobranca = person "Time de Cobrança" "Operadores responsáveis pela cobrança de contratos."

        coreBancario = softwareSystem "Core Bancário" "Produto terceirizado da Matera. Mantém contratos, contas e movimentações financeiras." {
            tags "Externo"
        }

        portalCliente = softwareSystem "Portal do Cliente" "Canal web e aplicativo onde o cliente solicita e acompanha o crédito." {
            tags "Interno"
        }

        motorCredito = softwareSystem "Motor de Crédito" "Avalia propostas de crédito; inclui backoffice usado pelos analistas." {
            tags "Interno"
        }

        cobranca = softwareSystem "Cobrança" "Gestão e operação da cobrança de contratos." {
            tags "Interno"
        }

        dataLake = softwareSystem "Data Lake" "Repositório analítico do time de dados que centraliza eventos dos sistemas internos." {
            tags "Interno"
        }

        cliente -> portalCliente "Solicita e acompanha crédito" "Web / App"
        analistaCredito -> motorCredito "Analisa e decide propostas" "Backoffice"
        timeCobranca -> cobranca "Opera a cobrança"

        portalCliente -> motorCredito "Envia propostas de crédito"
        motorCredito -> coreBancario "Cria contratos a partir de propostas aprovadas"
        cobranca -> coreBancario "Lê os contratos"

        portalCliente -> dataLake "Envia eventos" "Streaming"
        motorCredito -> dataLake "Envia eventos" "Streaming"
        cobranca -> dataLake "Envia eventos" "Streaming"
    }

    views {
        systemLandscape "Landscape" "Visão geral de todos os sistemas da fintech de crédito." {
            include *
            autoLayout lr
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
            element "Externo" {
                background #999999
                color #ffffff
            }
        }
    }
}
