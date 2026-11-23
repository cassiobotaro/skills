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

O pipeline de ingestão recebe eventos duplicados dos produtores, causados por reenvio em retry. No mês passado medimos 4% de eventos duplicados. As duplicatas inflam os relatórios de faturamento, e o financeiro já reclamou duas vezes.

## Proposta

Criar um serviço de deduplicação que fica entre o ingestor e o Kafka. Para cada evento recebido, o serviço consulta a chave idempotente do evento no Redis. Se a chave já existe, o serviço descarta o evento como repetido. Se não existe, o serviço guarda a chave no Redis com validade de 24 horas e entrega o evento ao Kafka.

Com isso a deduplicação acontece uma única vez, antes do Kafka, e nenhum consumidor precisa tratar duplicatas por conta própria.

### Alternativas consideradas

Esta seção não existe no template. Foi adicionada para registrar as alternativas já discutidas e descartadas.

- **Deduplicar no consumidor.** Cada consumidor teria que reimplementar a deduplicação. Descartada por isso.
- **Idempotência nativa do produtor Kafka.** Não cobre o reenvio entre reinícios do produtor, que é um dos casos que geram as duplicatas. Descartada por isso.

### Trade-off aceito

O serviço adiciona um salto ao caminho crítico da ingestão. A estimativa é de +5ms de latência. O time aceitou esse custo em troca de eliminar as duplicatas antes do Kafka.

## Riscos

O único risco discutido até agora é o do trade-off acima: um salto a mais no caminho crítico da ingestão, com latência estimada em +5ms, aceito pelo time. Os demais riscos e suas mitigações estão em [Perguntas abertas](#perguntas-abertas).

## Plano de rollout

Ainda não definido. Ver [Perguntas abertas](#perguntas-abertas).

## Métricas de sucesso

- Reduzir as duplicatas de 4% (medido no mês passado) para menos de 0,1%.

## Perguntas abertas

Rafael não pôde responder durante a escrita. Estas perguntas ficaram em aberto e precisam de resposta antes de o documento sair de Rascunho.

**Proposta**
1. Como se forma a chave idempotente? Os produtores já enviam uma, ou o serviço a deriva do conteúdo do evento?
2. Quem são os produtores e o que garante que o reenvio em retry reutiliza a mesma chave?
3. Qual o comportamento do serviço quando o Redis está indisponível: deixa passar os eventos, rejeita ou segura?
4. O que acontece com um reenvio que chega depois das 24h? Por que 24h é a janela certa?
5. O serviço roda em quantas instâncias, e como a consulta e o registro da chave se comportam com requisições concorrentes do mesmo evento?
6. Qual a origem da estimativa de +5ms, e existe um limite de latência que o ingestor não pode ultrapassar?

**Riscos**
7. Quais outros riscos o time enxerga, e como cada um será mitigado?

**Plano de rollout**
8. Em quais fases o serviço entra em produção, com que critério para avançar de uma fase para a seguinte e com que critério e procedimento de rollback?

**Métricas de sucesso**
9. Como a taxa de duplicatas será medida depois do rollout, e onde (por exemplo, no Kafka ou nos relatórios de faturamento)?
10. Além da taxa de duplicatas, existe meta para a latência adicional?

**Revisão**
11. Quem são os revisores do time de arquitetura que devem constar no cabeçalho?
