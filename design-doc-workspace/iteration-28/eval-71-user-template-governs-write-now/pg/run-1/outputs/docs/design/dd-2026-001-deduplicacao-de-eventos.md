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

Hoje nenhum componente do caminho entre o ingestor e o Kafka descarta repetidos, então cada duplicata chega aos consumidores como se fosse um evento novo.

## Proposta

Criamos um serviço de deduplicação que fica entre o ingestor e o Kafka. Para cada evento recebido do ingestor, o serviço consulta a chave idempotente do evento no Redis:

- Se a chave não existe, o serviço grava a chave no Redis com validade de 24 horas e encaminha o evento ao Kafka.
- Se a chave existe, o serviço descarta o evento e não o encaminha.

Como a janela de deduplicação é de 24 horas, um reenvio só é detectado se chegar até 24 horas depois do primeiro envio. A origem da chave idempotente e o comportamento do serviço quando o Redis não responde estão em [Perguntas abertas](#perguntas-abertas).

### Alternativas consideradas

O template não tem uma seção para alternativas, então esta seção foi acrescentada logo após a Proposta. O restante do documento segue a ordem do template.

- **Deduplicar no consumidor.** Descartada. Cada consumidor teria que reimplementar a deduplicação.
- **Idempotência nativa do produtor Kafka.** Descartada. Ela não cobre o reenvio entre reinícios do produtor, que é parte do problema.

A alternativa de não fazer nada não foi discutida no registro que originou este documento. Ver [Perguntas abertas](#perguntas-abertas).

### Trade-off aceito

O serviço adiciona um salto ao caminho crítico da ingestão. Estimamos +5 ms de latência por evento. O time aceita esse custo em troca de uma única implementação de deduplicação, aplicada antes do Kafka, que beneficia todos os consumidores.

## Riscos

Risco aceito: +5 ms de latência no caminho crítico da ingestão, por causa do salto adicional (estimativa, ainda não medida).

Os demais riscos, e a mitigação de cada um, não foram levantados até agora. Eles estão como perguntas em [Perguntas abertas](#perguntas-abertas) e entram aqui quando o autor responder.

## Plano de rollout

O plano ainda não foi definido: fases, critério de avanço e critério de rollback estão em [Perguntas abertas](#perguntas-abertas).

## Métricas de sucesso

- Taxa de eventos duplicados abaixo de 0,1%. A linha de base é 4%, medida no mês passado.

A latência adicional estimada de +5 ms não é meta aprovada. Se o time quiser um limite, ele entra aqui (ver [Perguntas abertas](#perguntas-abertas)).

## Perguntas abertas

Rollout
1. Como o serviço entra em produção? Há fases (por produtor, por percentual do tráfego, modo sombra que só mede duplicatas sem descartar)?
2. Qual critério faz o rollout avançar de uma fase para a próxima, e qual critério dispara o rollback?

Riscos
3. O que acontece com a ingestão se o Redis ficar indisponível ou lento: o serviço descarta nada e encaminha tudo (aceitando duplicatas), bloqueia a ingestão, ou outro comportamento?
4. O que acontece com a ingestão se o próprio serviço de deduplicação cair? Ele é replicado?
5. Há risco de descartar um evento legítimo (por exemplo, colisão ou reutilização de chave idempotente por um produtor)? Como mitigamos?
6. Reenvios que chegam depois de 24 horas passam como eventos novos. Esse limite é aceitável para o faturamento?

Proposta
7. De onde vem a chave idempotente de cada evento? Os produtores já a enviam hoje, ou precisam passar a enviar?
8. A gravação da chave e o encaminhamento ao Kafka precisam ser atômicos? O que acontece se o serviço gravar a chave e falhar antes de entregar o evento ao Kafka?
9. Qual é o volume de eventos por segundo que o serviço deve suportar, e qual o dimensionamento esperado do Redis?
10. Por que 24 horas? O que sustenta essa janela (por exemplo, o maior intervalo de retry observado)?
11. Houve a opção de não fazer nada ou de tratar as duplicatas apenas na etapa de faturamento? Se sim, por que perdeu?

Métricas
12. A estimativa de +5 ms foi medida ou calculada? Existe um limite de latência da ingestão que não podemos ultrapassar?
13. Como e onde medimos a taxa de duplicatas depois do rollout (a mesma medição que gerou os 4%)?

Impacto em outras equipes
14. Quais equipes, além do time autor, são afetadas (produtores, consumidores, financeiro, plataforma/infra que opera o Redis) e quem revisa este documento?
15. O número de sequência DD-2026-001 foi assumido porque `docs/design/` não tem outros documentos. Confirmar com a arquitetura se existe outra numeração.
