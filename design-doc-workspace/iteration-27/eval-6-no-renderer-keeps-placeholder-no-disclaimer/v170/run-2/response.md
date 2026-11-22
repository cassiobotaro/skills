Escrevi o design doc em `docs/design/webhooks-de-saida.md`, em português, com o diagrama de arquitetura e o fluxo de entrega com retry. A imagem do diagrama de arquitetura ainda não existe.

**O que o documento cobre**
- Cabeçalho, glossário (HMAC, DLQ, backoff, evento de domínio, tentativa), visão geral, contexto e objetivos.
- A solução, com o diagrama de containers e o fluxo de entrega com retry. O fluxo está em Mermaid e já renderiza no Markdown.
- Os trade-offs com ✓/✗. O custo que você aceitou, a entrega não ser imediata em alguns casos porque passa pela fila, aparece como ✗, junto com o custo de construir e operar o serviço.
- As alternativas: serviço próprio (escolhida), SaaS de webhooks e não fazer nada.
- Questões em aberto.

**Pendências**
- **Imagem do diagrama:** sem Docker nem CLI do Structurizr, não renderizei o diagrama de arquitetura. O `![…](diagrams/architecture.svg)` é um placeholder, e o DSL está dobrado logo abaixo. Não validei o DSL. Basta renderizar e salvar em `docs/design/diagrams/architecture.svg`.
- **Tecnologias nos diagramas:** só Kafka e Postgres foram citados por você. Os outros containers e as setas ficaram sem tecnologia, inclusive a DLQ.

**Questões em aberto** (o texto não assume resposta para nenhuma):
- fora de escopo;
- critério de sucesso do POST (quais respostas contam como entrega);
- agenda do backoff (intervalo inicial, fator e teto) e o mecanismo da espera entre tentativas;
- tipo da DLQ, quem a consome e se há reenvio;
- duplicidade e ordenação dos eventos;
- guarda e rotação do segredo HMAC;
- cadastro de destinos;
- retenção do payload no Postgres e dados pessoais;
- migração dos serviços atuais;
- métricas, alertas e testes;
- autores e revisores (o cabeçalho está como "A confirmar", com uma sugestão de áreas).

Passei o `technical-writing` e o `unslop` na prosa. Não fiz commit.
