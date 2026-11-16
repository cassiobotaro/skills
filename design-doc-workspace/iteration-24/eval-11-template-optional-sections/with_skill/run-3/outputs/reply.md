Rafael, o doc está em `docs/design/servico-de-deduplicacao-de-eventos.md`, no formato do `docs/design/TEMPLATE.md`, com o DSL do diagrama em `docs/design/diagrams/architecture.dsl`.

**O que fiz**
- Mantive os títulos e a ordem do template. Preenchi Motivação, Proposta, Riscos, Métricas de sucesso e Perguntas abertas só com o que você contou (4% de duplicatas, financeiro reclamando duas vezes, Redis por 24h, +5ms, meta abaixo de 0,1%).
- Removi as seções que o próprio template manda apagar ou deixa como opcionais e que não tinham conteúdo seu: Histórias de usuário, Critérios de aceite, Estratégia de migração e Plano de rollout. Se alguma se aplica, me diga e eu preencho.
- **Desvio do template, para você aceitar ou não:** acrescentei "Alternativas consideradas" como subseção de Proposta. O template não tem lugar para as alternativas que vocês discutiram (consumidor, idempotência do Kafka) nem para "não fazer nada". Se a arquitetura não aceitar, é só apagar a subseção.
- Diagrama de containers em Structurizr DSL, embutido como imagem e o DSL dobrado em `<details>`. A imagem `diagrams/architecture.svg` não foi renderizada (sem Docker nesta execução). É um placeholder para a passagem manual. Só coloquei tecnologia nas caixas Redis e Kafka, que vieram de você.

**O que ficou em aberto (listado em Perguntas abertas)**
- O número do documento: `DD-2026-<seq>` ficou como placeholder, e o nome do arquivo é um slug por isso.
- Os revisores.
- Riscos além da latência: o que acontece se o Redis cair, e o que acontece com repetido que chega depois de 24h. Não escrevi nada disso como fato.
- A definição da chave idempotente, a concorrência entre instâncias e como medir a taxa de duplicatas.
- Se existe plano de rollout ou história de backlog associada.
