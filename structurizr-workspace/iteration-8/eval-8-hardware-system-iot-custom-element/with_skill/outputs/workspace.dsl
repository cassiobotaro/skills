workspace "FabricaViva" "Plataforma de monitoramento de chão de fábrica: recebe frames das câmeras industriais e comanda os braços robóticos." {

    !identifiers hierarchical

    model {
        archetypes {
            hardwareSystem = element {
                metadata "Sistema de Hardware"
                tags "Hardware"
            }
        }

        operador = person "Operador" "Acompanha o chão de fábrica pelo painel web."

        fabricaViva = softwareSystem "FabricaViva" "Plataforma de monitoramento de chão de fábrica: recebe frames das câmeras industriais e comanda os braços robóticos." {
            painel = container "Painel" "Interface web usada pelos operadores para acompanhar o chão de fábrica." "Vue" {
                tags "WebBrowser"
            }
            ingestao = container "Serviço de Ingestão" "Recebe os frames de vídeo das câmeras industriais." "Go"
            comandos = container "Serviço de Comandos" "Envia comandos aos braços robóticos." "Go"
            telemetria = container "Banco de Telemetria" "Armazena a telemetria do chão de fábrica." "TimescaleDB" {
                tags "Database"
            }
        }

        // element <name> [metadata] [description]: the type line comes first, then the description
        cameras = hardwareSystem "Câmeras Industriais" "Sistema de Hardware" "Câmeras Basler com firmware fechado; capturam o chão de fábrica."
        bracos = hardwareSystem "Braços Robóticos" "Sistema de Hardware" "Braços robóticos KUKA que executam os comandos recebidos da plataforma."

        operador -> fabricaViva.painel "Acompanha o chão de fábrica usando" "HTTPS"
        cameras -> fabricaViva.ingestao "Envia frames de vídeo para" "RTSP"
        fabricaViva.comandos -> bracos "Envia comandos para" "OPC UA"
    }

    views {
        systemContext fabricaViva "SystemContext" {
            include *
            autoLayout
        }

        container fabricaViva "Containers" {
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
            element "WebBrowser" {
                shape webbrowser
            }
            element "Database" {
                shape cylinder
            }
            element "Hardware" {
                shape robot
                background #6b6b6b
                color #ffffff
            }
        }
    }

    configuration {
        scope softwaresystem
    }
}
