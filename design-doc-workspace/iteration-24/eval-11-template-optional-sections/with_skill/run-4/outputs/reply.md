Escrevi o doc em `docs/design/DD-2026-001-servico-deduplicacao-eventos.md`, seguindo o `docs/design/TEMPLATE.md` na ordem do template, com o que você me passou. Não inventei nada além disso.

**O que ficou de fora do template, e por quê**
- Histórias de usuário e Plano de rollout (opcionais): você não deu a substância, então omiti. O rollout virou pergunta aberta.
- Critérios de aceite: o template manda apagar se o doc não estiver ligado a uma história do backlog. Você não disse que está, então apaguei.
- Estratégia de migração: o template manda apagar se não houver dados a migrar. Você não falou de dados existentes, então apaguei. Me confirme, porque isso é uma suposição minha.

**Desvio do template, para você aceitar ou não**
Acrescentei a seção "Alternativas consideradas" (incluindo "não fazer nada", escrita só a partir da dor que você descreveu). O template não tem lugar para isso, e o time de arquitetura vai querer ver por que as outras opções perderam. Se eles não aceitarem a seção extra, dá para mover o conteúdo para dentro de Proposta.

**Pontos que precisam da sua resposta** (estão em Perguntas abertas)
- Revisores (campo do cabeçalho em branco).
- Número sequencial: usei `DD-2026-001` porque só há o template em `docs/design/`. Corrija se já existirem outros docs fora do repositório.
- Qual é a chave idempotente e quem a gera.
- Comportamento quando o Redis ou o serviço cai.
- Se há retries depois de 24h (a janela de 24h deixa passar esses).
- Rollout, história de backlog e migração, conforme acima.

**Diagrama**
O diagrama de containers está como Structurizr DSL dobrado em `<details>`. A imagem `diagrams/deduplicacao-containers.svg` é um placeholder que não foi renderizado. Renderize na passada manual, porque não rodei Docker. Só pus tecnologia onde você a citou (Redis, Kafka).

Os números do doc (4%, meta de 0,1%, +5 ms) são os seus. O +5 ms está marcado como estimativa.
