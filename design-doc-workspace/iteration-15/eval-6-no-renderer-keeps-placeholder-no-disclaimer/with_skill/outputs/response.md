Escrevi o documento em `docs/design/servico-de-webhooks-de-saida.md`.

Ele cobre o que você passou: o problema de hoje (POST na mão, sem reenvio, sem log central, descoberta pelo suporte), a solução com consumo do Kafka, persistência da tentativa no Postgres, POST assinado com HMAC, backoff exponencial por até 24h e DLQ, o custo aceito da entrega deixar de ser imediata, e as alternativas — o SaaS de webhooks e o "não fazer nada", que é o cenário atual.

**Os dois diagramas**

- **Arquitetura**: modelei como C4 de contêineres em Structurizr DSL, embutido dobrado num `<details>` logo abaixo da referência da imagem. Como aqui não tem Docker nem a CLI do Structurizr, a imagem `diagrams/arquitetura-webhooks.svg` ficou como marcador do lugar dela, com uma linha avisando que ela sai na passagem manual. Quando você estiver numa máquina com Docker, o export gera o arquivo a partir do DSL:

  ```
  docker run --rm -u $(id -u):$(id -g) -v "$PWD":/usr/local/structurizr \
      -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
      structurizr/structurizr export -workspace workspace.dsl -format plantuml -output diagrams
  ```

- **Fluxo de entrega com reenvio**: sequência em Mermaid, em bloco ```mermaid — o GitHub, o GitLab e a maioria dos wikis renderizam direto no Markdown. Sem MCP e sem mermaid-cli nesta máquina, não consegui pré-visualizar o bloco aqui; se quiser conferir antes, cole em https://mermaid.live.

**Dois pontos onde deixei a lacuna aberta em vez de preencher**: o serviço de entrega ficou sem linguagem/runtime e a DLQ ficou sem tecnologia, porque você não chegou a definir isso — as caixas estão lá, só sem a etiqueta. O mesmo vale para o cabeçalho que carrega a assinatura HMAC.

**O que preciso de você para fechar o rascunho:**

1. Quem assina como autor e quais áreas revisam? Sugeri Segurança, Infraestrutura e os times donos dos serviços que hoje entregam os webhooks — confirma ou troca.
2. Dá para colocar número nos objetivos? "Nenhum evento perdido" e "visibilidade de cada tentativa" ficam bem mais verificáveis com uma meta associada.
3. O que fica explicitamente **fora** desta entrega? Deixei a seção sinalizando que ainda não está delimitada em vez de inventar exclusão.
4. Quem consome a DLQ e como é o reprocessamento depois que o evento cai lá?
5. Como as chaves de HMAC por cliente são geradas, distribuídas e rotacionadas, e o payload guardado no Postgres tem dado sensível (isso muda a conversa de retenção)?

O resto do que ficou em aberto está listado no fim do documento, na seção "Questões em aberto".
