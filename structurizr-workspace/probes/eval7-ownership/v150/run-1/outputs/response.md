Escrevi um rascunho de `workspace.dsl` na raiz do repositório com tudo o que ficou claro na sua descrição, validado com `structurizr/structurizr validate` (passou limpo). Falta uma decisão sua antes de eu fechar o modelo — explico abaixo.

## O que está no arquivo

**Modelo (C4)**

- `OrderFlow` — software system, escopo do workspace.
  - `criar-pedido`, `listar-pedidos`, `webhook-pagamento` — três containers (AWS Lambda - Python). Cada função serverless é um container no C4.
  - `orders` — container de dados (Amazon DynamoDB), cilindro. As três funções "leem e gravam pedidos em" ela, via DynamoDB API/HTTPS.
- `Stripe` — software system externo (cinza). Relação: `Stripe → webhook-pagamento` "Envia eventos de pagamento para" (JSON/HTTPS).
- **API Gateway não é container**: é um conceito de deployment (só roteia e autentica por API key, sem lógica sua), então aparece como `infrastructureNode` nas deployment views, não na view de containers.

**Ambientes**

- `Desenvolvimento` — Laptop do desenvolvedor → LocalStack → API Gateway (emulado), Lambda (as três funções) e DynamoDB (`orders`).
- `Produção` — Amazon Web Services → us-east-1 → API Gateway, AWS Lambda (as três funções) e Amazon DynamoDB; o Stripe aparece como nó externo, e a chamada dele ao webhook é reroteada pelo API Gateway (`-/>`), que é como o tráfego passa de verdade.

**Views**: `SystemContext`, `Containers`, `Deployment-Dev` e `Deployment-Prod`, todas com `autoLayout`. Tema `amazon-web-services-2025.07` (bundled na imagem) para os ícones de AWS Cloud, Region, API Gateway, Lambda e DynamoDB na view de produção.

## O que ficou de fora de propósito: o app mobile

Você disse que "o app mobile (Flutter) dos clientes chama a API", mas não quem constrói o app — e isso muda o modelo:

- **Se o seu time constrói e faz deploy do app Flutter** (mesmo repo ou não, mas é de vocês): ele é um **container do OrderFlow** (`Flutter`, shape de mobile), o `Cliente` é uma `person` que usa o app, e o app chama `criar-pedido` e `listar-pedidos`. Nas deployment views ele aparece num nó "Smartphone do cliente".
- **Se outro time (ou parceiro) é dono do app**: ele é um **software system externo** que chama o OrderFlow, e o `Cliente` usa esse sistema — o OrderFlow não abre a caixa.

Não quis chutar, porque os dois desenhos contam histórias diferentes sobre o que o time é responsável. Para eu fechar:

1. **Quem é dono do app Flutter — o time do OrderFlow ou outro time?**
2. **Alguma das lambdas chama o Stripe de saída** (por exemplo, `criar-pedido` cria um PaymentIntent), ou o Stripe só chama o webhook? Hoje modelei só o sentido Stripe → webhook, que foi o que você descreveu.
3. **Em dev, como o webhook do Stripe chega ao laptop** (Stripe CLI encaminhando, eventos disparados à mão, ou não chega)? Deixei o Stripe fora do ambiente de desenvolvimento por enquanto.

Assumi também que o app chama `criar-pedido` e `listar-pedidos` (e não o webhook); me corrija se não for isso. Com as respostas eu adiciono o app e o cliente, as relações que faltam e o reroteamento app → API Gateway → lambdas nos dois ambientes.

## Para visualizar

Preview com live reload em `http://localhost:8080` (rodando da raiz do repo):

```
docker run --rm -it -p 8080:8080 -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_AUTOREFRESHINTERVAL=2000 \
    -e STRUCTURIZR_AUTOSAVEINTERVAL=5000 \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr local
```

Para exportar (PlantUML, Mermaid, etc.) depois de ajustar o layout na UI:

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr export -workspace workspace.json -format plantuml -output diagrams
```
