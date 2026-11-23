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

O pipeline de ingestão recebe eventos duplicados dos produtores. A causa é o reenvio em retry: o produtor reenvia um evento que a ingestão já recebeu. No mês passado medimos 4% de eventos duplicados.

As duplicatas chegam aos relatórios de faturamento e inflam os valores. O financeiro já reclamou duas vezes.

## Proposta

Criamos um serviço de deduplicação que fica entre o ingestor e o Kafka. O fluxo de cada evento:

```
produtor → ingestor → serviço de deduplicação → Kafka
                              │
                            Redis
```

O ingestor entrega o evento ao serviço de deduplicação em vez de publicá-lo direto no Kafka. O serviço consulta no Redis a chave idempotente do evento. Se a chave já existe, o serviço descarta o evento. Se não existe, o serviço grava a chave no Redis com validade de 24 horas e publica o evento no Kafka.

A deduplicação acontece uma vez, antes do Kafka. Nenhum consumidor precisa tratar duplicatas.

**Custo aceito.** O serviço é mais um salto no caminho crítico da ingestão. Estimamos +5 ms de latência por evento. O time aceita esse custo em troca de eliminar as duplicatas na origem.

**Limite da janela.** A chave vive 24 horas. Um reenvio que chegue depois disso não é reconhecido como duplicata.

## Alternativas consideradas

Esta seção não existe no template. Ela registra as alternativas discutidas, para que o motivo do descarte não se perca.

- **Deduplicar no consumidor.** Cada consumidor teria que reimplementar a deduplicação. Descartada.
- **Idempotência nativa do produtor Kafka.** Não cobre o reenvio entre reinícios do produtor, que é parte do problema. Descartada.
- **Não fazer nada.** Mantém 4% de duplicatas e o faturamento inflado. Não atende à reclamação do financeiro.

## Riscos

- **Latência no caminho crítico.** O novo salto adiciona cerca de 5 ms por evento (estimativa, ainda sem medição). É o trade-off aceito desta proposta. Mitigação: medir a latência real na fase inicial do rollout e comparar com a estimativa.
- **Dependência nova.** O Redis passa a participar da ingestão. O comportamento do serviço quando o Redis está indisponível ainda não está definido (ver Perguntas abertas).
- **Duplicatas fora da janela.** Reenvios após 24 horas não são descartados (ver Proposta).

## Plano de rollout

As fases, os critérios de avanço e o critério de rollback ainda não foram definidos (ver Perguntas abertas).

## Métricas de sucesso

- Taxa de eventos duplicados abaixo de 0,1% (hoje 4%, medida no mês passado).
- Latência adicional da ingestão, medida e comparada com a estimativa de +5 ms.

## Perguntas abertas

1. **Chave idempotente.** Quem gera a chave de cada evento, o produtor ou o ingestor? Ela já existe nos eventos de hoje?
2. **Falha do Redis.** Se o Redis estiver indisponível, o serviço deixa os eventos passarem (e aceita duplicatas) ou bloqueia a ingestão? Qual é a disponibilidade esperada do Redis e ele é dedicado ao serviço?
3. **Janela de 24 horas.** Algum dado mostra que os reenvios ocorrem dentro de 24 horas? Reenvios mais tardios são aceitáveis?
4. **Rollout.** Quais são as fases (por exemplo, por produtor ou por percentual de tráfego), o critério para avançar de uma fase e o critério de rollback?
5. **Meta e medição.** Em que prazo a meta de 0,1% deve ser atingida? Como mediremos a taxa de duplicatas depois do serviço no ar, com o mesmo método dos 4%?
6. **Latência.** Existe um limite de latência da ingestão que os +5 ms não podem ultrapassar? Como foi feita a estimativa?
7. **Escopo.** Há algo que fica explicitamente fora desta proposta?
8. **Revisores.** Quem do time de arquitetura e de outros times (financeiro, produtores) revisa este documento?
