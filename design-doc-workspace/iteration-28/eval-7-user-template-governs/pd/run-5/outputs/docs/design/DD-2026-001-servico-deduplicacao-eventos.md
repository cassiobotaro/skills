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

Os produtores reenviam eventos quando fazem retry, e o pipeline de ingestão recebe essas cópias como se fossem eventos novos. No mês passado, medimos 4% de eventos duplicados na ingestão.

As duplicatas inflam os relatórios de faturamento. O financeiro já reclamou duas vezes.

## Proposta

Criamos um serviço de deduplicação entre o ingestor e o Kafka. Para cada evento recebido do ingestor, o serviço consulta a chave idempotente do evento no Redis. Se a chave já existe, o serviço descarta o evento. Se não existe, o serviço guarda a chave no Redis por 24 horas e o evento segue para o Kafka. Eventos reenviados dentro dessa janela de 24 horas são descartados antes de chegar a qualquer consumidor.

Como a deduplicação acontece antes do Kafka, os consumidores recebem o fluxo já deduplicado e não precisam implementar nada.

A definição de quem gera a chave idempotente, a ordem entre gravar a chave e publicar no Kafka e o comportamento em caso de falha estão em [Perguntas abertas](#perguntas-abertas).

### Alternativas consideradas

Esta seção não existe no template. Mantemos aqui as alternativas que o time discutiu, para que o motivo do descarte fique registrado.

| Alternativa | Por que foi descartada |
|---|---|
| Deduplicar no consumidor | Cada consumidor teria que reimplementar a deduplicação. |
| Usar a idempotência nativa do produtor Kafka | Ela não cobre o reenvio entre reinícios do produtor. |

A alternativa de não fazer nada ainda não foi avaliada neste documento. Ela fica em [Perguntas abertas](#perguntas-abertas).

## Riscos

O custo que o time aceitou é um salto a mais no caminho crítico da ingestão. Estimamos +5ms de latência por evento. Essa é uma estimativa, ainda não uma medição.

Os demais riscos ainda não foram levantados. Estão em [Perguntas abertas](#perguntas-abertas).

## Plano de rollout

O plano ainda não foi definido. Veja [Perguntas abertas](#perguntas-abertas).

## Métricas de sucesso

Reduzir as duplicatas na ingestão de 4% (medição do mês passado) para menos de 0,1%.

O método de medição está em [Perguntas abertas](#perguntas-abertas).

## Perguntas abertas

**Riscos**

- O que acontece com a ingestão se o Redis ficar indisponível: o serviço bloqueia, deixa passar eventos sem deduplicar, ou outra política?
- Se o serviço gravar a chave no Redis e a publicação no Kafka falhar, o reenvio do produtor seria descartado como duplicata. Qual é a ordem entre gravar a chave e publicar, e que garantia de entrega queremos?
- Qual é o impacto de um reenvio que chega depois da janela de 24 horas?
- Que outros riscos o time enxerga, e qual a mitigação de cada um (incluindo a latência de +5ms)?

**Desenho**

- Quem gera a chave idempotente: o produtor ou o ingestor? Como ela é composta?
- Qual a avaliação de "não fazer nada" como alternativa, dado o impacto no faturamento?

**Rollout**

- Em quais fases o serviço entra em produção, com qual critério de avanço e qual critério de rollback?

**Métricas**

- Como mediremos a taxa de duplicatas depois do lançamento (mesma metodologia da medição de 4%)?
- Qual o limite aceitável de latência adicional, e como vamos medi-la?

**Revisão**

- Quem são os revisores do documento?
