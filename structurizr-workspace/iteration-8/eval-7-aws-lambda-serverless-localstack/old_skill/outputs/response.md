Criei o `workspace.dsl` na raiz do repositório e validei com a imagem `structurizr/structurizr` (Docker) — parse limpo, sem erros.

## Como modelei

**Modelo (C4)**

- **Pessoa:** `Cliente` — usa o app mobile.
- **App Mobile** (Flutter) — modelado como *software system externo*, já que você descreveu o OrderFlow como "a API" e o app como "dos clientes". Se o app for do mesmo time que a API, é só mover o bloco para dentro de `orderflow` como `container "App Mobile" "..." "Flutter"` e ajustar as duas relações; aviso porque isso muda o que aparece na view de containers.
- **Stripe** — software system externo; envia os eventos de pagamento para a função `webhook-pagamento`.
- **OrderFlow** — um software system com quatro containers:
  - `criar-pedido`, `listar-pedidos`, `webhook-pagamento` — cada Lambda em Python é um container (uma função serverless é uma unidade que roda separadamente);
  - `Tabela orders` — Amazon DynamoDB, com tag `Database` (cilindro). As três funções leem e escrevem nela, como você descreveu.
- **Amazon API Gateway** — como faz só roteamento e auth por API key (nada custom), é um conceito de *deployment*, não um container: aparece como `infrastructureNode` nos dois ambientes, e não na view de containers. Em produção, as chamadas App Mobile → funções e Stripe → webhook são reencaminhadas pelo gateway com `-/>`, então o diagrama mostra o caminho real (`App Mobile → API Gateway → criar-pedido`, etc.).

**Ambientes de deployment**

- `Desenvolvimento` — `Laptop do desenvolvedor` → `LocalStack` → API Gateway, Lambda (3 funções) e DynamoDB emulados.
- `Produção` — `Amazon Web Services` → `us-east-1` → API Gateway, AWS Lambda (3 funções) e Amazon DynamoDB; mais o smartphone do cliente (instância do App Mobile) e o Stripe, para que as chamadas externas apareçam no diagrama.

**Views:** `SystemContext` (recomendada pelo C4, vem junto), `Containers`, `Deployment-Dev` e `Deployment-Prod`. Uso o tema `amazon-web-services-2025.07` (empacotado na imagem) para os ícones de Lambda, DynamoDB e API Gateway nas views de deployment.

## Pontos que não inventei — me confirme se quiser que eu complete

1. **Stripe no ambiente de dev.** Não coloquei o Stripe na view de dev porque você não disse como o webhook é acionado no laptop (Stripe CLI encaminhando eventos? chamada manual?). Se for Stripe CLI, adiciono um nó para isso.
2. **App Mobile no ambiente de dev.** Pelo mesmo motivo (emulador no laptop? só `curl`?), a view de dev mostra o gateway invocando as funções, sem o cliente que chama o gateway.
3. **OrderFlow chama o Stripe?** Só modelei a direção que você descreveu (Stripe → webhook). Se `criar-pedido` cria o pagamento no Stripe (payment intent / checkout), me diga e adiciono a relação.

## Para ver e exportar

Preview com live-reload em `http://localhost:8080` (o layout manual é salvo em `workspace.json` — não edite esse arquivo à mão):

```
docker run --rm -it -p 8080:8080 -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_AUTOREFRESHINTERVAL=2000 \
    -e STRUCTURIZR_AUTOSAVEINTERVAL=5000 \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr local
```

Revalidar depois de editar:

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr validate -workspace workspace.dsl
```

Exportar (ex.: `plantuml`, `mermaid`, `static`) para `diagrams/`:

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr export -workspace workspace.dsl -format plantuml -output diagrams
```
