workspace "FabricaViva" "Plataforma de monitoramento de chão de fábrica: recebe frames das câmeras industriais, comanda os braços robóticos e expõe um painel web aos operadores." {

    !identifiers hierarchical

    model {
        operador = person "Operador" "Acompanha o chão de fábrica pelo painel web."

        fabricaviva = softwareSystem "FabricaViva" "Plataforma de monitoramento de chão de fábrica." {
            painel = container "Painel" "Painel web usado pelos operadores para acompanhar o chão de fábrica." "Vue" {
                tags "WebBrowser"
            }
            ingestao = container "Serviço de Ingestão" "Recebe os frames de vídeo enviados pelas câmeras industriais." "Go"
            comandos = container "Serviço de Comandos" "Envia comandos aos braços robóticos via OPC UA." "Go"
            telemetria = container "Banco de Telemetria" "Armazena a telemetria da plataforma." "TimescaleDB" {
                tags "Database"
            }
        }

        // Hardware de terceiros com firmware fechado: modelado como sistema externo (caixa fechada).
        cameras = softwareSystem "Câmeras Industriais" "Câmeras Basler com firmware fechado; enviam frames de vídeo para a plataforma." {
            tags "External" "Hardware"
        }
        robos = softwareSystem "Braços Robóticos" "Braços robóticos KUKA; recebem comandos da plataforma." {
            tags "External" "Hardware"
        }

        operador -> fabricaviva.painel "Acompanha o chão de fábrica usando" "HTTPS"
        cameras -> fabricaviva.ingestao "Envia frames de vídeo para" "RTSP"
        fabricaviva.comandos -> robos "Envia comandos para" "OPC UA"

        // TODO (a confirmar com o time): quem grava e quem lê o Banco de Telemetria,
        // e como o Painel se conecta aos serviços de Ingestão e Comandos.
    }

    views {
        systemContext fabricaviva "SystemContext" {
            include *
            autoLayout lr
        }

        container fabricaviva "Containers" {
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
            element "WebBrowser" {
                shape webbrowser
            }
            element "Database" {
                shape cylinder
            }
            element "External" {
                background #999999
                color #ffffff
            }
            element "Hardware" {
                shape hexagon
            }
        }
    }

    configuration {
        scope softwaresystem
    }
}
