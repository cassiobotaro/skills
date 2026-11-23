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

Quando um produtor faz retry, ele reenvia o evento, e o pipeline de ingestão recebe o reenvio como se fosse um evento novo. No mês passado medimos 4% de eventos duplicados. As duplicatas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes.

## Proposta

Vamos construir um serviço de deduplicação que fica entre o ingestor e o Kafka. O serviço guarda no Redis, por 24 horas, a chave idempotente de cada evento que recebe. Quando chega um evento cuja chave já está no Redis, o serviço descarta o evento como repetido; os demais seguem para o Kafka.

A deduplicação fica em um único ponto do pipeline, e os consumidores não precisam reimplementá-la.

### Custo aceito

O serviço acrescenta mais um salto no caminho crítico da ingestão. Estimamos um acréscimo de 5 ms de latência, e o time aceitou esse custo em troca de resolver a deduplicação em um único ponto do pipeline.

## Alternativas consideradas

O template não tem seção para alternativas. Esta seção foi acrescentada para registrar as opções que o time discutiu e por que cada uma perdeu.

| Alternativa | Por que foi descartada |
|---|---|
| Não fazer nada | Mantém os 4% de duplicatas inflando os relatórios de faturamento, problema que o financeiro já apontou duas vezes. |
| Deduplicar no consumidor | Cada consumidor teria que reimplementar a deduplicação. |
| Idempotência nativa do produtor Kafka | Não cobre o reenvio que acontece entre reinícios do produtor. |
| **Serviço de deduplicação entre o ingestor e o Kafka (escolhida)** | Resolve em um único ponto, ao custo de +5 ms estimados no caminho crítico (ver [Custo aceito](#custo-aceito)). |

## Riscos

Os riscos da proposta e as respectivas mitigações ainda não foram levantados. Ver [Perguntas abertas](#perguntas-abertas), item 3.

## Plano de rollout

Fases, critério de avanço e critério de rollback estão pendentes. Ver [Perguntas abertas](#perguntas-abertas), item 4.

## Métricas de sucesso

| Métrica | Hoje | Meta |
|---|---|---|
| Percentual de eventos duplicados que chegam ao Kafka | 4% (mês passado) | abaixo de 0,1% |

## Perguntas abertas

1. **Numeração.** Este é o primeiro design doc em `docs/design/`, por isso recebeu DD-2026-001. Se a coleção do time vive em outro lugar, qual é o próximo número da sequência?
2. **Revisores.** Quem deve revisar este documento, e de quais áreas (arquitetura, plataforma, time dono do Redis, financeiro)?
3. **Riscos.** Quais riscos o time enxerga nesta proposta, e qual é a mitigação de cada um?
4. **Rollout.** Como o serviço entra em produção: em quais fases, com qual critério para avançar de fase e qual critério para fazer rollback?
5. **Medição.** Como os 4% foram medidos, e como vamos medir a meta de 0,1%? Existe prazo para atingir a meta?
6. **Chave idempotente.** Quem gera a chave de cada evento? Todos os produtores já enviam essa chave hoje?
7. **Janela de 24 horas.** Como o time chegou a 24 horas? Essa janela cobre todos os reenvios observados?
8. **Latência.** De onde vem a estimativa de +5 ms? Existe um teto de latência que o caminho de ingestão não pode ultrapassar?
9. **Descarte.** O que o serviço devolve ao ingestor quando descarta um evento repetido? O descarte fica registrado em algum lugar?
10. **Ordem das operações.** Em que ordem o serviço grava a chave no Redis e publica o evento no Kafka?
11. **Redis.** O serviço usa um Redis já existente ou uma instância nova? Qual time opera esse Redis?
12. **Escopo.** Corrigir os relatórios de faturamento já afetados pelas duplicatas faz parte deste trabalho, ou fica fora do escopo?
13. **Diagrama.** O documento deve ganhar um diagrama da arquitetura (produtores, ingestor, serviço de deduplicação, Redis, Kafka) para a revisão da arquitetura?
