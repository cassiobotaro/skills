Escrevi o design doc em `docs/design/servico-webhooks-saida.md`, com o diagrama de arquitetura e o fluxo de entrega com retry. O texto usa só o que você descreveu: problema, proposta, a alternativa do SaaS, "não fazer nada", o trade-off da entrega não imediata e os dois objetivos.

Sobre os diagramas:
- **Arquitetura (C4, Structurizr DSL):** a imagem é uma referência para `docs/design/diagrams/architecture.svg`, que ainda não existe. Esta máquina não tem Docker nem a CLI do Structurizr, então não renderizei nem validei o DSL. O DSL está dobrado em um bloco `<details>` logo abaixo da referência. Para validar, rode no diretório do `workspace.dsl`: `docker run --rm -u $(id -u):$(id -g) -v "$PWD":/usr/local/structurizr structurizr/structurizr validate -workspace workspace.dsl`. Para gerar o SVG, use a imagem `structurizr/structurizr:<versão>-playwright` com `export -format svg`.
- **Fluxo de entrega (Mermaid):** também não foi validado, pelo mesmo motivo. O GitHub e o GitLab renderizam o bloco direto.
- Deixei em branco as tecnologias que você não citou: a do serviço de entrega, a da DLQ e o protocolo das setas.

Perguntas para fechar o documento (estão também em "Perguntas em aberto"):
1. Existe um número para os objetivos (taxa de eventos entregues, tempo até a primeira tentativa)? O que fica fora de escopo nesta primeira versão?
2. O que conta como entrega bem-sucedida? Quais respostas do cliente disparam novo retry?
3. Qual é o intervalo inicial e o teto do backoff? O serviço grava o resultado de cada tentativa antes ou depois do POST?
4. A DLQ é um tópico do Kafka ou outra coisa? Quem trata o que cai nela?
5. Como cada cliente cadastra o endpoint e o segredo do HMAC, e em qual header a assinatura viaja?
6. Como fica a migração dos serviços que hoje fazem o POST direto?
7. Quem são os autores e quais áreas devem revisar? O cabeçalho está com "A definir".
