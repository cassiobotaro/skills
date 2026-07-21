Escrevi o design doc em `docs/design/entrega-de-webhooks-de-saida.md`.

O que o documento cobre, a partir do que você me passou: o contexto (POST na mão em cada serviço, sem retry e sem log central), os objetivos (nenhum evento perdido por indisponibilidade do cliente e visibilidade de cada tentativa), a solução (consumo dos eventos de domínio do Kafka, tentativa persistida no Postgres, POST assinado com HMAC, backoff exponencial por até 24h e DLQ depois disso), o trade-off aceito (a entrega deixa de ser imediata em alguns casos) e as alternativas — o SaaS de webhooks que você descartou, com os dois motivos que você deu, e o "não fazer nada", que é o cenário de hoje.

Os dois diagramas que você pediu:

- **Arquitetura** — diagrama de contêineres em Structurizr DSL, com o DSL dobrado num `<details>` logo abaixo da imagem. Como não há Docker, CLI do Structurizr nem MCP nesta máquina, **a imagem ficou como referência de placeholder** apontando para `docs/design/diagrams/arquitetura-webhooks-saida.svg`: é só renderizar o DSL nesse caminho na próxima passagem, com a máquina que tiver a ferramenta. Um caminho:

  ```
  docker run --rm -u $(id -u):$(id -g) \
      -v "$PWD/docs/design":/usr/local/structurizr \
      -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
      structurizr/structurizr export -workspace workspace.dsl -format static -output diagrams
  ```

  (salvando antes o DSL do `<details>` como `docs/design/workspace.dsl`). Se preferir validar o DSL por MCP nas próximas sessões: `docker run --rm -p 3000:3000 -e PORT=3000 -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes structurizr/mcp -dsl -mermaid -plantuml`.

- **Fluxo de entrega com retentativa** — bloco ` ```mermaid `, que o GitHub/GitLab renderizam nativamente. Ele **não foi validado aqui** (sem MCP de Mermaid e sem mermaid-cli nesta máquina); dá para conferir colando em <https://mermaid.live>.

Duas coisas que deliberadamente não inventei: a tecnologia do serviço de entrega ficou como "A definir" no DSL, e o formato do cabeçalho da assinatura HMAC está marcado como a definir na nota do diagrama.

Para o documento sair do rascunho, faltam respostas suas — deixei todas na seção *Questões em aberto*, mas estas cinco são as que mais mudam o texto:

1. Quem assina o documento como autor, e quais times/áreas devem revisar? (sugeri Segurança, Infraestrutura/Plataforma e os donos dos serviços que hoje fazem o POST — confirme os nomes)
2. Qual a curva concreta do backoff dentro das 24h (intervalo inicial, fator, máximo de tentativas)? Com números, o objetivo "nenhum evento perdido" fica verificável.
3. Como o serviço descobre o endpoint e a chave HMAC de cada cliente — já existe um cadastro de assinantes, ou isso faz parte deste trabalho? E como as chaves são guardadas e rotacionadas?
4. Quais respostas do cliente contam como falha retentável? Um `4xx` de payload inválido dificilmente melhora no reenvio, e isso muda o desenho do ciclo.
5. A migração dos serviços de domínio acontece de uma vez ou serviço a serviço? Se for faseada, vale eu acrescentar uma seção de plano de implantação — hoje não há uma, porque não temos essa informação.

Se quiser, me responda o que já estiver decidido e eu incorporo direto no documento.
