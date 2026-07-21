Escrevi o design doc em `docs/design/servico-de-webhooks-de-saida.md`.

Como o repositório ainda não tinha design docs (nem template da casa), montei a estrutura
a partir do catálogo padrão, usando só o que você estabeleceu: cabeçalho, glossário, visão
geral, escopo e contexto, objetivos e fora de escopo, a solução (com arquitetura, fluxo de
entrega e uma nota sobre dados), trade-offs, alternativas, preocupações transversais e
questões em aberto.

**O que ficou registrado**

- O problema é o de hoje: POST na mão em cada serviço, sem retry e sem log central, com a
  falha chegando pelo suporte.
- A solução é o serviço único de entrega: consome os eventos de domínio do Kafka, persiste
  a tentativa no Postgres, faz o POST assinado com HMAC e reenvia com backoff exponencial
  por até 24h antes de mandar para a DLQ.
- O custo aceito está escrito com todas as letras na seção de trade-offs: a entrega deixa
  de ser imediata em alguns casos porque passa pela fila. Somei o custo operacional do
  serviço e do banco novos.
- As alternativas incluem o SaaS de webhooks (custo por evento e payload fora da nossa
  borda) e "não fazer nada", que é o cenário que motiva o documento.

**Diagramas**

- A arquitetura está como diagrama de contêineres em Structurizr DSL, com o DSL dobrado em
  um `<details>` e a imagem referenciada em `docs/design/diagrams/arquitetura.svg`. Essa
  máquina não tem a CLI do Structurizr nem Docker, então deixei a referência como
  *placeholder*, com um lembrete de renderizar na passada manual. Quando tiver o
  ambiente, para exportar e para validar o DSL:

  ```
  docker run --rm -u $(id -u):$(id -g) -v "$PWD":/usr/local/structurizr \
      -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
      structurizr/structurizr export -workspace workspace.dsl -format static -output diagrams

  docker run --rm -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
      -v "$PWD":/usr/local/structurizr structurizr/structurizr validate -workspace workspace.dsl
  ```

  E, se quiser validar direto pelo agente na próxima sessão, o servidor MCP:

  ```
  docker run --rm -p 3000:3000 -e PORT=3000 \
      -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
      structurizr/mcp -dsl -mermaid -plantuml
  ```

  Sem nenhuma dessas ferramentas aqui, o DSL **não foi validado** nesta máquina.

- O fluxo de entrega com retry é um bloco ```mermaid` dentro do documento, então renderiza
  direto no GitHub/GitLab. Também **não foi validado** aqui: não há servidor MCP conectado
  nem mermaid-cli instalado, e não instalei nada. O jeito privado de conferir é abrir o
  arquivo no GitHub/GitLab do próprio repositório; o mermaid.live também funciona, mas
  renderiza remotamente e o diagrama cita nomes internos — fica a seu critério.

**O que preciso de você**

1. Quem assina como autor, e quais times entram como revisores? Sugeri Segurança (HMAC,
   segredos, payload retido) e Plataforma/Infra (consumo do Kafka, banco novo) no
   cabeçalho, mas deixei "a definir".
2. O que é a DLQ concretamente — tópico do Kafka, tabela, outra coisa — e o que acontece
   com o que cai nela? Deixei o contêiner com tecnologia "a definir" no DSL.
3. Qual a tecnologia do serviço de entrega, e qual a curva do backoff (intervalo inicial,
   fator, teto) dentro das 24h?
4. Que resposta do cliente conta como sucesso, e erro permanente do endpoint tem
   tratamento diferente de indisponibilidade temporária?

Essas e outras quatro estão listadas em "Questões em aberto" no documento; me responda o
que já estiver decidido que eu incorporo ao texto.
