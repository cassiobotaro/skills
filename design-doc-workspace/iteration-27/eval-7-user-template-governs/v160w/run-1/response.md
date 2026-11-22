Salvei o design doc em `docs/design/DD-2026-001-deduplicacao-de-eventos.md`. Não o commitei e não rodei nada, só escrevi o arquivo.

O doc segue as seções do template, na ordem: Motivação, Proposta, Riscos, Plano de rollout, Métricas de sucesso e Perguntas abertas. Com o que você me deu, preenchi assim:
- **Motivação:** os 4% de duplicatas, que eu datei como outubro de 2026, as duas reclamações do financeiro e a meta de ficar abaixo de 0,1%.
- **Proposta:** um diagrama Mermaid do fluxo, o texto explicando o diagrama e o trade-off dos +5ms.
- **Riscos:** a latência extra, o Redis e o serviço no caminho crítico, e os reenvios que chegam depois de 24h. Só a latência tem mitigação, e as outras duas apontam para as perguntas abertas.
- **Plano de rollout:** ficou só um apontamento para as perguntas abertas, porque você não me deu nada sobre fases ou rollback.

Três pontos para você conferir:
- **Seção extra:** acrescentei "Alternativas consideradas" entre Proposta e Riscos, com "não fazer nada", deduplicar no consumidor e a idempotência nativa do Kafka. O template não tem lugar para isso, e a seção está marcada no próprio doc como fora do template. Se a arquitetura for rígida demais com isso, mova o conteúdo para dentro de Proposta.
- **Numeração:** usei DD-2026-001 porque `docs/design/` só tinha o template. Ajuste se houver numeração em outro lugar.
- **Campo vazio:** Revisores ficou em branco.

As perguntas abertas, que estão no fim do doc, são estas:
1. Quem revisa o doc?
2. Como é o rollout: fases, critério de avanço e rollback?
3. De onde vem a chave idempotente: o produtor a envia ou o serviço a deriva do conteúdo?
4. Se o Redis cair, a ingestão continua aceitando duplicatas ou para?
5. Qual a ordem e a atomicidade entre registrar a chave e publicar no Kafka?
6. Como o serviço trata dois reenvios simultâneos do mesmo evento?
7. Reenvios depois de 24h acontecem na prática, e a janela basta?
8. Qual o limite aceitável de latência, e os +5ms foram medidos ou só estimados?
9. Como e onde medimos a taxa de duplicatas depois do rollout?
10. A meta de 0,1% vale para o Kafka ou para os relatórios de faturamento?
