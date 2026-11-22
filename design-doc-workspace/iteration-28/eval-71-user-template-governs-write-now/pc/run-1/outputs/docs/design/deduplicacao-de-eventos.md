# Serviço de deduplicação de eventos · DD-2026-001

| | |
|---|---|
| **Documento** | DD-2026-001 |
| **Estado** | Rascunho |
| **Autores** | Rafael Nunes |
| **Revisores** | |
| **Criado em** | 2026-11-22 |
| **Última atualização** | 2026-11-22 |

## Motivação

O pipeline de ingestão recebe eventos duplicados dos produtores, que reenviam o mesmo evento quando fazem retry. Em outubro de 2026, 4% dos eventos recebidos eram duplicatas. As duplicatas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes.

## Proposta

Criamos um serviço de deduplicação que fica entre o ingestor e o Kafka. Para cada evento recebido, o serviço consulta a chave idempotente do evento no Redis. Se a chave já existe, o serviço descarta o evento. Se não existe, o serviço guarda a chave no Redis por 24 horas e entrega o evento ao Kafka.

O custo aceito é um salto a mais no caminho crítico da ingestão. A estimativa é de +5 ms de latência por evento.

Detalhes do serviço (origem da chave idempotente, comportamento quando o Redis não responde, garantias de atomicidade entre o Redis e o Kafka) aguardam resposta, ver as perguntas 2 e 3 em Perguntas abertas.

## Alternativas consideradas

Esta seção não consta do template e entra entre Proposta e Riscos.

Deduplicar no consumidor: descartada. Cada consumidor teria que reimplementar a deduplicação.

Idempotência nativa do produtor Kafka: descartada. Ela não cobre o reenvio entre reinícios do produtor.

## Riscos

Latência no caminho crítico. O serviço adiciona um salto entre o ingestor e o Kafka, estimado em +5 ms. O time aceitou esse custo em troca da redução de duplicatas.

Os demais riscos e suas mitigações aguardam resposta, ver a pergunta 3 em Perguntas abertas.

## Plano de rollout

Aguarda resposta, ver a pergunta 4 em Perguntas abertas.

## Métricas de sucesso

| Métrica | Antes | Meta |
|---|---|---|
| Duplicatas na ingestão | 4% (outubro de 2026) | abaixo de 0,1% |

## Perguntas abertas

1. Numeração e revisores. Usei DD-2026-001 porque não há outros docs em `docs/design/`. Esse é o número correto? Quem são os revisores da arquitetura?
2. Chave idempotente. Quem gera a chave de cada evento, o produtor ou o ingestor? Ela já existe hoje em todos os eventos?
3. Riscos e falhas. O que acontece com a ingestão se o Redis ficar indisponível: o serviço descarta, deixa passar ou bloqueia? Quais outros riscos o time identificou, e qual é a mitigação de cada um?
4. Rollout. Em que fases o serviço entra em produção, com qual critério de avanço e qual critério de rollback?
5. Alternativa "não fazer nada". O time quer registrar essa alternativa e a razão de tê-la descartado?
6. Latência. Os +5 ms são uma meta a acompanhar depois do rollout ou só uma estimativa? Se for meta, qual é o limite aceitável?
7. Escopo. Há algo deliberadamente fora do escopo deste serviço?
