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

O pipeline de ingestão recebe eventos duplicados dos produtores, que reenviam o mesmo evento quando fazem retry. No mês passado medimos 4% de duplicatas. Elas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes.

## Proposta

Vamos criar um serviço de deduplicação que fica entre o ingestor e o Kafka. Para cada evento recebido, o serviço consulta no Redis a chave idempotente do evento. Se a chave já existe, o serviço descarta o evento. Se não existe, o evento segue para o Kafka. O Redis guarda cada chave por 24 horas.

Como o serviço fica antes do Kafka, a deduplicação acontece uma única vez, e os consumidores recebem o fluxo já sem repetidos, sem implementar lógica própria.

Os detalhes do fluxo (origem da chave, ordem entre registrar a chave e publicar, comportamento quando o Redis está indisponível) estão em [Perguntas abertas](#perguntas-abertas).

## Alternativas consideradas

Esta seção não existe no template; entra aqui para registrar o raciocínio da decisão.

- **Não fazer nada.** Mantém os 4% de duplicatas e os relatórios de faturamento inflados. Não resolve a reclamação do financeiro.
- **Deduplicar no consumidor.** Descartada: cada consumidor teria que reimplementar a deduplicação.
- **Idempotência nativa do produtor Kafka.** Descartada: não cobre o reenvio entre reinícios do produtor.

## Riscos

- **Latência no caminho crítico.** O serviço adiciona um salto à ingestão, estimado em +5 ms de latência. O time aceitou esse custo em troca da redução de duplicatas.

Demais riscos e mitigações estão em [Perguntas abertas](#perguntas-abertas).

## Plano de rollout

As fases, os critérios de avanço e o critério de rollback estão em [Perguntas abertas](#perguntas-abertas).

## Métricas de sucesso

| Métrica | Hoje | Meta |
|---|---|---|
| Taxa de duplicatas nos eventos ingeridos | 4% (mês passado) | abaixo de 0,1% |
| Latência adicionada à ingestão | n/a | +5 ms (estimativa, ainda não medida) |

## Perguntas abertas

1. **Chave idempotente.** Quem gera a chave de cada evento (o produtor ou o ingestor) e de que campos ela é composta?
2. **Redis indisponível.** Quando o Redis falha ou degrada, o serviço deixa o evento passar (aceitando duplicatas) ou o rejeita (arriscando perda e backpressure nos produtores)?
3. **Ordem entre registro e publicação.** O serviço registra a chave antes ou depois de publicar no Kafka? Qual é o comportamento esperado se a publicação falhar depois do registro?
4. **Por que 24 horas.** O que fundamenta a janela de 24 h (por exemplo, o maior intervalo de retry conhecido dos produtores)? Duplicatas que chegam depois disso passam?
5. **Outros riscos.** Além da latência, que riscos o time enxerga (disponibilidade do novo serviço, capacidade do Redis, consistência da chave) e qual a mitigação de cada um?
6. **Rollout.** Em quais fases o serviço entra em produção, qual critério permite avançar de fase e qual dispara rollback?
7. **Latência.** O +5 ms é estimativa. Existe um limite de latência da ingestão que, se ultrapassado, invalida a proposta? Qual é a latência de hoje?
8. **Medição da meta.** Como e onde se mede a taxa de duplicatas (a mesma medição dos 4%)? Em que prazo após o rollout a meta de 0,1% deve ser atingida?
9. **Escopo.** O que fica fora deste trabalho (por exemplo, duplicatas já gravadas no histórico de faturamento)?
10. **Revisores e numeração.** Quem revisa este documento pela arquitetura? O número DD-2026-001 assume que este é o primeiro doc da pasta, já que `docs/design/` só tem o template. Confirma?
