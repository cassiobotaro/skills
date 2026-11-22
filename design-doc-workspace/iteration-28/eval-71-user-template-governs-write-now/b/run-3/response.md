Rafael, o documento está salvo em `docs/design/servico-de-deduplicacao-de-eventos.md`. Ele ainda não está completo: três seções do template estão sem conteúdo, esperando suas respostas.

**Como ficou:** segui o template na ordem, com cabeçalho, Motivação, Proposta, Riscos, Plano de rollout, Métricas de sucesso e Perguntas abertas.
- **Motivação:** os 4% de duplicatas, o reenvio em retry e as duas reclamações do financeiro.
- **Proposta:** o serviço entre o ingestor e o Kafka, com a chave no Redis por 24h.
- **Métricas de sucesso:** a meta de duplicatas abaixo de 0,1%, com os 4% como linha de base.

**Desvio do template, para você aceitar ou não:** o template não tem lugar para os trade-offs nem para as alternativas que você descreveu. Criei duas subseções dentro de Proposta, "Trade-offs da solução escolhida" e "Alternativas consideradas". Entram aí o +5ms de latência, as duas alternativas descartadas e "não fazer nada". As seções do template continuam intactas e na mesma ordem. Se o time de arquitetura não aceitar subseções extras, é só mover esse conteúdo.

**Seções que ficaram só com uma linha de "aguarda resposta":**
- **Riscos:** você não citou riscos, e não quis escrever nenhum por conta própria.
- **Plano de rollout:** você não falou de fases, de critério de avanço nem de rollback.
- Os campos **Revisores** e o número sequencial do **DD-2026-<seq>** também ficaram em aberto.

**Perguntas (estão também no fim do documento):**
1. Qual é o número sequencial do documento? Só existe o template na pasta.
2. Quem são os revisores e de quais áreas?
3. De onde vem a chave idempotente: os produtores já a enviam, ou o ingestor a gera?
4. O que o serviço faz se o Redis cair: deixa o evento passar ou rejeita?
5. Quais riscos você enxerga e como mitigá-los?
6. Como será o rollout: fases, critério de avanço e rollback?
7. Como vamos medir a taxa de duplicatas depois do lançamento, e há um limite aceitável de latência além dos +5ms?

Não incluí diagrama, porque a arquitetura não tinha tecnologias nem protocolos que você tivesse informado. A skill `unslop` não está instalada neste ambiente, então a revisão de estilo foi só a manual.
