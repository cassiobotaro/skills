# Serviço de deduplicação de eventos · DD-2026-<seq>

| | |
|---|---|
| **Documento** | DD-2026-<seq> |
| **Estado** | Rascunho |
| **Autores** | Rafael Nunes |
| **Revisores** | |
| **Criado em** | 2026-11-22 |
| **Última atualização** | 2026-11-22 |

## Motivação

O pipeline de ingestão recebe eventos duplicados dos produtores, que reenviam o mesmo evento quando fazem retry. No mês passado medimos 4% de eventos duplicados. As duplicatas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes.

## Proposta

Criamos um serviço de deduplicação entre o ingestor e o Kafka. Para cada evento recebido, o serviço consulta a chave idempotente do evento no Redis. Se a chave já existe, o serviço descarta o evento. Se não existe, o serviço guarda a chave por 24 horas e deixa o evento seguir para o Kafka.

Com isso a deduplicação acontece uma vez, antes do Kafka, e os consumidores recebem o fluxo já sem repetidos.

### Trade-off aceito

O serviço é mais um salto no caminho crítico da ingestão. Estimamos +5ms de latência por evento. O time aceita esse custo em troca de eliminar as duplicatas na entrada, num único lugar.

## Alternativas consideradas

| Alternativa | Resultado | Motivo |
|---|---|---|
| Deduplicar no consumidor | ✗ Descartada | Cada consumidor teria que reimplementar a deduplicação. |
| Idempotência nativa do produtor Kafka | ✗ Descartada | Não cobre o reenvio entre reinícios do produtor. |
| Serviço de deduplicação entre o ingestor e o Kafka | ✓ Escolhida | Deduplica uma vez, na entrada. Custa +5ms no caminho crítico. |

A alternativa de não fazer nada segue o problema descrito em Motivação: os 4% de duplicatas continuam inflando o faturamento.

## Riscos

- **Latência no caminho crítico.** O novo salto adiciona cerca de 5ms (estimativa) a cada evento. É o custo aceito descrito na Proposta.

Os demais riscos e suas mitigações dependem de informação que ainda não temos. As perguntas estão em Perguntas abertas.

## Plano de rollout

Ainda não definido. As perguntas estão em Perguntas abertas.

## Métricas de sucesso

- Taxa de eventos duplicados abaixo de 0,1% (hoje: 4%, medida no mês passado).
- Latência adicional de ingestão próxima da estimada de +5ms.

## Perguntas abertas

**Riscos**

1. O que acontece com a ingestão se o Redis ficar indisponível: o serviço deixa passar os eventos sem deduplicar ou bloqueia a ingestão?
2. Como o serviço deve tratar um reenvio que chega depois das 24h de retenção da chave?
3. Há outros riscos que o time já discutiu (perda de dados do Redis, capacidade, evento descartado por engano)? Qual a mitigação de cada um?

**Plano de rollout**

4. A entrada em produção é de uma vez ou em fases (por exemplo, por produtor)?
5. Qual o critério para avançar de uma fase à seguinte e qual o critério e o procedimento de rollback?

**Métricas de sucesso**

6. Como medimos a taxa de duplicatas depois do serviço (mesma metodologia dos 4% do mês passado)? Em que janela e com que prazo após o lançamento a meta de 0,1% deve ser atingida?
7. A latência de +5ms é um limite aceitável (com alerta) ou só uma estimativa a confirmar?

**Cabeçalho**

8. Qual é o número de sequência deste documento (DD-2026-`<seq>`)?
9. Quem deve revisar? Sugestão: as áreas de infraestrutura (Redis e Kafka), o financeiro (consumidor dos relatórios de faturamento) e as equipes produtoras dos eventos.
