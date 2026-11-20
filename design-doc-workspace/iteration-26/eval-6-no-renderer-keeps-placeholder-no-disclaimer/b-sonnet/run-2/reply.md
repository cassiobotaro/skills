Escrevi o design doc em `docs/design/webhooks-de-saida.md` (estado: Rascunho, datas de hoje, 2026-11-20). Ele traz glossário, visão geral, contexto, objetivos, o design (arquitetura e fluxo de entrega com retry), trade-offs, alternativas (incluindo "não fazer nada" e o SaaS descartado) e questões em aberto. Usei só o que você descreveu.

Diagramas:
- **Arquitetura**: está em Structurizr DSL, dobrado em um bloco `<details>` abaixo de uma referência de imagem (`diagrams/architecture.svg`). Esse arquivo ainda não existe. Sem Docker nem CLI do Structurizr aqui, não consegui validar o DSL nem renderizar a imagem. Deixei o placeholder e uma nota para o passe manual. Para validar e exportar depois, rode `docker run --rm -u $(id -u):$(id -g) -v "$PWD":/usr/local/structurizr structurizr/structurizr validate -workspace workspace.dsl`, depois a exportação SVG com a variante `-playwright` da imagem.
- **Fluxo de entrega com retry**: está em Mermaid, direto no documento. Também não foi validado aqui, mas o GitHub e o GitLab renderizam o bloco. Para checar localmente: `docker run --rm -u "$(id -u):$(id -g)" -v "$DIR":/data minlag/mermaid-cli -i d.mmd -o d.svg`.
- Deixei sem tecnologia ou protocolo o que você não informou (a DLQ, o Kafka, o `POST`). Desenhei só o caminho de falha do endpoint do cliente. Outras falhas (do próprio serviço, do Postgres, do Kafka) estão anotadas como não descritas.

Perguntas, que estão como questões em aberto no documento:
1. Quem são os autores e quais equipes devem revisar (serviços que hoje fazem o `POST`, segurança, infraestrutura)? O cabeçalho está sem autores e revisores por isso.
2. Quais são os parâmetros do backoff (intervalo inicial, fator, teto) e o que conta como falha de entrega (códigos de resposta, timeout)?
3. A DLQ vive em que tecnologia, quem a consome e o que acontece com o evento depois que chega lá?
4. Onde ficam o segredo HMAC e a URL de cada cliente, e como o segredo é rotacionado? Quais cabeçalhos levam a assinatura?
5. Há algo fora de escopo nesta primeira versão, como a ordenação de eventos? Como será a implantação (migração de uma vez ou em etapas) e quais métricas e alertas acompanham a entrega?

Quando você responder, eu incorporo as respostas ao corpo do documento e tiro as perguntas respondidas da lista.
