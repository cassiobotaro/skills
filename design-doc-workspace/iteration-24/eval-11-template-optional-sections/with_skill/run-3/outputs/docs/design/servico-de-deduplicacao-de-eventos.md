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

O pipeline de ingestão recebe eventos duplicados dos produtores, que reenviam o mesmo evento quando fazem retry. No mês passado medimos 4% de duplicatas. As duplicatas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes.

## Proposta

Criamos um serviço de deduplicação que fica entre o ingestor e o Kafka. Para cada evento recebido, o serviço consulta no Redis a chave idempotente do evento. Se a chave já existe, o serviço descarta o evento. Se não existe, o serviço guarda a chave no Redis por 24h e publica o evento no Kafka.

![Diagrama de containers: pipeline de ingestão com o serviço de deduplicação](diagrams/architecture.svg)

*Imagem a renderizar na passagem manual, a partir do DSL em `diagrams/architecture.dsl`.*

<details>
<summary>Fonte do diagrama (Structurizr DSL)</summary>

```
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
```

</details>

Os produtores enviam eventos ao ingestor, como hoje. O ingestor passa a encaminhar cada evento ao serviço de deduplicação em vez de publicá-lo direto no Kafka. O serviço de deduplicação usa o Redis para saber se já viu a chave idempotente do evento nas últimas 24h e publica no Kafka só os eventos que ainda não viu. Os relatórios de faturamento recebem os eventos pelo Kafka.

### Alternativas consideradas

Esta seção não existe no template. Acrescentamos porque o time pesou alternativas que o template não tem onde registrar.

- **Não fazer nada.** Os produtores continuam reenviando e 4% dos eventos chegam duplicados, o que segue inflando os relatórios de faturamento. O financeiro já reclamou duas vezes.
- **Deduplicar no consumidor.** Descartada, porque cada consumidor teria que reimplementar a deduplicação.
- **Usar a idempotência nativa do produtor Kafka.** Descartada, porque ela não cobre o reenvio entre reinícios do produtor.

## Riscos

| Risco | Mitigação |
|---|---|
| O serviço adiciona um salto ao caminho crítico da ingestão, estimado em +5ms de latência. | O time aceitou esse custo em troca da redução de duplicatas. Nenhuma mitigação adicional definida. |

Outros riscos ainda não foram levantados com o autor. Veja as Perguntas abertas.

## Métricas de sucesso

Reduzir as duplicatas de 4% (medição do mês passado) para menos de 0,1%.

## Perguntas abertas

- Qual o número sequencial deste documento (DD-2026-<seq>)?
- Quem revisa este documento?
- O que o serviço faz quando o Redis está indisponível: descarta nada e publica tudo, ou bloqueia a ingestão?
- O que acontece com um evento repetido que chega depois das 24h de retenção da chave?
- Qual campo ou combinação de campos forma a chave idempotente, e quem a define, o produtor ou o ingestor?
- Quantas instâncias do serviço rodam, e como o serviço lida com dois eventos iguais chegando ao mesmo tempo?
- Como medimos a taxa de duplicatas depois do lançamento, e com que periodicidade?
- Existe plano de rollout (fases, critério de avanço, rollback)? Se sim, entra na seção "Plano de rollout" do template.
- Este doc está ligado a uma história do backlog? Se sim, entra a seção "Critérios de aceite".
- Algum outro risco além da latência deve entrar em Riscos?
