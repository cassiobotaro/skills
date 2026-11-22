# Serviço de deduplicação de eventos · DD-2026-<seq>

| | |
|---|---|
| **Documento** | DD-2026-<seq> (aguarda a pergunta 1) |
| **Estado** | Rascunho |
| **Autores** | Rafael Nunes |
| **Revisores** | Aguarda a pergunta 2 |
| **Criado em** | 2026-11-22 |
| **Última atualização** | 2026-11-22 |

## Motivação

O pipeline de ingestão recebe eventos duplicados dos produtores, que reenviam o mesmo evento quando fazem retry. No mês passado, medimos 4% de duplicatas. Elas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes.

## Proposta

Criamos um serviço de deduplicação entre o ingestor e o Kafka. Para cada evento recebido, o serviço consulta a chave idempotente do evento no Redis. Se a chave já existe, o serviço descarta o evento como repetido. Se não existe, o serviço guarda a chave por 24 horas e repassa o evento ao Kafka.

Os detalhes de como o serviço obtém a chave, do comportamento quando o Redis fica indisponível e do formato da chave aguardam resposta (perguntas 3 e 4).

### Trade-offs da solução escolhida

- ✓ A deduplicação acontece uma vez, antes do Kafka, e nenhum consumidor precisa reimplementá-la.
- ✓ Cobre o reenvio entre reinícios do produtor.
- ✗ O serviço vira mais um salto no caminho crítico da ingestão. Estimamos +5ms de latência. Aceitamos esse custo.

### Alternativas consideradas

- **Deduplicar no consumidor** (descartada): cada consumidor teria que reimplementar a deduplicação.
- **Idempotência nativa do produtor Kafka** (descartada): não cobre o reenvio entre reinícios do produtor.
- **Não fazer nada** (descartada): as duplicatas continuam em 4% e continuam inflando os relatórios de faturamento.

## Riscos

Aguarda resposta. Veja a pergunta 5 em Perguntas abertas.

## Plano de rollout

Aguarda resposta. Veja a pergunta 6 em Perguntas abertas.

## Métricas de sucesso

- Duplicatas abaixo de 0,1% (linha de base: 4% no mês passado).

A forma de medir e a métrica de latência aguardam resposta (pergunta 7).

## Perguntas abertas

1. Qual é o número sequencial deste documento (DD-2026-<seq>)? Só existe o template em `docs/design/`, então não deduzi o próximo.
2. Quem revisa, e de quais áreas? O time de arquitetura aceita o documento, e as áreas impactadas (financeiro, donos dos produtores e consumidores) podem entrar.
3. De onde vem a chave idempotente: os produtores já a enviam em cada evento, ou o ingestor a gera?
4. O que o serviço faz quando o Redis está indisponível: deixa o evento passar, ou rejeita?
5. Quais riscos vocês enxergam e como mitigá-los (por exemplo, a perda de chaves no Redis, a janela de 24h menor que o intervalo de retry)? Liste os que a equipe considera relevantes.
6. Como o serviço entra em produção: em fases, com qual critério de avanço e qual de rollback?
7. Como mediremos a taxa de duplicatas depois do lançamento, e há um limite aceitável para a latência além dos +5ms estimados?
