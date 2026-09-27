Escrevi o `workspace.dsl` na raiz do projeto e validei com `structurizr/structurizr validate` via Docker: passou sem erros.

## O que está no modelo

- **OrderFlow** (software system) com quatro containers: as Lambdas `criar-pedido`, `listar-pedidos` e `webhook-pagamento` (tecnologia "AWS Lambda - Python") e a `Tabela orders` (Amazon DynamoDB, desenhada como cilindro). Cada Lambda "lê e grava pedidos em" na tabela, como você descreveu.
- **Stripe** como sistema externo (cinza), que "envia eventos de pagamento para" o `webhook-pagamento`.
- **API Gateway não é container**: ele só roteia e autentica por API key, então entra como `infrastructureNode` nas deployment views, não na view de containers (a view de containers mostra a arquitetura lógica; gateway é infraestrutura).
- Views: `SystemContext`, `Containers`, `Deployment-Dev` e `Deployment-Prod`.
  - **Desenvolvimento**: Laptop do desenvolvedor → LocalStack → API Gateway (emulado), Lambda (com as três funções) e DynamoDB (com a tabela).
  - **Produção**: Amazon Web Services → us-east-1 → API Gateway, AWS Lambda e Amazon DynamoDB, com ícones do tema oficial da AWS. O webhook do Stripe está roteado pelo API Gateway (`-/>`), em vez de chegar direto na Lambda.

## O que ficou de fora, de propósito: o app Flutter

Não coloquei o app mobile no modelo porque a classificação dele depende de uma coisa que você não disse, e eu não quis chutar. Há um comentário `// PENDENTE` no topo do `model` marcando o lugar.

1. **Quem constrói o app Flutter, o mesmo time do OrderFlow ou outro time/parceiro?** Isso decide o nível C4:
   - *Mesmo time* → o app é um **container do OrderFlow** (aparece dentro da caixa na view de containers):
     ```
     cliente = person "Cliente" "Faz e acompanha pedidos pelo app mobile."
     // dentro de orderflow { ... }:
     mobileApp = container "App mobile" "Permite ao cliente criar e consultar pedidos." "Flutter"

     cliente -> orderflow.mobileApp "Cria e consulta pedidos usando"
     orderflow.mobileApp -> orderflow.createOrder "Cria pedidos via" "JSON/HTTPS"
     orderflow.mobileApp -> orderflow.listOrders "Lista pedidos via" "JSON/HTTPS"
     ```
   - *Outro time* → o app é um **software system separado** que consome a API:
     ```
     cliente = person "Cliente" "Faz e acompanha pedidos pelo app mobile."
     mobileApp = softwareSystem "App mobile dos clientes" "App Flutter mantido por outro time; consome a API do OrderFlow." {
         tags "External"
     }

     cliente -> mobileApp "Cria e consulta pedidos usando"
     mobileApp -> orderflow.createOrder "Cria pedidos via" "JSON/HTTPS"
     mobileApp -> orderflow.listOrders "Lista pedidos via" "JSON/HTTPS"
     ```
2. **Em dev, o app roda apontando para o LocalStack do laptop?** Se sim, ele entra também na `Deployment-Dev`; se não, só na de produção.

Me responde essas duas e eu fecho o modelo: adiciono o bloco certo, coloco o smartphone do cliente como nó de deployment e roteio as chamadas do app pelo API Gateway nas duas deployment views, do mesmo jeito que já fiz com o Stripe.

Uma terceira dúvida, menor: a `criar-pedido` chama o Stripe (por exemplo, para iniciar o pagamento) ou a única interação com o Stripe é o webhook? Hoje só o webhook está no modelo, porque foi só isso que você descreveu.

## Como ver e exportar

Preview com live reload em `http://localhost:8080` (salva o layout manual em `workspace.json`):

```
docker run --rm -it -p 8080:8080 -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_AUTOREFRESHINTERVAL=2000 \
    -e STRUCTURIZR_AUTOSAVEINTERVAL=5000 \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr local
```

Exportar (por exemplo PlantUML ou Mermaid) para `diagrams/`:

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr export -workspace workspace.dsl -format plantuml -output diagrams
```
