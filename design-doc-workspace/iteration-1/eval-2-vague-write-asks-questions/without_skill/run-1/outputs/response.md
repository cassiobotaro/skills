Criei um rascunho de design doc em `DESIGN-DOC-migracao-microservicos.md`, na raiz do repositório.

Mas preciso ser honesto: o repositório está **vazio** (não há código do monolito para eu inspecionar) e a mensagem não trouxe contexto sobre o sistema, o time ou o objetivo da migração. Sem isso, eu teria que **inventar** stack, banco, nomes de serviços, prazos e métricas — e chutes num design doc levam a decisões erradas. Então fiz o seguinte:

- Entreguei um **design doc completo na estrutura**, com a estratégia de referência (Strangler Fig), critérios para definir fronteiras de serviço por domínio (DDD), a parte mais difícil (migração de dados: database-per-service, saga, outbox, CDC), comunicação entre serviços, infra/observabilidade, plano de rollout/rollback e tabela de riscos.
- Marquei com `_(preencher)_` tudo que depende da realidade do projeto, em vez de inventar.
- Coloquei logo no início uma **Seção 0 com as perguntas** que transformam o rascunho num doc de verdade.

Para eu fechar o documento, me responde principalmente:

1. **Por que migrar agora?** Qual a dor concreta (deploys lentos, acoplamento, escala, custo, organização dos times)? E como vocês vão medir sucesso?
2. **Qual a stack do monolito** (linguagem/framework) e o **banco** (um banco compartilhado? quantas tabelas/volume)?
3. **Quais são os principais domínios/módulos** de negócio dentro do monolito, e quais **mais mudam** ou **mais escalam**?
4. Como é o **deploy hoje** (VM, container, Kubernetes, PaaS) e qual o **tráfego/carga**?
5. **Tamanho e experiência do time** com sistemas distribuídos, e se há prazo/orçamento definidos.

Um ponto que vale destacar antes de irmos adiante: microsserviços **não são automaticamente melhores** — eles trocam código acoplado por complexidade operacional distribuída. Se a dor principal for "código bagunçado", um **monolito modular** pode resolver com uma fração do custo. Vale a pena alinharmos o "porquê" (pergunta 1) antes de comprometer o time com a migração. Deixei essa reflexão registrada no doc também.

Se você me der acesso ao repositório do monolito (ou ao menos descrever a estrutura), eu consigo preencher as fronteiras de serviço e a ordem de extração com base no código real, em vez de placeholders.
