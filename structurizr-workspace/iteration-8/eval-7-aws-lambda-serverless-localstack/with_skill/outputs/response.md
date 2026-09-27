Criei o `workspace.dsl` na raiz do repositório e validei com o `structurizr/structurizr` via Docker (saída limpa, sem erros).

## O que foi modelado

**Modelo**

- **Cliente** (pessoa) usa o **App Mobile** (Flutter), modelado como um software system à parte que chama o OrderFlow.
- **OrderFlow** (o sistema em foco) com quatro containers:
  - `criar-pedido`, `listar-pedidos`, `webhook-pagamento` — funções Lambda em Python (declaradas via um archetype `lambda`, para não repetir tecnologia e tag em cada uma);
  - `Tabela orders` — Amazon DynamoDB, estilizada como cilindro.
  - As três funções leem e gravam na tabela (`DynamoDB API/HTTPS`).
- **Stripe** (sistema externo, cinza) envia eventos de pagamento ao `webhook-pagamento`.
- O **API Gateway não aparece na view de containers**: como só faz roteamento e auth por API key, é um conceito de deployment (`infrastructureNode`), e entra apenas nas deployment views.

**Views** (`autoLayout` em todas; chaves estáveis para não perder layout salvo)

| Chave | Conteúdo |
|---|---|
| `SystemContext` | OrderFlow, Cliente, App Mobile e Stripe (recomendada pelo C4, vem junto com a de containers) |
| `Containers` | as três Lambdas e a tabela DynamoDB, com App Mobile e Stripe ao redor |
| `Deployment-Desenvolvimento` | Laptop do dev → LocalStack → API Gateway (emulado), Lambda com as três funções, DynamoDB com a tabela |
| `Deployment-Producao` | AWS → us-east-1 → API Gateway, AWS Lambda (três funções), Amazon DynamoDB; smartphone do cliente com o app e o Stripe como origens das chamadas |

Em produção as chamadas do app e o webhook do Stripe são **reencaminhadas pelo API Gateway** (`-/>`): a seta direta app → Lambda some e no lugar aparecem app → API Gateway → Lambda (idem para Stripe → API Gateway → webhook). O tema `amazon-web-services-2025.07` (empacotado na imagem) coloca os ícones da AWS nos nós de produção.

## Dois pontos que deixei em aberto de propósito

1. **App Mobile como sistema separado.** Você descreveu o OrderFlow como "a API", então o app ficou fora da fronteira. Se o mesmo time é dono do app e da API, ele deveria ser um *container* dentro do OrderFlow — é uma mudança de três linhas, me avise.
2. **Ambiente de dev sem App Mobile nem Stripe.** Só modelei o que você disse que roda no LocalStack. Se em dev o app roda num emulador no mesmo laptop, ou se o webhook do Stripe chega via Stripe CLI/túnel, me diga como e eu acrescento ao ambiente.

## Como visualizar e exportar

Preview com live reload em `http://localhost:8080` (o layout manual é salvo em `workspace.json` — não edite esse arquivo à mão):

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

Exportar (por exemplo para PlantUML ou Mermaid) para `diagrams/`:

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr export -workspace workspace.dsl -format plantuml -output diagrams
```
