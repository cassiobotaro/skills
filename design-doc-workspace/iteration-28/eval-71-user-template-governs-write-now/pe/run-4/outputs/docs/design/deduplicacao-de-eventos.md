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

O pipeline de ingestão recebe eventos duplicados dos produtores. A causa é o reenvio em retry: quando um produtor reenvia um evento, o pipeline o processa de novo. No mês passado (outubro de 2026), medimos 4% de eventos duplicados.

As duplicatas inflam os relatórios de faturamento. O financeiro já reclamou duas vezes.

## Proposta

Criamos um serviço de deduplicação que fica entre o ingestor e o Kafka. Todo evento passa por ele antes de chegar ao Kafka.

Para cada evento, o serviço consulta a chave idempotente no Redis. Se a chave já existe, o evento é um repetido e o serviço o descarta. Se não existe, o serviço guarda a chave no Redis com validade de 24 horas e entrega o evento ao Kafka.

Com isso, a deduplicação acontece uma vez, antes do Kafka, e os consumidores recebem um fluxo já sem repetidos. Nenhum consumidor precisa implementar deduplicação por conta própria.

## Alternativas consideradas

Este template não tem seção para alternativas. Mantive a estrutura e a ordem do template e acrescentei esta seção logo após a Proposta.

**Deduplicar no consumidor.** Descartada. Cada consumidor teria que reimplementar a deduplicação.

**Usar a idempotência nativa do produtor Kafka.** Descartada. Ela não cobre o reenvio entre reinícios do produtor, que é um dos casos que geram as duplicatas.

## Riscos

**Latência no caminho crítico.** O serviço adiciona um salto ao caminho crítico da ingestão. Estimamos +5ms de latência por evento. O time aceitou esse custo em troca da remoção das duplicatas.

Outros riscos ainda não foram levantados. Ver Perguntas abertas.

## Plano de rollout

A definir. Ver Perguntas abertas.

## Métricas de sucesso

- Taxa de eventos duplicados abaixo de 0,1%. Ponto de partida: 4%, medido em outubro de 2026.

## Perguntas abertas

1. **Chave idempotente.** Quem gera a chave de cada evento? Os produtores já a enviam hoje, ou o ingestor a deriva do conteúdo do evento?
2. **Falha do Redis.** O que o serviço faz com o evento quando o Redis está indisponível ou lento: deixa passar (aceitando duplicatas) ou bloqueia (aceitando perder vazão)? Com a primeira opção, a meta de 0,1% vale durante a indisponibilidade?
3. **Atomicidade.** Dois reenvios do mesmo evento podem chegar ao mesmo tempo. A verificação e o registro da chave precisam ser uma única operação atômica?
4. **Janela de 24h.** O que acontece com um reenvio que chega depois das 24h? Existe produtor com retry que passe desse prazo? Por que 24h?
5. **Falha do próprio serviço.** Quantas instâncias rodam? O que acontece com o ingestor se o serviço cair? Ele é novo ponto único de falha?
6. **Riscos adicionais.** Há outros riscos que o time já discutiu e que devem entrar na seção Riscos, com a mitigação de cada um?
7. **Latência.** Os +5ms são uma estimativa ou uma medição? Em qual percentil? Existe um orçamento de latência da ingestão que o salto adicional precisa respeitar?
8. **Medição da meta.** Como mediremos a taxa de duplicatas depois do serviço? Usamos o mesmo método que produziu os 4%?
9. **Plano de rollout.** Em quais fases o serviço entra em produção (por exemplo, por produtor ou por percentual de tráfego)? Qual o critério para avançar e qual o gatilho de rollback?
10. **Capacidade do Redis.** Qual o volume de eventos por dia, e quem opera o Redis (instância nova ou compartilhada)?
11. **Impacto em outras equipes.** Os produtores e os consumidores precisam mudar algo? Quem deve revisar este documento?
12. **Numeração.** Usei DD-2026-001 por não haver outro documento em `docs/design/`. Confirmar o número correto com o time de arquitetura.
