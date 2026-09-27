Criei o `workspace.dsl` na raiz do repositório e validei com a imagem `structurizr/structurizr` (Docker): a validação terminou limpa, sem erros.

## O que está no modelo

**Pessoas e sistemas**
- `Cliente` (pessoa) → usa o `App Mobile`.
- `App Mobile` (Flutter) — modelado como um **sistema separado** que chama o OrderFlow (veja a pergunta abaixo).
- `OrderFlow` — o sistema em foco, com quatro containers:
  - `criar-pedido`, `listar-pedidos`, `webhook-pagamento` — `AWS Lambda (Python)`, via um archetype `lambda` para não repetir tecnologia e tags;
  - `orders` — tabela `Amazon DynamoDB` (tag `Database`, desenhada como cilindro).
- `Stripe` (sistema externo) → notifica eventos de pagamento para `webhook-pagamento`.
- As três funções têm a mesma relação com a tabela ("Lê e grava pedidos em", `DynamoDB API/HTTPS`), como você descreveu.

**O API Gateway não é um container.** Como ele só roteia e autentica por API key (sem lógica custom), é um `infrastructureNode` nos ambientes de deployment. Em produção, as relações lógicas `App Mobile → lambdas` e `Stripe → webhook` são redirecionadas por ele com `-/>`, então a deployment view mostra o caminho real (cliente/Stripe → API Gateway → Lambda), enquanto a view de containers continua mostrando só quem fala com quem.

**Views** (todas com `autoLayout`):
- `SystemContext` e `Containers` (a dupla que o C4 recomenda sempre).
- `Deployment-Dev` — `Laptop do desenvolvedor` → `LocalStack` → API Gateway (emulado), Lambda (emulado) com as três funções e DynamoDB (emulado) com a tabela.
- `Deployment-Prod` — `Amazon Web Services` → `us-east-1` → `Amazon API Gateway`, `AWS Lambda` (três funções) e `Amazon DynamoDB`; mais o dispositivo do cliente e o Stripe como origem das chamadas. O tema `amazon-web-services-2025.07` (empacotado na imagem) põe os ícones AWS.

## Uma pergunta antes de fechar

Quem é dono do **app Flutter**? Você chamou o OrderFlow de "nossa API", então deixei o app fora da fronteira do sistema, como um sistema separado que a consome. Se for o **mesmo time** que mantém a API, o correto em C4 é ele ser um *container* do OrderFlow — nesse caso eu movo `app` para dentro de `orderflow` (vira `orderflow.app = container "App Mobile" "..." "Flutter"`) e ajusto as relações e a instância em produção; a mudança é pequena e vale mais a pena fazer agora do que depois de você arrumar o layout.

Deixei de fora, por não ter sido descrito: o app ou o Stripe apontando para o LocalStack em dev (a view de dev mostra só o que roda no laptop), e qualquer chamada das lambdas *para* o Stripe (por exemplo, `criar-pedido` criando a cobrança). Se existir, me diz que eu adiciono.

## Para ver e exportar

Preview com live-reload em `http://localhost:8080` (o layout manual fica salvo em `workspace.json`, que não deve ser editado à mão):

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
