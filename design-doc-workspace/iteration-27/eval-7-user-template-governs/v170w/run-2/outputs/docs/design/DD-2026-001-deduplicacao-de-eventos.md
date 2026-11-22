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

Vamos criar um serviço de deduplicação entre o ingestor e o Kafka. Para cada evento recebido, o serviço consulta a chave idempotente do evento no Redis. Se a chave já existe, o serviço descarta o evento. Se não existe, o serviço guarda a chave e o evento segue para o Kafka. O Redis mantém cada chave por 24 horas.

Como a deduplicação acontece uma vez, antes do Kafka, nenhum consumidor precisa tratar duplicatas. Como a chave fica no Redis e não na memória do produtor, o serviço reconhece um reenvio feito depois de um reinício do produtor. A janela de 24 horas define o alcance: o serviço não reconhece um reenvio que chegue depois dela.

### Trade-offs

- ✓ A deduplicação existe em um só lugar, e os consumidores não a reimplementam.
- ✓ Cobre o reenvio entre reinícios do produtor, que a idempotência nativa do produtor Kafka não cobre.
- ✗ O serviço é mais um salto no caminho crítico da ingestão. Estimamos +5 ms de latência. O time aceita esse custo.
- ✗ Um reenvio fora da janela de 24 horas passa como evento novo.

### Alternativas consideradas

| Alternativa | Resultado | Motivo |
|---|---|---|
| Não fazer nada | ✗ Descartada | Os 4% de duplicatas continuam inflando o faturamento, e o financeiro já reclamou duas vezes. |
| Deduplicar no consumidor | ✗ Descartada | Cada consumidor teria que reimplementar a deduplicação. |
| Idempotência nativa do produtor Kafka | ✗ Descartada | Não cobre o reenvio entre reinícios do produtor. |
| **Serviço de deduplicação com Redis** | ✓ Escolhida | Deduplica em um só lugar e cobre o reenvio entre reinícios. O custo é o salto extra. |

## Riscos

| Risco | Mitigação |
|---|---|
| +5 ms de latência no caminho crítico da ingestão (estimativa, ainda não medida). | O time aceita o custo. Vamos medir a latência real no rollout (ver Métricas de sucesso). |
| Falha do serviço ou do Redis no caminho crítico. | Indefinida. Ver Perguntas abertas. |
| Reenvio depois da janela de 24 horas. | Indefinida. Ver Perguntas abertas. |

## Plano de rollout

As fases, os critérios de avanço e o rollback ainda não existem. Estão nas Perguntas abertas.

## Métricas de sucesso

| Métrica | Base | Meta |
|---|---|---|
| Taxa de eventos duplicados | 4% (mês passado) | Abaixo de 0,1% |
| Latência adicionada na ingestão | Estimativa de +5 ms | Medir e comparar com a estimativa |

## Perguntas abertas

1. Quem revisa este documento? Arquitetura, financeiro e os times donos dos produtores e dos consumidores entram na lista?
2. Qual é a chave idempotente? Quem a gera, o produtor ou o ingestor, e ela já existe em todos os eventos hoje?
3. Qual é a ordem entre guardar a chave no Redis e publicar no Kafka? Se o serviço guarda a chave e falha antes de publicar, o retry do produtor é descartado e o evento se perde.
4. O que acontece com a ingestão quando o serviço ou o Redis fica indisponível: o evento passa sem deduplicação ou a ingestão para?
5. Por quanto tempo os produtores reenviam um evento? A janela de 24 horas cobre esse período?
6. Como o serviço escala, e o Redis tem alta disponibilidade ou persistência? O que acontece com as chaves se o Redis reinicia?
7. Como medimos a taxa de duplicatas e a latência adicionada: com que instrumento, e em que ponto do pipeline?
8. Como o serviço entra em produção: em fases, com que critério de avanço, e como volta atrás se algo falhar?
9. O serviço fica em um repositório novo ou dentro do ingestor, e qual time o opera?
