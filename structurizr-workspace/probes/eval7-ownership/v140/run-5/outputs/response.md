Escrevi o `workspace.dsl` do OrderFlow na raiz do repositório e validei com a imagem `structurizr/structurizr` via Docker — passou sem erros.

## Como modelei

**Modelo (C4)**

- **Cliente** (pessoa) → usa o **App Mobile** (container, Flutter).
- **OrderFlow** (software system) com cinco containers: `App Mobile`, as três funções `criar-pedido`, `listar-pedidos` e `webhook-pagamento` (Python, AWS Lambda) e a `Tabela orders` (Amazon DynamoDB). Cada função tem sua própria relação "lê e grava" com a tabela, como você descreveu.
- **Stripe** como sistema externo, que envia eventos de pagamento para o `webhook-pagamento`.
- **API Gateway não é container.** Como ele só faz roteamento e auth por API key (nada custom), é um conceito de implantação: entra como `infrastructureNode` nas duas deployment views e o tráfego app → lambdas (e Stripe → webhook) é redirecionado por ele com `-/>`. Na container view as chamadas aparecem diretas app → função, que é a estrutura lógica.

**Views**

- `SystemContext` — adicionei além do que você pediu, porque o C4 recomenda o par contexto + containers e ela custa zero manutenção.
- `Containers` — a view que você pediu.
- `Deployment-Dev` — laptop do dev com o app Flutter rodando localmente e um nó **LocalStack** emulando API Gateway, Lambda (três instâncias) e DynamoDB.
- `Deployment-Production` — AWS → us-east-1 → API Gateway, AWS Lambda (três funções) e Amazon DynamoDB; o app no smartphone do cliente e o Stripe fora da AWS. Usei o tema `amazon-web-services-2025.07` (empacotado na imagem) com as tags de ícone de Lambda, DynamoDB, API Gateway, Region e AWS Cloud — conferi que os cinco nomes existem nessa versão do tema.

## Pontos em aberto (não inventei, deixei de fora)

1. **Stripe em dev** — não modelei o Stripe na deployment view de dev, porque você não disse como o webhook chega no LocalStack (Stripe CLI encaminhando, mock, nada). Me diga e eu adiciono.
2. **OrderFlow chama o Stripe?** — só modelei a direção Stripe → webhook. Se `criar-pedido` cria o pagamento no Stripe (PaymentIntent/Checkout), falta uma relação `criar-pedido → Stripe`.
3. **Onde o app Flutter roda em dev** — coloquei como "execução local" no laptop, sem afirmar emulador ou dispositivo físico.

## Ver e exportar

Preview com live-reload em `http://localhost:8080` (o layout manual fica salvo em `workspace.json`, que não deve ser editado à mão):

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

Revalidar depois de qualquer edição:

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr validate -workspace workspace.dsl
```
