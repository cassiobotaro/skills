Salvei o doc em `docs/design/DD-2026-001-deduplicacao-de-eventos.md`. Ele ainda está incompleto, porque faltam informações que só você pode dar.

Segui as seções do template na ordem. Usei DD-2026-001 como número, já que `docs/design/` só tinha o template. Estado: Rascunho, datas de hoje, autor Rafael Nunes.

**O que já está no doc**
- **Motivação:** os 4% de duplicatas e as duas reclamações do financeiro.
- **Proposta:** o fluxo do serviço entre o ingestor e o Kafka, com chave no Redis por 24h. Incluí um diagrama Mermaid simples e o texto que o explica.
- **Alternativas consideradas:** o template não tem essa seção, então criei uma depois da Proposta. Ela guarda as duas alternativas descartadas e o motivo de cada. Se a arquitetura preferir sem ela, é só remover.
- **Riscos:** só os +5ms de latência, registrados como trade-off aceito.
- **Métricas de sucesso:** duplicatas abaixo de 0,1%, com o baseline de 4%.

**O que ficou como pergunta, sem eu inventar resposta**
Esses pontos estão em Perguntas abertas, e Riscos, Rollout e Métricas apontam para lá:
1. **Redis fora do ar:** o serviço descarta, deixa passar ou rejeita os eventos? Há outros riscos além da latência?
2. **Chave idempotente:** quem a gera e de quais campos ela é composta?
3. **Ordem do registro:** a chave é gravada antes ou depois de o Kafka confirmar o evento?
4. **Rollout:** quais são as fases, o critério para avançar e o gatilho de rollback?
5. **Medição:** como medimos a taxa de duplicatas para comparar com os 0,1%?
6. **Revisores:** quem revisa o doc? O campo do cabeçalho está vazio.

Se você responder essas perguntas, eu preencho as seções. Como o time de arquitetura exige o formato, eu não mandaria o doc para eles com Riscos e Rollout vazios. Também não registrei a alternativa de não fazer nada. Se ela foi discutida, me conte e eu incluo.
