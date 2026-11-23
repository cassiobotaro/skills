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

O pipeline de ingestão recebe eventos duplicados dos produtores, que reenviam o mesmo evento quando fazem retry. No mês passado medimos 4% de eventos duplicados. As duplicatas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes.

Hoje nada no caminho da ingestão descarta esses repetidos antes de chegarem ao Kafka, então cada consumidor recebe as duplicatas.

## Proposta

Vamos criar um serviço de deduplicação que fica entre o ingestor e o Kafka. Para cada evento recebido, o serviço consulta no Redis a chave idempotente do evento:

- Se a chave ainda não existe, o serviço a grava no Redis com validade de 24 horas e entrega o evento ao Kafka.
- Se a chave já existe, o evento é um repetido e o serviço o descarta.

Como a deduplicação acontece antes do Kafka, os consumidores recebem o fluxo já sem repetidos e não precisam implementar nada. A janela de 24 horas define até quando um reenvio ainda é reconhecido como duplicata.

### Alternativas consideradas

Este template não tem seção para alternativas. Adicionei esta, dentro de Proposta, para registrar por que a escolha foi essa.

- **Deduplicar no consumidor.** Descartada: cada consumidor teria que reimplementar a deduplicação.
- **Idempotência nativa do produtor Kafka.** Descartada: não cobre o reenvio entre reinícios do produtor.
- **Não fazer nada.** Mantém os 4% de duplicatas e o impacto nos relatórios de faturamento. Não foi discutida em detalhe (ver Perguntas abertas).

### Trade-off aceito

O serviço adiciona um salto ao caminho crítico da ingestão. Estimamos +5ms de latência por evento. O time aceita esse custo em troca de uma deduplicação única e central, sem trabalho nos consumidores.

## Riscos

- **Latência no caminho crítico.** Estimamos +5ms por evento, ainda não medidos. Mitigação: medir a latência real antes de ampliar o tráfego (ver Plano de rollout, ainda por definir).

Os demais riscos desta proposta (por exemplo, o comportamento quando o Redis estiver indisponível) ainda não foram discutidos e estão em Perguntas abertas.

## Plano de rollout

Ainda não definido. As fases, os critérios de avanço e de rollback dependem das respostas em Perguntas abertas.

## Métricas de sucesso

- Taxa de eventos duplicados abaixo de 0,1% (linha de base: 4% no mês passado).
- Latência adicional na ingestão próxima da estimativa de +5ms (o limite aceitável ainda não foi definido).

## Perguntas abertas

Proposta
1. De onde vem a chave idempotente de cada evento? O produtor a envia, ou o serviço a calcula a partir do conteúdo?
2. A consulta e a gravação da chave no Redis acontecem em uma única operação atômica? Como o serviço evita que dois reenvios simultâneos passem juntos?
3. O que o serviço responde ao ingestor quando descarta um repetido? O produtor vê isso como sucesso ou como erro?
4. Por que 24 horas? Os reenvios que medimos acontecem todos dentro dessa janela?
5. O serviço é stateless? Quantas instâncias rodam, e o Redis é dedicado a ele?

Alternativas
6. O que foi considerado sobre "não fazer nada" além do impacto no faturamento, por exemplo corrigir só nos relatórios do financeiro?

Riscos
7. O que acontece quando o Redis está indisponível: o serviço deixa passar eventos (fail-open, com duplicatas) ou bloqueia a ingestão (fail-closed)?
8. Qual o risco de descartar um evento legítimo por colisão ou chave reutilizada, e quem arca com essa perda?
9. Como o serviço se comporta se o Redis perder dados (reinício, falha, eviction)? Duplicatas voltariam a passar durante a janela afetada?
10. Qual a capacidade esperada (eventos por segundo, volume de chaves em 24h, memória no Redis)?

Plano de rollout
11. Como entra em produção: por produtor, por percentual de tráfego, em modo sombra (só contando duplicatas, sem descartar) antes de descartar de fato?
12. Qual o critério para avançar de fase e qual dispara o rollback (por exemplo, limite de latência ou de erros)?

Métricas de sucesso
13. Como medimos a taxa de duplicatas depois do serviço? Usamos a mesma medição dos 4%?
14. Qual o limite máximo de latência aceitável no caminho crítico, além da estimativa de +5ms?

Geral
15. Quem revisa este documento (time de arquitetura e financeiro, outros)? Algum outro time é impactado, como produtores, consumidores ou infraestrutura do Redis?
