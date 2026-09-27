Criei o `workspace.dsl` na raiz do repositório e validei com a imagem `structurizr/structurizr` (Docker) — sem erros.

## O que está no modelo

**Pessoas e sistemas**

- `Cliente` (pessoa) → usa o **App Mobile**.
- **App Mobile** (Flutter) — sistema à parte, que chama a API do OrderFlow (ver "ponto em aberto" abaixo).
- **OrderFlow** — a API serverless de pedidos, com quatro containers:
  - `criar-pedido`, `listar-pedidos`, `webhook-pagamento` — cada Lambda é um container (`AWS Lambda, Python`);
  - `orders` — a tabela DynamoDB, container de dados (cilindro).
- **Stripe** — sistema externo (cinza) que envia os eventos de pagamento para `webhook-pagamento`.

**Relacionamentos:** as três Lambdas leem e gravam em `orders` (`AWS SDK/HTTPS`); o App Mobile chama `criar-pedido` e `listar-pedidos`; o Stripe chama `webhook-pagamento` (`JSON/HTTPS (webhook)`).

**Amazon API Gateway não é container.** Como ele só roteia e autentica por API key, sem lógica própria, ele é um conceito de deployment: aparece como `infrastructureNode` nas duas deployment views (não na view de containers), e em produção as chamadas do app e do Stripe são reencaminhadas por ele com `-/>` (app → API Gateway → Lambda).

**Views** (todas com `autoLayout`, chaves estáveis):

| Chave | Conteúdo |
|---|---|
| `SystemContext` | Cliente, App Mobile, OrderFlow, Stripe |
| `Containers` | as três Lambdas + tabela `orders`, com quem as chama |
| `Deployment-Dev` | Laptop do desenvolvedor → LocalStack (API Gateway emulado, Lambda emulado com as três funções, DynamoDB emulado com `orders`) |
| `Deployment-Producao` | Smartphone do cliente (App Mobile), Stripe, AWS → us-east-1 → API Gateway, AWS Lambda (três funções), Amazon DynamoDB (`orders`) |

Uso o tema empacotado `amazon-web-services-2025.07` para os ícones de API Gateway, Lambda e DynamoDB nas deployment views.

## Ponto em aberto: o App Mobile é parte do OrderFlow?

Você descreveu o OrderFlow como "a API serverless" (as três Lambdas + tabela) e o app como quem *chama* a API, então modelei o app como um **sistema separado**, fora da fronteira do OrderFlow. No C4 isso depende de propriedade: **se o seu time também é dono do app e ele faz parte do OrderFlow**, o correto é ele ser um *container* dentro do OrderFlow. Nesse caso a mudança é pequena:

1. Remova o `app = softwareSystem "App Mobile" …` e adicione dentro do `orderflow`:
   `app = container "App Mobile" "App dos clientes para criar e consultar pedidos." "Flutter" { tags "Mobile" }`
2. Troque `app` por `orderflow.app` nos relacionamentos, nos blocos `-/>` e no `instanceOf` do smartphone; troque `cliente -> app` por `cliente -> orderflow.app`.
3. (Opcional) `element "Mobile" { shape mobileDevicePortrait }` em `styles`.

Se confirmar qual é o caso, eu faço a alteração.

## O que deixei de fora de propósito (não foi mencionado)

- Chamadas do OrderFlow *para* o Stripe (criar pagamento etc.) — só modelei o webhook Stripe → OrderFlow. Se `criar-pedido` chama o Stripe, me diga e eu adiciono.
- Em dev, quem chama o API Gateway do LocalStack (app em emulador? `curl`? Stripe CLI encaminhando webhooks?). A view mostra o LocalStack com tudo dentro, mas não inventei o cliente local.

## Como ver e exportar

Preview com live-reload em `http://localhost:8080` (o layout manual é salvo em `workspace.json`, que não deve ser editado à mão):

```
docker run --rm -it -p 8080:8080 -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_AUTOREFRESHINTERVAL=2000 \
    -e STRUCTURIZR_AUTOSAVEINTERVAL=5000 \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr local
```

Revalidar após edições:

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr validate -workspace workspace.dsl
```

Exportar (por exemplo PlantUML ou Mermaid) para `diagrams/`:

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr export -workspace workspace.dsl -format plantuml -output diagrams
```
