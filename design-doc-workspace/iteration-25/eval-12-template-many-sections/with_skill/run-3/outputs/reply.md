Escrevi o doc em `docs/design/deduplicacao-de-eventos.md`, seguindo `docs/design/TEMPLATE.md` seção por seção, na ordem original (cabeçalho, 1 a 7).

O que está preenchido, só com o que você disse: problema (4% de duplicatas, faturamento inflado, financeiro reclamou duas vezes), proposta (serviço entre ingestor e Kafka, chave idempotente no Redis por 24h), meta (menos de 0,1%), trade-off (+5 ms no caminho crítico) e as alternativas, incluindo "não fazer nada". Datas: 2026-11-16. Estado: RASCUNHO.

Um desvio do template, que você precisa aceitar: o template não tem lugar para alternativas e trade-offs, então acrescentei a seção 5.6 "Alternativas consideradas e trade-offs" no fim do desenho técnico. Se a arquitetura não aceitar seção extra, essa tabela pode ir para 2.2.

Não inventei o que faltava. Estas seções ficaram marcadas como "Pendente", com a pergunta a responder, e o resumo está em 2.2:
- Cabeçalho: número DD-2026-<seq>, dono do requisito, QA, suporte, revisores, Jira e issues. Pus você como "Desenvolvedores (autor)"; ajuste se precisar.
- 1.3: demais atores e cenários. Não-objetivos: nenhum informado.
- 3.1 e 4: API nova? Mudança nos produtores, no ingestor ou nos consumidores?
- 5.2: convivência no deploy, migração e rollback.
- 5.3: volume, tamanho do Redis, como desligar. A estimativa de +5 ms está marcada como não medida.
- 5.4: segurança e dados sensíveis.
- 5.5: métricas, logs e alertas.
- 6: critérios de teste. 7: outros artefatos.
- Perguntas de substância: de onde vem a chave idempotente (produtor ou serviço) e o que o serviço faz se o Redis ficar indisponível.

Não incluí diagrama: não tenho as tecnologias nem os protocolos, e o template não exige um. Não rodei validação nem renderização.
