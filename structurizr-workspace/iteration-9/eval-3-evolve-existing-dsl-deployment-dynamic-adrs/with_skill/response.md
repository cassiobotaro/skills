Evoluí o `workspace.dsl` com os três itens pedidos, só adicionando blocos novos — nenhum identificador, rótulo, view ou estilo existente foi alterado, então o layout que vocês já tenham salvo no `workspace.json` continua válido.

## O que mudou

**1. Ambiente de produção na AWS** (bloco `producao = deploymentEnvironment "Produção"` no `model`)

- `Amazon Web Services` → `Amazon ECS` (tecnologia `AWS Fargate`) com três tasks: `Portal Task` (1 instância do Portal Web), `API Task` (**`instances 2`** da API de Faturamento) e `Worker Task` (1 instância do Worker).
- `Amazon RDS` → `PostgreSQL` com a instância do Banco de Dados.
- `Application Load Balancer` como `infrastructureNode` na frente da API. A relação lógica Portal → API foi redirecionada no ambiente com `-/>`: no diagrama de deployment aparece Portal → ALB → API; os diagramas de contexto e de containers continuam iguais (o ALB é um conceito de deployment e não entra neles).
- Os nós carregam as tags do tema `amazon-web-services-2025.07` (bundled na imagem Docker), adicionado com uma linha `theme` no fim de `views`. O tema só estiliza elementos com tag `Amazon Web Services - …`, então os diagramas existentes não mudam de aparência.
- View nova: `deployment faturamento "Produção" "Deployment-Producao"`.

**2. Diagrama dinâmico "Emissão de fatura"** (`dynamic faturamento "EmissaoDeFatura"`)

Seis passos, cada um respaldado por uma relação que já existia no modelo (o validador rejeita passos sem relação de suporte):

1. Atendente → Portal Web: emite a fatura
2. Portal Web → API: envia a fatura (JSON/HTTPS)
3. API → Banco de Dados: grava a fatura (SQL/TCP)
4. API → Fila de Faturas: publica a fatura emitida
5. Worker → Fila de Faturas: consome a fatura
6. Worker → ERP: envia a fatura (HTTPS)

Não incluí o passo "Worker atualiza status no banco" porque ele não fazia parte do fluxo que você descreveu — se fizer sentido, é uma linha a mais entre os passos 5 e 6 (a relação já existe no modelo).

**3. ADRs vinculados**: `!adrs docs/adr` no escopo do workspace. Os três arquivos seguem o formato adr-tools (`# N. Título`, `Date:`, `## Status`), que é o importador padrão, então nada mais foi necessário. Na exportação aparecem as três decisões: "Registrar decisões de arquitetura", "Usar PostgreSQL como banco de dados" e "Processamento assíncrono com RabbitMQ".

## Validação

Rodei `structurizr/structurizr validate` (Docker) no diretório do repositório: saiu limpo, exit 0, sem erros nem avisos. Também exportei uma cópia para JSON e conferi que as views novas e os três ADRs estão lá. Nenhum `workspace.json` foi gerado dentro do repositório.

## Dois pontos que ficaram em aberto (não inventei)

1. **Onde roda o RabbitMQ em produção?** Você não mencionou a fila no ambiente AWS, então ela **não** aparece no diagrama de deployment — e por isso as setas API → Fila e Worker → Fila também não aparecem lá (o Structurizr só desenha relações entre instâncias presentes no ambiente). Me diga o que é (Amazon MQ? container no mesmo cluster ECS? EC2?) e eu adiciono o nó.
2. **O ERP deve aparecer no deployment?** Ele é externo e mantido por terceiro; sem saber onde/como é acessado, deixei de fora. Se quiser vê-lo no diagrama de deployment, basta um `deploymentNode` para ele com `instanceOf erp` — me diz como vocês o enxergam (data center do fornecedor, SaaS, etc.).

Também não mencionei uma região AWS porque você não citou; se houver uma (ex.: `sa-east-1`), dá para inserir um nó de região entre o nó AWS e os serviços.

Sugestão opcional, fora do escopo pedido: o workspace não tem `configuration { scope softwaresystem }`; adicionar isso deixa explícito que é um workspace de sistema único. Não incluí para manter o diff mínimo.

## Para visualizar e exportar

Preview com live-reload em `http://localhost:8080` (salva o layout manual em `workspace.json`):

```
docker run --rm -it -p 8080:8080 -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_AUTOREFRESHINTERVAL=2000 \
    -e STRUCTURIZR_AUTOSAVEINTERVAL=5000 \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr local
```

Exportar (ex.: PlantUML ou Mermaid) para `diagrams/`:

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr export -workspace workspace.dsl -format plantuml -output diagrams
```

---

**Arquivos escritos**

- `workspace.dsl` (editado: `!adrs`, `deploymentEnvironment "Produção"`, view `EmissaoDeFatura`, view `Deployment-Producao`, `theme amazon-web-services-2025.07`)

**Referências do skill lidas**

- `references/dsl-reference.md`
- `references/deployment-patterns.md`

**Validador executado**

- `docker run --rm -u $(id -u):$(id -g) -v "$PWD":/usr/local/structurizr -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes structurizr/structurizr validate -workspace workspace.dsl` — resultado: **exit 0, sem saída** (nenhum erro ou aviso). Controle negativo com uma cópia deliberadamente quebrada retornou `ERROR … The destination element "faturamento.naoexiste" does not exist`, exit 1, confirmando que o validador está reportando de verdade.
