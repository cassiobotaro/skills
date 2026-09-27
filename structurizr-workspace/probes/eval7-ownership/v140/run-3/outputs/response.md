Escrevi o `workspace.dsl` na raiz do repositório e validei com `structurizr/structurizr validate` (Docker): passou sem erros.

## O que foi modelado

**Modelo**

- Pessoa: **Cliente**, que usa o app mobile.
- Sistema **OrderFlow** (escopo do workspace), com quatro containers:
  - `criar-pedido`, `listar-pedidos`, `webhook-pagamento` — "Python, AWS Lambda"
  - `orders` — "Amazon DynamoDB" (tag `Database`, cilindro)
  - As três funções leem e gravam em `orders` (`Lê e grava pedidos em`, via AWS SDK).
- Sistema **App Mobile** (Flutter, dos clientes) → chama `criar-pedido` e `listar-pedidos` por HTTPS.
- Sistema externo **Stripe** → chama `webhook-pagamento` por HTTPS.
- O **Amazon API Gateway não aparece como container**: como ele só roteia e autentica por API key (nada custom), no C4 ele é um conceito de deploy — entra como `infrastructureNode` nas deployment views, e as chamadas do app e do Stripe são reroteadas por ele com `-/>`. Na view de containers as setas vão direto do app/Stripe para as lambdas.

**Views** (todas com `autoLayout`, chaves estáveis)

- `SystemContext` — incluída por padrão junto com a de containers.
- `Containers` — a view que você pediu.
- `Deployment-Dev` — *Laptop do desenvolvedor → LocalStack*, com API Gateway, Lambda e DynamoDB emulados e as três funções + a tabela como instâncias.
- `Deployment-Prod` — *Amazon Web Services → us-east-1*, com Amazon API Gateway, AWS Lambda (3 funções) e Amazon DynamoDB; o smartphone do cliente (App Mobile) e o Stripe aparecem como origem das chamadas que passam pelo gateway. Ícones da AWS via o tema `amazon-web-services-2025.07`, que vem embutido na imagem Docker.

## Um ponto de classificação que só você decide

Modelei o **App Mobile como um sistema à parte** porque você descreveu o OrderFlow como "a API". Se o **mesmo time** é dono do app Flutter, o C4 manda colocá-lo *dentro* do OrderFlow como container. Para trocar, basta:

1. Apagar o bloco `appMobile = softwareSystem "App Mobile" …` e criar dentro do `orderflow`:
   `appMobile = container "App Mobile" "Aplicativo dos clientes…" "Flutter" { tags "Mobile App" }`
2. Trocar `appMobile` por `orderflow.appMobile` nas relações e no `softwareSystemInstance appMobile` de produção (que vira `containerInstance orderflow.appMobile`).

O `-/>` de produção continua funcionando do mesmo jeito.

## O que ficou de fora de propósito (me diga se quiser incluir)

- **Em dev**, não coloquei nem o app mobile nem o Stripe: você não disse como o app é apontado para o LocalStack nem como o webhook é exercitado localmente (Stripe CLI? chamada manual?). Sem essa informação a view de dev mostra só a stack que roda no laptop.
- **Nenhuma chamada de `criar-pedido` para o Stripe** (por exemplo, criar um PaymentIntent). Você só descreveu o caminho Stripe → webhook; se a API também chama o Stripe, me diga e eu adiciono a relação.
- Sem `!adrs`: o repositório não tem log de decisões.

## Para ver e exportar

Preview com live-reload em http://localhost:8080 (o layout manual fica salvo em `workspace.json`):

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

(Depois de arrumar o layout na UI, troque `-workspace workspace.dsl` por `-workspace workspace.json` para exportar com o layout salvo.)
