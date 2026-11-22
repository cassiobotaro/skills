# Serviço de deduplicação de eventos · DD-2026-<seq>

| | |
|---|---|
| **Documento** | DD-2026-<seq> (aguarda a sequência, ver Perguntas abertas) |
| **Estado** | Rascunho |
| **Autores** | Rafael Nunes |
| **Revisores** | |
| **Criado em** | 2026-11-22 |
| **Última atualização** | 2026-11-22 |

## Motivação

Os produtores reenviam eventos quando fazem retry, e o pipeline de ingestão recebe esses eventos duplicados. No mês passado medimos 4% de duplicatas. Elas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes.

## Proposta

Um novo serviço de deduplicação fica entre o ingestor e o Kafka. Para cada evento recebido, o serviço consulta a chave idempotente do evento no Redis. Se a chave já existe, o serviço descarta o evento. Se não existe, guarda a chave no Redis por 24 horas e encaminha o evento ao Kafka.

### Trade-off aceito

O serviço adiciona um salto ao caminho crítico da ingestão, estimado em +5ms de latência. O time aceitou esse custo em troca de eliminar as duplicatas antes que cheguem ao Kafka, num ponto único, sem que cada consumidor trate o problema.

### Alternativas consideradas

O template não tem seção para alternativas, então esta seção foi acrescentada, mantendo as seções do template na ordem original.

- **Deduplicar no consumidor.** Descartada: cada consumidor teria que reimplementar a deduplicação.
- **Usar a idempotência nativa do produtor Kafka.** Descartada: ela não cobre o reenvio entre reinícios do produtor.

## Riscos

Aguarda resposta do autor: quais riscos o time enxerga e como mitiga cada um (pergunta 1 em Perguntas abertas).

## Plano de rollout

Aguarda resposta do autor: fases, critério de avanço e de rollback (pergunta 2 em Perguntas abertas).

## Métricas de sucesso

- Duplicatas abaixo de 0,1% (linha de base: 4% no mês passado).

O custo de latência estimado (+5ms) ainda não tem um limite de aceitação definido (pergunta 3 em Perguntas abertas).

## Perguntas abertas

1. **Riscos:** o que pode dar errado com esta proposta e como mitigamos cada risco? Por exemplo, o que acontece com a ingestão quando o serviço ou o Redis ficam indisponíveis?
2. **Plano de rollout:** como o serviço entra em produção, em quais fases, com qual critério de avanço e de rollback?
3. **Latência:** os +5ms são uma estimativa. Há um limite máximo aceitável, e como vamos medir o valor real?
4. **Numeração:** qual é o número de sequência deste documento (DD-2026-?) e quem são os revisores?
5. **Fazer nada:** a alternativa de manter o cenário atual foi considerada e descartada pelo custo das duplicatas no faturamento, ou há outro motivo a registrar?
