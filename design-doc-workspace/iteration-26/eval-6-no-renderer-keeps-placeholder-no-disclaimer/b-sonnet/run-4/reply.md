Escrevi o design doc em `docs/design/webhooks-de-saida.md`, com o que você descreveu: problema, proposta, alternativa descartada (SaaS), trade-off aceito, objetivos, o diagrama de arquitetura e o fluxo de entrega com retry.

Pontos de atenção:

- **Diagrama de arquitetura**: o DSL do Structurizr está dobrado em um bloco `<details>`. A imagem `diagrams/architecture.svg` é um placeholder, porque aqui não há Docker nem CLI do Structurizr. O DSL **não foi validado** e a imagem não foi gerada. Para validar e renderizar na sua máquina, a partir de um `workspace.dsl` com esse conteúdo:
  `docker run --rm -u $(id -u):$(id -g) -v "$PWD":/usr/local/structurizr structurizr/structurizr validate -workspace workspace.dsl`
  Para o SVG, use a imagem `structurizr/structurizr:<versão>-playwright` com `export -format svg`.
- **Fluxo de entrega**: o diagrama Mermaid está inline e também **não foi validado** aqui. Para validar: `docker run --rm -u "$(id -u):$(id -g)" -v "$DIR":/data minlag/mermaid-cli -i d.mmd -o d.svg`. O GitHub e o GitLab renderizam o bloco direto.
- Deixei sem tecnologia o que você não informou (DLQ, serviço de entrega, protocolo do POST), para não inventar.

Perguntas para fechar o documento (estão em Questões em aberto):

1. Quem são os autores e quais equipes devem revisar? O cabeçalho ficou sem esses campos.
2. O que conta como falha do endpoint do cliente (timeout, 5xx, 4xx)? Quais são os intervalos do backoff?
3. O que é a DLQ (tópico Kafka, tabela, outra coisa) e quem reprocessa o que cai nela?
4. Existe uma meta mensurável para "visibilidade de cada tentativa" (por exemplo, onde e como o suporte consulta)? O que fica fora de escopo desta primeira versão?
5. Onde ficam o endpoint e o segredo HMAC de cada cliente, e quem os gerencia?
