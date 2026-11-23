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

O pipeline de ingestão recebe eventos duplicados dos produtores, que reenviam o mesmo evento quando fazem retry. No mês passado medimos 4% de eventos duplicados. As duplicatas chegam aos relatórios de faturamento e inflam os valores: o financeiro já reclamou duas vezes.

Hoje nada no caminho entre o ingestor e o Kafka descarta esses repetidos, então cada consumidor recebe a duplicata e o problema aparece no fim da cadeia, no faturamento.

## Proposta

Vamos criar um serviço de deduplicação que fica entre o ingestor e o Kafka. Para cada evento recebido, o serviço consulta a chave idempotente do evento no Redis. Se a chave já existe, o serviço descarta o evento como repetido. Se não existe, o serviço guarda a chave no Redis com validade de 24 horas e entrega o evento ao Kafka.

```
produtor → ingestor → serviço de deduplicação → Kafka
                              │
                              └── Redis (chave idempotente, TTL 24h)
```

O diagrama mostra o novo salto no caminho da ingestão. O ingestor deixa de publicar direto no Kafka e passa a enviar ao serviço. O Redis é o único estado do serviço: guarda as chaves vistas nas últimas 24 horas.

### Alternativas consideradas

- **Deduplicar no consumidor.** Descartada: cada consumidor teria que reimplementar a deduplicação.
- **Idempotência nativa do produtor Kafka.** Descartada: não cobre o reenvio entre reinícios do produtor.
- **Não fazer nada.** Mantém os 4% de duplicatas e as distorções no faturamento. Não foi discutida em detalhe (ver Perguntas abertas).

### Trade-off aceito

O serviço adiciona um salto no caminho crítico da ingestão. A estimativa é de +5 ms de latência. O time aceita esse custo em troca de deduplicar em um único ponto, antes do Kafka.

## Riscos

- **Mais um salto no caminho crítico da ingestão (+5 ms estimados).** É o custo aceito descrito na Proposta. A estimativa ainda não foi medida.

Os demais riscos da proposta ainda não foram levantados. Ver Perguntas abertas.

## Plano de rollout

O plano ainda não foi definido: fases, critério de avanço e critério de rollback dependem das respostas em Perguntas abertas.

## Métricas de sucesso

- Duplicatas abaixo de 0,1% dos eventos (linha de base: 4% no mês passado).
- Latência adicional na ingestão próxima dos +5 ms estimados. Ainda não há um limite aceitável definido (ver Perguntas abertas).

## Perguntas abertas

**Motivação e escopo**
1. Qual é a chave idempotente do evento? Quem a gera (o produtor ou o ingestor) e ela já existe hoje em todos os produtores?
2. Por que 24 horas? Reenvios que cheguem depois dessa janela passam como eventos novos. Isso é aceitável?
3. Como foi medido o 4% do mês passado, e como mediremos o 0,1%?
4. O que está fora de escopo (por exemplo, correção dos relatórios de faturamento já inflados)?
5. Qual foi o motivo concreto para descartar "não fazer nada", além do impacto no faturamento?

**Proposta**
6. O que o serviço faz quando o Redis está indisponível: deixa passar eventos sem deduplicar ou rejeita a ingestão?
7. Como o Redis será operado (instância, replicação, persistência) e quem é o dono dele?
8. Como o serviço escala e como fica a ordem dos eventos para o Kafka?

**Riscos**
9. Além da latência, quais riscos o time enxerga e como cada um será mitigado?

**Plano de rollout**
10. Em quais fases o serviço entra em produção, com qual critério de avanço e qual critério de rollback?

**Métricas de sucesso**
11. Existe um limite máximo de latência para a ingestão? Qual valor de latência adicional dispara revisão da proposta?

**Documento**
12. Quem são os revisores? O número de sequência DD-2026-001 foi assumido por ser o primeiro doc em `docs/design/`; confirmar com o time de arquitetura.
