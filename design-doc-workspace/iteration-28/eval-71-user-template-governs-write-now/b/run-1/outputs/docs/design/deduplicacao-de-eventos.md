# Serviço de deduplicação de eventos · DD-2026-<seq>

| | |
|---|---|
| **Documento** | DD-2026-<seq> (número aguarda resposta, ver pergunta 1) |
| **Estado** | Rascunho |
| **Autores** | Rafael Nunes |
| **Revisores** | Aguarda resposta (pergunta 2) |
| **Criado em** | 2026-11-22 |
| **Última atualização** | 2026-11-22 |

## Motivação

O pipeline de ingestão recebe eventos duplicados dos produtores, que reenviam o mesmo evento em caso de retry. No mês passado, medimos 4% de eventos duplicados. As duplicatas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes.

### Metas

- Reduzir as duplicatas que chegam ao Kafka de 4% para menos de 0,1%.

O que fica fora do escopo aguarda resposta (pergunta 3).

## Proposta

Criamos um serviço de deduplicação que fica entre o ingestor e o Kafka. Para cada evento, o serviço consulta a chave idempotente no Redis. Ele guarda cada chave por 24 horas e descarta os eventos cuja chave já existe.

Como a deduplicação acontece antes do Kafka, os consumidores recebem o fluxo já sem repetidos e não precisam implementar nada.

Detalhes do fluxo (o que define a chave idempotente, o que o serviço faz quando o Redis não responde) aguardam resposta (perguntas 4 e 5).

### Trade-offs aceitos

- ✓ A deduplicação fica em um único ponto, em vez de em cada consumidor.
- ✓ Cobre o reenvio dos produtores mesmo entre reinícios deles, caso que a idempotência nativa do produtor Kafka não cobre.
- ✗ O serviço é mais um salto no caminho crítico da ingestão. Estimamos +5ms de latência, e o time aceitou esse custo.

### Alternativas consideradas

- **Não fazer nada.** Os relatórios de faturamento seguem inflados por 4% de duplicatas, e o financeiro já reclamou duas vezes.
- **Deduplicar no consumidor.** Descartada: cada consumidor teria que reimplementar a deduplicação.
- **Idempotência nativa do produtor Kafka.** Descartada: não cobre o reenvio entre reinícios do produtor.
- **Serviço entre o ingestor e o Kafka, com chaves no Redis por 24h.** Escolhida.

## Riscos

Aguarda resposta (pergunta 5). O único custo que o time já declarou é a latência de +5ms, registrada em Trade-offs aceitos.

## Plano de rollout

Aguarda resposta (pergunta 6).

## Métricas de sucesso

- Taxa de eventos duplicados abaixo de 0,1% (linha de base: 4% no mês passado).

Como e onde medimos essa taxa aguarda resposta (pergunta 7).

## Perguntas abertas

1. Qual é o número deste documento (DD-2026-<seq>)? Não há outros design docs no repositório para continuar a sequência.
2. Quem revisa, e de quais áreas? A arquitetura aceita o documento, e talvez o financeiro e os times dos consumidores também devam revisar.
3. O que fica explicitamente fora do escopo desta entrega?
4. O que compõe a chave idempotente de um evento, e quem a gera?
5. O que pode dar errado com esta proposta e como mitigamos cada risco? Em particular, o que o serviço faz quando o Redis está indisponível, e o que acontece com um duplicado que chega depois das 24h?
6. Como o serviço entra em produção: em fases ou de uma vez? Qual o critério de avanço e qual o plano de rollback?
7. Como e onde medimos a taxa de duplicatas para comparar com a meta de 0,1%? A medição de 4% usou o mesmo método?
