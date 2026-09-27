Escrevi o `workspace.dsl` na raiz do repositório e validei com a imagem `structurizr/structurizr` (Docker): o arquivo passa sem erros.

**O que está no modelo**

- **Pessoa:** Cliente, que usa o app mobile.
- **OrderFlow** (sistema em foco) com quatro containers: `criar-pedido`, `listar-pedidos` e `webhook-pagamento` (Python, AWS Lambda) e a `Tabela orders` (Amazon DynamoDB). As três funções leem e gravam na tabela, como você descreveu.
- **Stripe** como sistema externo, chamando `webhook-pagamento`.
- **App Mobile** (Flutter) como sistema externo, chamando `criar-pedido` e `listar-pedidos` — veja a pergunta abaixo.
- **API Gateway** não aparece na view de containers: como ele só roteia e autentica por API key, sem lógica própria, é um conceito de deployment. Ele entra nas duas deployment views como `infrastructureNode`, e em produção as chamadas do app e do Stripe são redirecionadas por ele (`-/>`), chegando às Lambdas via gateway.
- **Ambientes:** `Desenvolvimento` (laptop do dev → LocalStack emulando API Gateway, Lambda e DynamoDB) e `Produção` (AWS → us-east-1 → API Gateway, AWS Lambda, Amazon DynamoDB, com o tema oficial da AWS para os ícones).
- **Views:** `SystemContext`, `Containers`, `Deployment-Development` e `Deployment-Production`.

**Uma decisão que preciso que você confirme**

Modelei o app Flutter como um sistema *separado* do OrderFlow, porque você descreveu o OrderFlow como "a API". Se o **mesmo time** mantém o app e a API, o correto em C4 é o app ser um **container dentro do OrderFlow** (ele passa a aparecer na view de containers como parte do sistema, e não como caixa cinza externa). Me diz qual é o caso e eu ajusto — é uma mudança pequena, e o comentário no DSL marca o ponto.

**O que ficou de fora de propósito (não inventei)**

- Em dev, o app mobile e o Stripe não aparecem: você não disse como as chamadas chegam ao LocalStack no laptop (emulador? `curl`? túnel para o webhook do Stripe?). Se quiser isso no diagrama, me conta como funciona.
- Nenhuma chamada *do OrderFlow para o Stripe* (criar cobrança, por exemplo): você só mencionou o webhook de entrada. Se existir, qual função chama e com que propósito?

**Para ver e exportar**

Preview com live-reload em `http://localhost:8080` (o layout manual fica salvo em `workspace.json`; não edite esse arquivo à mão):

```
docker run --rm -it -p 8080:8080 -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_AUTOREFRESHINTERVAL=2000 \
    -e STRUCTURIZR_AUTOSAVEINTERVAL=5000 \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr local
```

Exportar (por exemplo PlantUML) para `diagrams/`:

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr export -workspace workspace.dsl -format plantuml -output diagrams
```
