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

O pipeline de ingestão recebe eventos duplicados dos produtores, que reenviam o mesmo evento quando fazem retry. No mês passado medimos 4% de duplicatas. Elas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes.

## Proposta

Criamos um serviço de deduplicação entre o ingestor e o Kafka. Para cada evento recebido, o serviço consulta a chave idempotente do evento no Redis. Se a chave já existe, o serviço descarta o evento. Se não existe, o serviço guarda a chave no Redis por 24 horas e encaminha o evento ao Kafka.

Como a deduplicação acontece antes do Kafka, os consumidores não precisam implementar nada.

### Trade-offs da proposta

- ✓ A deduplicação fica em um só lugar, antes do Kafka, e nenhum consumidor a reimplementa.
- ✓ Cobre o reenvio entre reinícios do produtor.
- ✗ O serviço entra como mais um salto no caminho crítico da ingestão. Estimamos +5ms de latência. A equipe aceitou esse custo.

### Alternativas consideradas

| Alternativa | Resultado | Motivo |
|---|---|---|
| Não fazer nada | ✗ Descartada | 4% de duplicatas continuam inflando os relatórios de faturamento, e o financeiro já reclamou duas vezes. |
| Deduplicar no consumidor | ✗ Descartada | Cada consumidor teria que reimplementar a deduplicação. |
| Idempotência nativa do produtor Kafka | ✗ Descartada | Não cobre o reenvio entre reinícios do produtor. |
| **Serviço de deduplicação com Redis (escolhida)** | ✓ | Centraliza a deduplicação e cobre o reenvio entre reinícios, ao custo de +5ms no caminho crítico. |

## Riscos

- **Latência no caminho crítico.** O novo salto acrescenta cerca de 5ms (estimativa, ainda não medida) a cada evento ingerido. A equipe aceitou o custo. A mitigação está nas Perguntas abertas.

Os demais riscos e suas mitigações dependem de informação que ainda falta. Ver Perguntas abertas.

## Plano de rollout

O plano ainda não foi definido. Ver Perguntas abertas.

## Métricas de sucesso

- Duplicatas abaixo de 0,1% dos eventos (hoje: 4%, medido no mês passado).
- Latência adicional de ingestão próxima da estimativa de +5ms. O limite aceitável ainda não foi definido (ver Perguntas abertas).

## Perguntas abertas

**Revisores**
1. Quem do time de arquitetura e de quais áreas (por exemplo, financeiro, plataforma, donos do Redis e do Kafka) deve revisar este documento?

**Riscos**
2. O que acontece com a ingestão se o Redis ficar indisponível ou lento: o serviço descarta, deixa passar eventos sem deduplicar ou bloqueia a ingestão?
3. Como a equipe mitiga a latência de +5ms, e qual é o teto de latência aceitável no caminho crítico?
4. Existe risco para a meta de 0,1% com a janela de 24h, por exemplo reenvios que chegam depois de 24 horas? Quais riscos adicionais a equipe enxerga e como cada um é mitigado?

**Plano de rollout**
5. Como o serviço entra em produção: em fases? Qual o critério para avançar de uma fase para a seguinte e qual o critério e o procedimento de rollback?

**Métricas de sucesso**
6. Como e onde a taxa de duplicatas e a latência adicional serão medidas em produção, e quem acompanha?

**Proposta**
7. Como é definida a chave idempotente de um evento e quem a gera (produtor ou ingestor)?
8. O serviço roda em quantas instâncias e o Redis é compartilhado com outros sistemas ou dedicado?

**Documento**
9. O número DD-2026-001 está correto? Não há outros documentos na pasta para continuar a sequência.
