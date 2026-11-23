# Serviço de deduplicação de eventos · DD-2026-001

| | |
|---|---|
| **Documento** | DD-2026-001 |
| **Estado** | Rascunho |
| **Autores** | Rafael Nunes |
| **Revisores** | |
| **Criado em** | 2026-11-23 |
| **Última atualização** | 2026-11-23 |

## Motivação

O pipeline de ingestão recebe eventos duplicados dos produtores, que reenviam o mesmo evento quando fazem retry. No mês passado medimos 4% de eventos duplicados.

As duplicatas inflam os relatórios de faturamento. O financeiro já reclamou duas vezes.

## Proposta

Vamos criar um serviço de deduplicação entre o ingestor e o Kafka. Para cada evento recebido, o serviço consulta no Redis a chave idempotente do evento. Se a chave já existe, o serviço descarta o evento. Se não existe, o serviço grava a chave no Redis com validade de 24h e encaminha o evento ao Kafka.

![Diagrama de containers: serviço de deduplicação de eventos](diagrams/dedup-de-eventos.svg)

<details>
<summary>Fonte do diagrama (Structurizr DSL)</summary>

```
workspace {
    model {
        producer = softwareSystem "Produtores de eventos" "Enviam eventos e reenviam em caso de retry"

        pipeline = softwareSystem "Pipeline de ingestão" {
            ingestor = container "Ingestor" "Recebe os eventos dos produtores"
            dedup = container "Serviço de deduplicação" "Descarta eventos cuja chave idempotente já foi vista nas últimas 24h"
            redis = container "Redis" "Guarda as chaves idempotentes por 24h"
            kafka = container "Kafka" "Recebe os eventos únicos"
        }

        producer -> ingestor "Envia eventos"
        ingestor -> dedup "Repassa cada evento"
        dedup -> redis "Consulta e grava a chave idempotente"
        dedup -> kafka "Publica eventos não duplicados"
    }

    views {
        container pipeline {
            include *
            autolayout lr
        }
    }
}
```

</details>

O ingestor deixa de publicar direto no Kafka e passa a entregar cada evento ao serviço de deduplicação. O serviço decide, com base no Redis, se o evento é novo. Só eventos novos chegam ao Kafka, então os consumidores não precisam tratar duplicatas. A janela de deduplicação é de 24h: a chave expira do Redis depois disso.

### Alternativas consideradas

- **Deduplicar no consumidor.** Descartada. Cada consumidor teria que reimplementar a deduplicação.
- **Idempotência nativa do produtor Kafka.** Descartada. Ela não cobre o reenvio entre reinícios do produtor.

### Trade-off aceito

O serviço adiciona um salto no caminho crítico da ingestão. Estimamos +5ms de latência por evento. O time aceita esse custo em troca de eliminar as duplicatas num ponto único, antes do Kafka.

## Riscos

- **Latência no caminho crítico.** O novo salto soma cerca de 5ms (estimativa, ainda não medida) a toda ingestão. Este custo foi aceito (ver Trade-off aceito). A medição real entra nas métricas de sucesso.

Outros riscos e suas mitigações dependem das respostas em [Perguntas abertas](#perguntas-abertas).

## Plano de rollout

O plano de fases, os critérios de avanço e os critérios de rollback dependem das respostas em [Perguntas abertas](#perguntas-abertas).

## Métricas de sucesso

| Métrica | Hoje | Meta |
|---|---|---|
| Eventos duplicados no pipeline | 4% (mês passado) | abaixo de 0,1% |
| Latência adicionada à ingestão | n/a | estimativa de +5ms, a confirmar com medição |

## Perguntas abertas

1. **Chave idempotente.** Quem gera a chave de cada evento, o produtor ou o ingestor? Que campos a compõem? O reenvio por retry carrega sempre a mesma chave?
2. **Falha do serviço ou do Redis.** Quando o serviço de deduplicação ou o Redis estiver indisponível, o ingestor deve rejeitar os eventos (fail closed) ou encaminhá-los sem deduplicar (fail open)? Qual das duas consequências o time prefere aceitar?
3. **Janela de 24h.** De onde vem o número? Um reenvio que chegue depois de 24h passa como evento novo. O time aceita isso?
4. **Atomicidade.** Se o serviço gravar a chave no Redis e falhar antes de publicar no Kafka, o retry do produtor é descartado e o evento se perde. Como tratar esse caso?
5. **Riscos adicionais.** Que outros riscos o time enxerga, e qual a mitigação de cada um?
6. **Rollout.** Em quais fases o serviço entra em produção? Qual critério avança cada fase e qual dispara rollback?
7. **Limite de latência.** Qual valor de latência adicional é aceitável além da estimativa de 5ms?
8. **Revisores.** Quem do time de arquitetura e de outras equipes (por exemplo, financeiro e donos dos consumidores) deve revisar este documento?
9. **Detalhes do diagrama.** Que tecnologias e protocolos ligam o ingestor, o serviço de deduplicação, o Redis e o Kafka? O diagrama os omite porque não foram informados.
10. **Numeração.** O número DD-2026-001 assume que este é o primeiro design doc do repositório. Confirmar a sequência correta.
11. **Diagrama renderizado.** O arquivo `diagrams/dedup-de-eventos.svg` ainda não existe. Renderizar a partir do DSL acima.
