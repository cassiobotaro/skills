Rafael, o doc está em `docs/design/deduplicacao-de-eventos.md`, seguindo o `docs/design/TEMPLATE.md` na ordem e com todas as seções.

**O que está preenchido** (só o que você disse):
- O problema: 4% de duplicatas no mês passado, faturamento inflado, duas reclamações do financeiro.
- A proposta: um serviço entre o ingestor e o Kafka, com a chave no Redis por 24h.
- As alternativas, com o motivo de cada descarte, mais "não fazer nada".
- O custo aceito: um salto a mais no caminho crítico, +5 ms estimados.
- A meta de duplicatas abaixo de 0,1%.
- O diagrama de contêineres em Structurizr DSL, sem tecnologia nas setas.

**Vocabulário do template:**
- "Autor" não é um campo do template. Coloquei você em "Desenvolvedores (autor do documento)". Ajuste se for diferente.
- As alternativas e os trade-offs não têm seção própria no template. Ficaram em 2.2, junto com as desvantagens conhecidas. Mantive a ordem e os títulos do template e não criei seção nova. Se o time de arquitetura preferir outro lugar, diga.

**O que ficou pendente.** O template exige estas seções e você não deu a substância, então elas dizem "A preencher" e remetem a perguntas numeradas em 2.2. Não inventei nada para preencher:
1. Cabeçalho: número DD-2026-seq, Jira, issues, dono do requisito, engenheiros de qualidade e de suporte, revisores técnicos.
2. Não-objetivos, e onde e como medir a meta de 0,1%.
3. Consumidores e produtores afetados (1.3).
4. API: origem da chave idempotente e o que acontece com o evento descartado (3.1).
5. Mudanças nos clientes (4).
6. Componentes: processo próprio ou parte do ingestor, e como se comunicam (5.1).
7. Compatibilidade, rollout e rollback (5.2).
8. Volume, pico, falha ou lentidão do Redis, como desligar (5.3).
9. Segurança: dados sensíveis na chave, acesso ao Redis (5.4).
10. Observabilidade (5.5).
11. Critérios de teste (6).
12. Outros artefatos (7).

Estado: RASCUNHO. A data usada é 2026-11-16.

**Diagrama:** a imagem `docs/design/diagrams/architecture.svg` não foi gerada (não rodei Docker). A referência é um placeholder e o DSL está dobrado em `<details>` logo abaixo. Renderize na passada manual.
