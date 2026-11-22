Rafael, o documento está salvo em `docs/design/deduplicacao-de-eventos.md`. Segui o `TEMPLATE.md` na ordem e com os mesmos títulos: cabeçalho, Motivação, Proposta, Riscos, Plano de rollout, Métricas de sucesso e Perguntas abertas.

**O que preenchi com o que você disse**
- **Motivação:** os 4% de duplicatas do mês passado, o efeito nos relatórios de faturamento e as duas reclamações do financeiro.
- **Proposta:** o serviço entre o ingestor e o Kafka, com a chave idempotente guardada no Redis por 24h e os repetidos descartados.
- **Métricas de sucesso:** duplicatas abaixo de 0,1%.

**Uma mudança em relação ao template:** ele não tem lugar para as alternativas nem para o trade-off. Para não perder essa parte, criei duas subseções dentro de Proposta, "Trade-offs aceitos" e "Alternativas consideradas". A segunda inclui "não fazer nada". O trade-off é o +5ms de latência no caminho crítico, que marquei como estimativa. Se o time de arquitetura preferir que isso entre de outro jeito, é fácil mover.

**Seções que ficaram sem conteúdo:** Riscos, Plano de rollout e a forma de medir a meta. Em cada uma deixei uma linha dizendo que aguarda sua resposta, com a pergunta correspondente. Não inventei risco nem fase de rollout. O número `DD-2026-<seq>` e os revisores também ficaram em aberto.

**Perguntas no final do documento**
1. Qual é o número do documento (`DD-2026-<seq>`) e quem são os revisores, com a área de cada um?
2. Qual é a chave idempotente de um evento e quem a gera, o produtor ou o ingestor?
3. Quais são os riscos e as mitigações? O que o serviço faz se o Redis ficar indisponível?
4. Como entra em produção: de uma vez ou em fases? Qual o critério para avançar e qual o rollback?
5. Como e onde a taxa de duplicatas será medida, e em que prazo?
6. Os +5ms vêm de medição ou de estimativa? Existe um limite de latência para a ingestão?
7. O que fica explicitamente fora do escopo?

Não rodei o `unslop` porque ele não está instalado aqui. Revisei o texto à mão, sem tiques de escrita. Não incluí diagrama, porque você não deu detalhes de componentes além de Redis e Kafka e o template só pede diagrama como complemento ao texto.
