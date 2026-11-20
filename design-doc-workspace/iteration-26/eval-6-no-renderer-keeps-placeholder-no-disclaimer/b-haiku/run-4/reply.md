Escrevi o design doc em `docs/design/servico-webhooks-saida.md`, com o diagrama de contêineres e o fluxo de entrega com retentativa.

**O que está no documento**

- Problema, objetivos (nenhum evento perdido por indisponibilidade do cliente; cada tentativa visível), solução, trade-offs, alternativas (não fazer nada e SaaS de webhooks) e preocupações transversais (HMAC, payload, carga sobre o cliente).
- Diagrama de contêineres como DSL do Structurizr, dobrado num bloco `<details>`, com a imagem em `diagrams/arquitetura-containers.svg` como placeholder para a passagem manual.
- Fluxo de entrega com retentativa em Mermaid: consumo do Kafka, registro no Postgres, POST assinado, backoff exponencial dentro de 24 horas e desvio para a DLQ.

**Validação**

- O DSL do Structurizr **não foi validado** nesta sessão, e o diagrama não foi renderizado. Para validar e exportar, rode a partir da pasta `docs/design/`, quando tiver o Docker disponível:
  `docker run --rm -u $(id -u):$(id -g) -v "$PWD":/usr/local/structurizr -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes structurizr/structurizr validate -workspace <arquivo>.dsl`
  Para o PNG/SVG, use a variante `-playwright` com `export -format svg`.
- O diagrama Mermaid de sequência também **não foi validado** nesta sessão. Para validar, com o daemon Docker ativo: `docker run --rm -u "$(id -u):$(id -g)" -v "$DIR":/data minlag/mermaid-cli -i d.mmd -o d.svg`, onde `$DIR` é a pasta que contém `d.mmd`.
- Divergência do ambiente: eu tinha informado que esta máquina não teria Docker. Ao verificar, o daemon Docker responde (`docker info` retorna 0) e há imagens locais de `structurizr/structurizr` (incluindo `2026.10.26-playwright`) e de `minlag/mermaid-cli`. Como o ambiente declarado era sem Docker, não rodei a validação nem a renderização. Se quiser, eu faço as duas agora.

**Questões em aberto** (também registradas na seção homônima do documento)

1. Quem são os autores e quais áreas devem revisar?
2. O que fica fora de escopo, por exemplo a ordem de entrega dos eventos de um mesmo cliente?
3. O que conta como sucesso na resposta do cliente: um código de status específico ou qualquer confirmação?
4. Como as retentativas serão agendadas: tópicos de retentativa no Kafka, tabela no Postgres ou outro mecanismo?
5. Com que tecnologia o serviço de entrega será construído, e como a DLQ será implementada?
6. Como são criados, armazenados e rotacionados os segredos HMAC de cada cliente?
7. O cliente consegue tratar um mesmo evento recebido mais de uma vez? Há um identificador do evento no POST?
8. Os payloads contêm dados pessoais ou sensíveis?
9. Quem trata os eventos da DLQ, e como são reprocessados?
10. Quais métricas e alertas indicam que o serviço está saudável?
11. A implantação será de uma vez ou em etapas?

As três primeiras são as que mais afetam o design; as demais podem ficar para a revisão.
