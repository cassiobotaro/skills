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

O pipeline de ingestão recebe eventos duplicados dos produtores, que reenviam o mesmo evento quando fazem retry. No mês passado medimos 4% de duplicatas. Elas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes.

Sem uma mudança, as duplicatas continuam entrando no Kafka e chegando a todos os consumidores, inclusive os que alimentam o faturamento.

## Proposta

Criar um serviço de deduplicação entre o ingestor e o Kafka. O ingestor entrega cada evento ao serviço. O serviço consulta no Redis a chave idempotente do evento. Se a chave já existe, o serviço descarta o evento. Se não existe, o serviço grava a chave com validade de 24 horas e publica o evento no Kafka.

![Diagrama de containers: serviço de deduplicação de eventos](diagrams/deduplicacao-containers.svg)

*Placeholder: renderizar este diagrama a partir do DSL abaixo na passada manual.*

<details>
<summary>Código do diagrama (Structurizr DSL)</summary>

```
workspace {
    model {
        produtores = softwareSystem "Produtores de eventos" "Enviam eventos e reenviam em caso de retry." "External"

        pipeline = softwareSystem "Pipeline de ingestão" {
            ingestor = container "Ingestor" "Recebe os eventos dos produtores."
            dedup = container "Serviço de deduplicação" "Descarta eventos cuja chave idempotente já foi vista nas últimas 24h."
            redis = container "Redis" "Guarda as chaves idempotentes por 24h." "Redis" "Database"
            kafka = container "Kafka" "Recebe os eventos únicos." "Kafka"
        }

        produtores -> ingestor "Envia eventos"
        ingestor -> dedup "Entrega cada evento"
        dedup -> redis "Consulta e grava a chave idempotente"
        dedup -> kafka "Publica eventos não repetidos"
    }

    views {
        container pipeline "Containers" {
            include *
            autolayout lr
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

O ingestor deixa de publicar direto no Kafka e passa a entregar os eventos ao serviço de deduplicação. O serviço decide, para cada evento, se a chave idempotente já está no Redis. O Redis guarda cada chave por 24 horas. O Kafka passa a receber só a primeira ocorrência de cada evento dentro dessa janela. Os consumidores não mudam e não precisam tratar duplicatas.

O custo aceito é um salto a mais no caminho crítico da ingestão. A estimativa é de +5 ms de latência por evento. Não medimos esse número; é uma estimativa.

## Riscos

| Risco | Mitigação |
|---|---|
| O novo salto no caminho crítico adiciona latência à ingestão (estimativa de +5 ms). | Aceito pelo time em troca de eliminar as duplicatas. Sem mitigação definida até aqui. |
| Retries que chegam depois de 24 horas do evento original passam pela deduplicação, porque a chave já expirou. | Ver Perguntas abertas. |

Os demais riscos (indisponibilidade do serviço ou do Redis, por exemplo) ainda não foram discutidos e estão em Perguntas abertas.

## Métricas de sucesso

- Duplicatas abaixo de 0,1% dos eventos (hoje 4%, medido no mês passado).
- Latência adicional na ingestão: acompanhar contra a estimativa de +5 ms.

## Alternativas consideradas

Esta seção não existe no template do time. Entrou aqui para registrar o raciocínio da escolha; o time de arquitetura decide se mantém.

| Alternativa | Por que foi descartada |
|---|---|
| Não fazer nada | Mantém 4% de duplicatas e o faturamento inflado, e o financeiro continua reclamando. |
| Deduplicar no consumidor | Cada consumidor teria que reimplementar a deduplicação. |
| Idempotência nativa do produtor Kafka | Não cobre o reenvio entre reinícios do produtor. |

## Perguntas abertas

1. Quem são os revisores do documento?
2. Qual é a chave idempotente de um evento e quem a gera (produtor ou ingestor)?
3. O que o serviço faz se o Redis ou o próprio serviço ficar indisponível: bloqueia a ingestão, deixa passar eventos sem deduplicar ou enfileira?
4. Existem retries que chegam depois de 24 horas? Se existirem, a janela de 24 horas basta?
5. Como entra em produção (fases, critério de avanço, rollback)? O template tem um Plano de rollout opcional, que ficou de fora até haver essa resposta.
6. Este doc está ligado a uma história do backlog? Se estiver, a seção Critérios de aceite precisa ser preenchida.
7. Há dados existentes a migrar? Se houver, falta a seção Estratégia de migração.
