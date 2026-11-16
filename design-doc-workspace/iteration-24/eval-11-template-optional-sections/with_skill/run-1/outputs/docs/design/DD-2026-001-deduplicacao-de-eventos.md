# Serviço de deduplicação de eventos · DD-2026-001

| | |
|---|---|
| **Documento** | DD-2026-001 |
| **Estado** | Rascunho |
| **Autores** | Rafael Nunes |
| **Revisores** | |
| **Criado em** | 2026-11-16 |
| **Última atualização** | 2026-11-16 |

## Motivação

O pipeline de ingestão recebe eventos duplicados dos produtores, que reenviam o mesmo evento em retry. No mês passado medimos 4% de eventos duplicados. As duplicatas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes.

## Proposta

Vamos criar um serviço de deduplicação que fica entre o ingestor e o Kafka. Para cada evento recebido, o serviço consulta a chave idempotente do evento no Redis. Se a chave já existe, o serviço descarta o evento. Se não existe, o serviço guarda a chave no Redis por 24 horas e entrega o evento ao Kafka.

![Diagrama de containers: serviço de deduplicação de eventos](diagrams/architecture.svg)

> Render pendente: gerar a imagem a partir do DSL abaixo no passe manual.

<details>
<summary>Código do diagrama (Structurizr DSL)</summary>

```
workspace {
    model {
        produtores = softwareSystem "Produtores de eventos" "Enviam eventos e reenviam em retry." "External"

        pipeline = softwareSystem "Pipeline de ingestão" {
            ingestor = container "Ingestor" "Recebe os eventos dos produtores."
            dedup = container "Serviço de deduplicação" "Descarta eventos repetidos pela chave idempotente."
            redis = container "Redis" "Guarda a chave idempotente de cada evento por 24h." "Redis" "Database"
            kafka = container "Kafka" "Recebe os eventos únicos." "Kafka"
        }

        produtores -> ingestor "Envia eventos"
        ingestor -> dedup "Encaminha eventos"
        dedup -> redis "Consulta e grava chaves idempotentes"
        dedup -> kafka "Entrega eventos não repetidos"
    }

    views {
        container pipeline "Containers" {
            include *
            autolayout lr
        }
        styles {
            element "External" {
                background #999999
            }
            element "Database" {
                shape cylinder
            }
        }
    }
}
```

</details>

Os produtores enviam eventos ao ingestor, e um retry do produtor gera o mesmo evento outra vez. O ingestor não entrega mais direto ao Kafka: ele encaminha cada evento ao serviço de deduplicação. O serviço usa o Redis como memória das chaves idempotentes já vistas, com validade de 24 horas, e só entrega ao Kafka os eventos cuja chave ainda não existe. Os consumidores do Kafka passam a receber eventos sem repetição e não precisam deduplicar por conta própria.

### Alternativas consideradas

O template não tem uma seção para alternativas, e o time as discutiu. Por isso esta seção extra entra logo após a proposta, sem alterar a ordem das seções do template.

| Opção | Resultado | Motivo |
|---|---|---|
| Não fazer nada | ✗ Descartada | Os 4% de duplicatas continuam inflando os relatórios de faturamento, e o financeiro já reclamou duas vezes. |
| Deduplicar no consumidor | ✗ Descartada | Cada consumidor teria que reimplementar a deduplicação. |
| Idempotência nativa do produtor Kafka | ✗ Descartada | Não cobre o reenvio entre reinícios do produtor. |
| **Serviço de deduplicação entre o ingestor e o Kafka** | ✓ Escolhida | Deduplica uma vez, antes do Kafka, e cobre o reenvio em retry. |

## Riscos

- **Mais um salto no caminho crítico da ingestão.** O serviço adiciona uma chamada a cada evento, e estimamos +5ms de latência. O time aceitou esse custo em troca de eliminar as duplicatas. A estimativa ainda não foi medida.
- **Mitigações.** Ainda não definimos como mitigar este risco nem outros riscos do desenho. Veja as perguntas abertas.

## Métricas de sucesso

- Taxa de eventos duplicados abaixo de 0,1% (hoje: 4%, medida no mês passado).
- Latência adicional na ingestão: estimativa de +5ms, a confirmar com medição.

## Perguntas abertas

- Qual é a chave idempotente de cada evento, e quem a gera (o produtor ou o ingestor)?
- O que o serviço faz quando o Redis está indisponível: deixa passar os eventos ou os bloqueia? Qual é o impacto de cada escolha no faturamento e na latência?
- Como mitigamos o salto extra no caminho crítico (por exemplo, limite de latência aceitável e alerta)?
- Quais outros riscos o time identificou, e qual é a mitigação de cada um?
- Qual é a latência real do serviço, e como a medimos antes do rollout?
- Quem revisa este documento (arquitetura, plataforma, financeiro)?
- Este doc está ligado a uma história do backlog? Se sim, quais são os critérios de aceite?
- Há dados existentes a migrar, por exemplo eventos já ingeridos que precisam ser deduplicados?
- Como o serviço entra em produção (fases, critério de avanço, rollback)?
