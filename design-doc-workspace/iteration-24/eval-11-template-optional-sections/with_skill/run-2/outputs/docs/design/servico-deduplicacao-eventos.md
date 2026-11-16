# Serviço de deduplicação de eventos · DD-2026-<seq>

| | |
|---|---|
| **Documento** | DD-2026-<seq> |
| **Estado** | Rascunho |
| **Autores** | Rafael Nunes |
| **Revisores** | |
| **Criado em** | 2026-11-16 |
| **Última atualização** | 2026-11-16 |

## Motivação

O pipeline de ingestão recebe eventos duplicados dos produtores, que reenviam o mesmo evento quando fazem retry. No mês passado medimos 4% de duplicatas. Elas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes.

## Proposta

Vamos criar um serviço de deduplicação entre o ingestor e o Kafka. Para cada evento, o serviço consulta a chave idempotente no Redis. Se a chave já existe, o serviço descarta o evento. Se não existe, grava a chave com validade de 24h e repassa o evento ao Kafka.

![Diagrama de containers: serviço de deduplicação](diagrams/arquitetura.svg)

> Renderizar na passada manual: o diagrama acima ainda não foi exportado para imagem.

<details>
<summary>Código do diagrama (Structurizr DSL)</summary>

```
workspace {
    model {
        produtores = softwareSystem "Produtores de eventos" "Reenviam o evento em caso de retry" "Existing"
        pipeline = softwareSystem "Pipeline de ingestão" {
            ingestor = container "Ingestor" "Recebe os eventos dos produtores"
            dedup = container "Serviço de deduplicação" "Descarta eventos cuja chave idempotente já foi vista"
            redis = container "Redis" "Guarda a chave idempotente de cada evento por 24h" "" "Database"
            kafka = container "Kafka" "Recebe os eventos únicos"
        }

        produtores -> ingestor "Envia eventos"
        ingestor -> dedup "Encaminha eventos"
        dedup -> redis "Consulta e grava a chave idempotente"
        dedup -> kafka "Publica eventos não repetidos"
    }

    views {
        container pipeline "Containers" {
            include *
            autoLayout lr
        }
        styles {
            element "Database" {
                shape Cylinder
            }
        }
    }
}
```

</details>

O ingestor continua recebendo os eventos dos produtores, mas agora entrega cada um ao serviço de deduplicação em vez de publicar direto no Kafka. O serviço consulta o Redis com a chave idempotente do evento. Quando a chave já está lá, o evento é um reenvio e o serviço o descarta. Quando a chave é nova, o serviço a grava no Redis, que a mantém por 24h, e publica o evento no Kafka. Os consumidores do Kafka passam a ler um fluxo já sem reenvios e não precisam deduplicar nada.

Trade-off aceito: o serviço entra no caminho crítico da ingestão como mais um salto, e estimamos +5ms de latência por evento. Em troca, a deduplicação fica em um único lugar, na entrada do Kafka.

## Riscos

| Risco | Mitigação |
|---|---|
| Mais um salto no caminho crítico da ingestão, com +5ms estimados de latência. | Aceito pelo time em troca de deduplicar em um único ponto. A estimativa ainda não foi medida (ver Perguntas abertas). |

Outros riscos da proposta, e a mitigação de cada um, dependem das respostas listadas em Perguntas abertas.

## Alternativas consideradas

Esta seção não existe no template; ela guarda as alternativas que o time discutiu, que o template não tem onde registrar.

| Alternativa | Resultado | Motivo |
|---|---|---|
| **Serviço entre o ingestor e o Kafka, com Redis (escolhida)** | ✓ escolhida | Deduplica em um ponto só. Custa um salto a mais no caminho crítico (+5ms estimados). |
| Deduplicar no consumidor | ✗ descartada | Cada consumidor teria que reimplementar a deduplicação. |
| Idempotência nativa do produtor Kafka | ✗ descartada | Não cobre o reenvio entre reinícios do produtor. |
| Não fazer nada | ✗ descartada | Os 4% de duplicatas continuam inflando os relatórios de faturamento, e o financeiro já reclamou duas vezes. |

## Métricas de sucesso

- Duplicatas abaixo de 0,1% dos eventos (hoje: 4%, medido no mês passado).

## Perguntas abertas

- Qual é o campo ou a composição de campos que forma a chave idempotente do evento?
- O que o serviço faz quando o Redis está indisponível: descarta, deixa passar ou recusa o evento?
- Quem revisa este documento (áreas e times impactados)?
- Qual é o número sequencial deste documento (`DD-2026-<seq>`)?
- O rollout será gradual ou de uma vez, e existe plano de rollback?
