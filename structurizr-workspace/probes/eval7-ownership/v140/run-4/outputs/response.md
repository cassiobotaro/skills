Criei o `workspace.dsl` na raiz do repositório e validei com o `structurizr/structurizr` via Docker: passou sem erros.

## O que foi modelado

**Modelo (C4)**

- **Cliente** (pessoa) usa o **App Mobile** (Flutter).
- **OrderFlow** (sistema) com cinco containers: App Mobile, as três funções `criar-pedido`, `listar-pedidos` e `webhook-pagamento` (Python / AWS Lambda) e a **Tabela orders** (Amazon DynamoDB). As três funções leem e gravam na tabela, como você descreveu.
- **Stripe** como sistema externo, enviando eventos de pagamento para o `webhook-pagamento`.
- O **API Gateway não aparece na view de containers**: como ele só roteia e valida API key (nada custom), em C4 ele é um conceito de deployment, então entrou como `infrastructureNode` nos dois ambientes. Nas deployment views as chamadas App → Lambda e Stripe → webhook são redirecionadas (`-/>`) para passar pelo gateway.

**Views**

| Chave | Conteúdo |
|---|---|
| `SystemContext` | Cliente, OrderFlow e Stripe (o par contexto + containers é a recomendação padrão do C4, por isso incluí o contexto) |
| `Containers` | os cinco containers e a Stripe |
| `Deployment-Dev` | Laptop do desenvolvedor → LocalStack (API Gateway, Lambda, DynamoDB emulados) + o app no próprio laptop |
| `Deployment-Prod` | AWS / us-east-1 → API Gateway, AWS Lambda, Amazon DynamoDB; smartphone do cliente; Stripe |

Usei o tema `amazon-web-services-2025.07` (já vem na imagem Docker) para os ícones de API Gateway, Lambda e DynamoDB.

## Pontos para você confirmar

Preferi deixar lacunas a inventar; ajuste o que estiver diferente da realidade:

1. **App em dev** — como você disse que "cada dev roda tudo no laptop", coloquei uma instância do App Mobile no nó do laptop. Se em dev vocês só testam a API (curl/Postman) sem o app, basta remover a linha `instanceOf orderflow.app` do nó `laptop` e o bloco `-/>` de dev.
2. **Stripe em dev** — não coloquei a Stripe no ambiente de desenvolvimento, porque não sei como o webhook chega no laptop (Stripe CLI com forward? não chega?). Me diga e eu acrescento.
3. **Protocolos** — usei `HTTPS` (app → API), `Webhook/HTTPS` (Stripe → webhook) e `AWS SDK/HTTPS` (Lambda → DynamoDB) como rótulos genéricos; refine se quiser algo mais específico.

## Como ver e exportar

Preview com live-reload em `http://localhost:8080` (o layout manual fica salvo em `workspace.json`, que não deve ser editado à mão):

```
docker run --rm -it -p 8080:8080 -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_AUTOREFRESHINTERVAL=2000 \
    -e STRUCTURIZR_AUTOSAVEINTERVAL=5000 \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr local
```

Exportar (por exemplo para PlantUML ou Mermaid) para a pasta `diagrams/`:

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr export -workspace workspace.dsl -format plantuml -output diagrams
```

Revalidar depois de editar:

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr validate -workspace workspace.dsl
```
