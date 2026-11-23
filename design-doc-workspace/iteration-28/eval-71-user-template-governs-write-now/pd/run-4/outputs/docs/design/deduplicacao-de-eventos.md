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

A meta é levar a taxa de duplicatas para abaixo de 0,1%.

## Proposta

Vamos criar um serviço de deduplicação entre o ingestor e o Kafka. Para cada evento recebido do ingestor, o serviço consulta a chave idempotente do evento no Redis. Se a chave já existe, o serviço descarta o evento como repetido. Se não existe, o serviço guarda a chave no Redis por 24 horas e entrega o evento ao Kafka.

```
Produtores → Ingestor → Serviço de deduplicação → Kafka
                                 │
                                 └── Redis (chaves idempotentes, TTL de 24h)
```

O diagrama mostra o novo salto no caminho crítico: todo evento da ingestão passa pelo serviço antes de chegar ao Kafka. O Redis guarda somente as chaves idempotentes, e o TTL de 24h define a janela em que um reenvio ainda é reconhecido como duplicata. Os detalhes de como a chave é obtida e de como o serviço se comporta quando o Redis falha estão em [Perguntas abertas](#perguntas-abertas).

### Alternativas consideradas

Este bloco não existe no template. Ele foi adicionado aqui, entre Proposta e Riscos, porque o template não tem lugar para o raciocínio que levou à escolha.

- **Deduplicar no consumidor.** Descartada: cada consumidor teria que reimplementar a deduplicação.
- **Idempotência nativa do produtor Kafka.** Descartada: ela não cobre o reenvio entre reinícios do produtor.
- **Não fazer nada.** Mantém os 4% de duplicatas e o problema no faturamento. A discussão da equipe não registrou outro raciocínio sobre esta opção.

### Trade-off aceito

O serviço adiciona um salto no caminho crítico da ingestão. A estimativa é de +5ms de latência por evento. A equipe aceita esse custo.

## Riscos

- **Latência no caminho crítico.** O salto extra custa cerca de +5ms por evento (estimativa, ainda não medida). A equipe aceitou esse custo.

Os demais riscos (por exemplo, o comportamento diante de falhas do serviço ou do Redis) ainda não foram levantados. Eles estão em [Perguntas abertas](#perguntas-abertas).

## Plano de rollout

Ainda não definido. As fases, os critérios de avanço e o rollback estão em [Perguntas abertas](#perguntas-abertas).

## Métricas de sucesso

| Métrica | Hoje | Meta |
|---|---|---|
| Eventos duplicados que chegam ao Kafka | 4% (mês passado) | abaixo de 0,1% |

A latência adicional estimada é de +5ms. Um limite para ela é uma pergunta em aberto (ver [Perguntas abertas](#perguntas-abertas)).

## Perguntas abertas

Rafael não pôde responder durante a escrita. Estas perguntas ficam para a próxima revisão.

**Proposta**
1. De onde vem a chave idempotente? Os produtores a enviam no evento, ou o serviço a deriva do conteúdo?
2. O que o serviço faz quando o Redis está indisponível: deixa passar os eventos (aceitando duplicatas) ou bloqueia a ingestão?
3. A consulta e a gravação da chave acontecem em uma operação atômica? Como o serviço trata dois reenvios simultâneos do mesmo evento?
4. A chave é gravada antes ou depois de o Kafka confirmar o recebimento? O que acontece se a entrega ao Kafka falhar depois da gravação?
5. O serviço roda em quantas instâncias, e o Redis é um cluster existente ou novo?
6. A janela de 24h cobre a janela máxima de retry dos produtores? Quanto tempo depois do primeiro envio um reenvio pode chegar?

**Riscos**
7. Quais outros riscos a equipe enxerga, e qual a mitigação de cada um?
8. Há um limite aceitável para a latência total da ingestão? A estimativa de +5ms vem de medição ou de cálculo?

**Plano de rollout**
9. Como o serviço entra em produção (por exemplo, por produtor, por percentual do tráfego ou em modo sombra)? Qual o critério para avançar de fase e qual o critério e o procedimento de rollback?

**Métricas de sucesso**
10. Como e onde medimos a taxa de duplicatas depois do rollout? Foi a mesma medição usada para chegar aos 4%?
11. Em quanto tempo após o rollout a meta de 0,1% deve ser atingida?

**Revisão**
12. Quem são os revisores deste documento?
