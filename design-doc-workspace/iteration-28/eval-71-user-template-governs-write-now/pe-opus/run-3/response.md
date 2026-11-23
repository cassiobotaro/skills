Escrevi o doc e salvei em `docs/design/DD-2026-001-deduplicacao-de-eventos.md`. Ele segue as seções do `TEMPLATE.md` na mesma ordem: cabeçalho, Motivação, Proposta, Riscos, Plano de rollout, Métricas de sucesso e Perguntas abertas.

**Um desvio do template para você aprovar:** o template não tem onde colocar as alternativas descartadas nem o trade-off aceito. Coloquei os dois como subseções dentro de **Proposta** ("Trade-offs" e "Alternativas consideradas"), sem mudar a estrutura de seções principais. Nas alternativas incluí também "não fazer nada", com o motivo que você deu: 4% de duplicatas inflando o faturamento e as duas reclamações do financeiro. Se a arquitetura recusar subseções fora do template, dá para mover ou tirar.

**O que ficou em aberto de propósito:**
- **Riscos** e **Plano de rollout** estão quase vazios. Você não citou riscos (fora o custo aceito de +5ms) nem fases de rollout, e eu não quis inventar. As duas seções apontam para as perguntas.
- **Diagrama de sequência:** o fluxo vai do produtor ao ingestor, depois ao serviço de deduplicação, ao Redis e ao Kafka. Ele não indica protocolos. Também não decide a ordem entre gravar a chave e publicar no Kafka; isso virou a pergunta 4.
- **Revisores** ficaram em branco.
- **ID do documento:** usei DD-2026-001 porque é o primeiro doc do repositório.

As 12 perguntas no final estão agrupadas por seção. As mais importantes para fechar o design são:
- de onde vem a chave idempotente;
- o que o serviço faz quando não consegue consultar o Redis;
- se a janela de 24h basta;
- como a taxa de 4% foi medida.

Não fiz commit.
