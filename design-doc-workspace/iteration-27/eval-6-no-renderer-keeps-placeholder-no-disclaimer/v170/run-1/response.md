Escrevi o design doc em `docs/design/webhooks-de-saida.md`. Faltam duas coisas antes de ele estar pronto para revisão: renderizar a imagem do diagrama de arquitetura e responder às perguntas em aberto.

**O que o documento cobre**
- Cabeçalho (estado "Rascunho") e glossário.
- Visão geral, contexto, objetivos e fora de escopo.
- Design: arquitetura e fluxo de entrega com retry.
- Trade-offs com ✓/✗, incluindo a entrega não imediata em alguns casos.
- Alternativas: não fazer nada, SaaS de webhooks (descartado por custo por evento e por o payload sair da borda) e o serviço próprio.
- Perguntas em aberto.

**Diagramas**
- **Arquitetura:** o diagrama está em Structurizr DSL, dentro de um bloco `<details>`. A imagem `diagrams/architecture.svg` é só um placeholder, porque não há Docker nem CLI do Structurizr aqui. Dá para renderizar na revisão manual. Não validei o DSL.
- **Fluxo de entrega com retry:** está em Mermaid e renderiza direto no Markdown.
- **Tecnologias:** só entraram Kafka e PostgreSQL, que você citou. Deixei sem tecnologia o serviço de entrega e a DLQ, e sem protocolo as setas.

**Perguntas em aberto**

Não inventei nada além do que você disse. Estas ficaram registradas como perguntas:
- Autores e revisores. Sugiro Segurança (assinatura HMAC e guarda dos segredos) e os times dos serviços que hoje fazem o POST.
- Metas numéricas para os dois objetivos.
- O que conta como entrega bem-sucedida, e se há timeout por tentativa.
- Parâmetros do backoff e como o serviço agenda os reenvios ao longo de 24h.
- O que é a DLQ, quem a consome e como se reprocessa um evento que caiu nela.
- Onde ficam o endpoint do cliente e o segredo do HMAC, e como o serviço sabe a qual endpoint enviar cada evento.
- Tecnologia do serviço de entrega.
- Migração dos serviços atuais.
- Se o mesmo evento pode chegar duplicado ao cliente por causa do retry.

Passei as skills `technical-writing` e `unslop` na prosa. Não fiz commit.
