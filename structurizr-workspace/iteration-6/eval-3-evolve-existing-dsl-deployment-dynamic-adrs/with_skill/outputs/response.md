Evoluí o `workspace.dsl` de forma puramente aditiva — nenhuma linha existente foi alterada ou removida.

## O que foi adicionado

**1. Ambiente de produção na AWS** (`deploymentEnvironment "Produção"`)

- `deploymentNode "Amazon Web Services"` contendo:
  - `infrastructureNode "Application Load Balancer"` na frente da API;
  - `deploymentNode "Amazon ECS" ... "AWS Fargate"` com três tarefas (`Docker Container`): Portal Web, API (`instances 2`) e Worker;
  - `deploymentNode "Amazon RDS" ... "RDS PostgreSQL"` com a instância do Banco de Dados.
- O ALB entra pelo reroteamento `portal -/> api`, que é a forma correta em C4: load balancer é conceito de *deployment*, não container — por isso ele aparece só na visão de deployment e a visão de containers continua intacta.
- Adicionei o tema `amazon-web-services-2025.07` (empacotado na imagem oficial) e as tags dos serviços, para os ícones AWS na visão de deployment.

**2. Visão dinâmica "Emissão de fatura"** (`dynamic faturamento "EmissaoDeFatura"`) com os seis passos que você descreveu: atendente → portal → API → banco → fila → worker → ERP. Todos os passos usam relacionamentos que **já existiam** no modelo; nenhum relacionamento novo foi inventado.

**3. ADRs vinculados**: `!adrs docs/adr` no escopo do workspace. Os arquivos estão no formato adr-tools (`# N. Título`, `Date:`, `## Status/Context/Decision/Consequences`), que é o importador padrão — não precisou de parâmetro extra. As três decisões passam a aparecer no log de decisões do workspace.

## Validação

Não há servidor MCP do Structurizr conectado nesta sessão, então usei o fallback via Docker:

```
docker run --rm -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    -v "$PWD":/usr/local/structurizr structurizr/structurizr validate -workspace workspace.dsl
```

Resultado: **validou limpo** (saída vazia, exit 0 — confirmei que o comando realmente acusa erro quando existe, testando antes com um DSL quebrado).

## Um ponto em aberto (não inventei)

Você não disse onde a **Fila de Faturas (RabbitMQ)** roda em produção — Amazon MQ, um serviço no próprio ECS, ou uma instância gerenciada por outro time? Por isso ela ficou de fora do ambiente de produção: prefiro a lacuna a colocar uma infraestrutura que você não confirmou. Me diga qual é o caso e eu adiciono o nó (e, se quiser, a região da AWS, que também não foi especificada).

## Para visualizar

```
docker run --rm -it -p 8080:8080 -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr local
```

Abra `http://localhost:8080` — as novas visões são **Emissão de fatura** (dinâmica) e **Deployment-Producao**, além do log de decisões vindo de `docs/adr`.
