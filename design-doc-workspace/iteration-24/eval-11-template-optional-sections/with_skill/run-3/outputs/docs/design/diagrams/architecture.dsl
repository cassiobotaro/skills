workspace {
    model {
        produtor = softwareSystem "Produtores de eventos" "Enviam eventos e reenviam em caso de retry."
        faturamento = softwareSystem "Relatórios de faturamento" "Consomem os eventos ingeridos."

        pipeline = softwareSystem "Pipeline de ingestão" {
            ingestor = container "Ingestor" "Recebe os eventos dos produtores."
            dedup = container "Serviço de deduplicação" "Descarta eventos cuja chave idempotente já foi vista nas últimas 24h."
            redis = container "Redis" "Guarda a chave idempotente de cada evento por 24h." "Redis"
            kafka = container "Kafka" "Recebe os eventos únicos." "Kafka"
        }

        produtor -> ingestor "Envia eventos"
        ingestor -> dedup "Encaminha eventos"
        dedup -> redis "Consulta e registra a chave idempotente"
        dedup -> kafka "Publica eventos não repetidos"
        kafka -> faturamento "Entrega eventos"
    }
    views {
        container pipeline "container" {
            include *
            autolayout lr
        }
    }
}
