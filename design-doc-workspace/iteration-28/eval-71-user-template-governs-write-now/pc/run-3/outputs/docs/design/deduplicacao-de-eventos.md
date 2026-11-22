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

O pipeline de ingestão recebe eventos duplicados dos produtores, que reenviam o mesmo evento quando fazem retry. No mês passado medimos 4% de eventos duplicados. As duplicatas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes.

## Proposta

Vamos criar um serviço de deduplicação que fica entre o ingestor e o Kafka. Para cada evento recebido, o serviço consulta a chave idempotente do evento no Redis. Se a chave já existe, o serviço descarta o evento. Se não existe, o serviço registra a chave no Redis e o evento segue para o Kafka. O Redis guarda cada chave por 24 horas, e esse é o intervalo em que um reenvio ainda é reconhecido como duplicata.

## Alternativas consideradas

O template não tem uma seção para alternativas. Acrescentei esta seção entre Proposta e Riscos, sem mexer na ordem das seções do template.

| Alternativa | Por que foi descartada |
|---|---|
| Deduplicar em cada consumidor | Cada consumidor teria que reimplementar a deduplicação. |
| Usar a idempotência nativa do produtor Kafka | Não cobre o reenvio entre reinícios do produtor. |

## Riscos

Latência no caminho crítico (custo aceito). O serviço adiciona um salto ao caminho crítico da ingestão. Estimamos +5 ms de latência por evento. A equipe aceitou esse custo.

Os demais riscos e as mitigações aguardam resposta do autor (ver Perguntas abertas, 1).

## Plano de rollout

As fases, os critérios de avanço e o critério de rollback aguardam resposta do autor (ver Perguntas abertas, 2).

## Métricas de sucesso

| Métrica | Linha de base | Meta |
|---|---|---|
| Taxa de eventos duplicados | 4% (mês passado) | abaixo de 0,1% |

A latência adicional de +5 ms é uma estimativa, não uma meta. O método de medição da taxa de duplicatas e o limite aceitável de latência aguardam resposta do autor (ver Perguntas abertas, 3).

## Perguntas abertas

1. Riscos. O que pode dar errado com o serviço e como mitigamos? Em particular: o que acontece com a ingestão se o Redis ficar indisponível (descarta a deduplicação e deixa passar, ou bloqueia)? E o serviço em si, como fica a disponibilidade dele sendo mais um salto no caminho crítico?
2. Plano de rollout. Como o serviço entra em produção? Quais são as fases (por exemplo, por produtor ou por percentual de tráfego), o critério para avançar de uma fase à seguinte e o critério para fazer rollback?
3. Métricas. Como medimos a taxa de duplicatas depois do serviço (mesma medição do 4%)? A estimativa de +5 ms vem de medição ou de cálculo, e existe um limite de latência a partir do qual a proposta deixa de valer?
4. Chave idempotente. Quem gera a chave de cada evento (produtor ou ingestor) e todos os produtores já a enviam hoje?
5. Janela de 24h. O que acontece com um reenvio que chega depois de 24 horas, e isso é aceitável para o faturamento? De onde veio o valor de 24 horas?
6. Escopo. O que fica fora desta proposta? Por exemplo, os 0,1% restantes ou duplicatas que já estão no Kafka.
7. Fazer nada. Há algo além do problema do faturamento que descarta manter o cenário atual, ou o custo é só o descrito na Motivação?
8. Revisores e numeração. Quem revisa o doc na arquitetura? DD-2026-001 assume que este é o primeiro doc do ano, porque `docs/design/` só tinha o template. Confirma a sequência?
