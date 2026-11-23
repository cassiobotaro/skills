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

Os produtores reenviam eventos em caso de retry, e o pipeline de ingestão recebe essas duplicatas. No mês passado medimos 4% de eventos duplicados. As duplicatas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes.

## Proposta

Vamos criar um serviço de deduplicação entre o ingestor e o Kafka. Para cada evento recebido, o serviço consulta no Redis a chave idempotente do evento. Se a chave já existe, o serviço descarta o evento como repetido. Se não existe, o serviço grava a chave no Redis com validade de 24 horas e repassa o evento ao Kafka.

Com isso, a deduplicação acontece uma única vez, antes do Kafka, e nenhum consumidor precisa tratar repetidos.

O custo aceito é um salto a mais no caminho crítico da ingestão. Estimamos +5ms de latência por evento.

## Alternativas consideradas

Esta seção não existe no template. Foi adicionada para registrar as alternativas discutidas, com a ordem das demais seções preservada.

- **Deduplicar no consumidor.** Descartada. Cada consumidor teria que reimplementar a deduplicação.
- **Idempotência nativa do produtor Kafka.** Descartada. Ela não cobre o reenvio entre reinícios do produtor.

## Riscos

- **Latência no caminho crítico.** O novo salto adiciona cerca de 5ms por evento (estimativa). A equipe aceitou esse custo em troca da redução de duplicatas.

Os demais riscos da proposta e suas mitigações estão em [Perguntas abertas](#perguntas-abertas).

## Plano de rollout

As fases, os critérios de avanço e os critérios de rollback estão em [Perguntas abertas](#perguntas-abertas).

## Métricas de sucesso

- Taxa de eventos duplicados abaixo de 0,1% (linha de base: 4% no mês passado).
- Latência adicional na ingestão próxima da estimativa de +5ms. O limite aceitável está em [Perguntas abertas](#perguntas-abertas).

## Perguntas abertas

Riscos
1. O que acontece com a ingestão quando o Redis fica indisponível: o serviço descarta, repassa sem deduplicar ou bloqueia?
2. O que o serviço faz se falhar depois de gravar a chave no Redis e antes de entregar o evento ao Kafka? O evento se perderia ou seria reenviado?
3. Qual é a mitigação para a perda de chaves no Redis (reinício, eviction), que reabre a janela de duplicatas?
4. Duplicatas que chegam depois de 24h passam. Essa janela é suficiente para os reenvios observados?
5. Quem produz a chave idempotente de cada evento, e todos os produtores já a enviam?

Rollout
6. Quais são as fases (por exemplo, por produtor ou por percentual de tráfego), e qual critério avança cada uma?
7. Qual critério dispara o rollback, e como o serviço é desligado sem perder eventos?

Métricas
8. Qual é o limite aceitável de latência (p50, p99) além dos +5ms estimados?
9. Como e onde medimos a taxa de duplicatas, para comparar com os 4% de hoje?

Documento
10. Quem são os revisores?
