Evoluí o `workspace.dsl` com as três mudanças pedidas, sem alterar o que já existia (identificadores, nomes, relacionamentos, views `Contexto`/`Containers` e estilos foram preservados). O arquivo foi validado com `structurizr/structurizr validate` via Docker e passou limpo.

## O que foi adicionado

**1. Ambiente de produção na AWS** (`producao = deploymentEnvironment "Produção"`)

- `Amazon Web Services` → `Amazon ECS` (tecnologia `AWS Fargate`) com três nós:
  - `Task do Portal` → instância de `faturamento.portal`
  - `Task da API` → instância de `faturamento.api`, `instances 2`
  - `Task do Worker` → instância de `faturamento.worker`
- `Amazon RDS` → `PostgreSQL` → instância de `faturamento.banco`
- `Application Load Balancer` como `infrastructureNode` (é conceito de deploy, não aparece na view de containers). A chamada Portal → API foi reroteada com `-/>` para passar pelo ALB: `Portal → ALB "Chama" (JSON/HTTPS)` e `ALB → API "Encaminha requisições para" (JSON/HTTPS)`.
- Nova view `deployment faturamento producao "Deployment-Producao"`.
- Tema `amazon-web-services-2025.07` (bundled na imagem, resolve offline) com tags nos nós AWS para os ícones, e estilo `Infrastructure Node` em elipse para distinguir o ALB dos nós de deploy. Ambos são cosméticos.

**2. Diagrama dinâmico "Emissão de fatura"** (`dynamic faturamento "EmissaoFatura"`), seis passos, todos apoiados em relacionamentos que já existiam no modelo:

1. Atendente → Portal Web: "Emite a fatura em"
2. Portal Web → API de Faturamento: "Envia a fatura emitida para"
3. API → Banco de Dados: "Grava a fatura em"
4. API → Fila de Faturas: "Publica a fatura emitida em"
5. Worker → Fila de Faturas: "Consome a fatura de"
6. Worker → ERP: "Envia a fatura para"

**3. ADRs vinculados**: `!adrs docs/adr` no escopo do workspace. Os três arquivos estão no formato adr-tools/Nygard (`# N. Título`, `Date:`, `## Status`), que é o importador padrão — a validação confirmou a importação das decisões 1, 2 e 3.

## Pontos que deixei em aberto de propósito

Não inventei nada que você não descreveu, então estes itens ficaram fora do ambiente de produção. Me diga e eu completo:

1. **Onde o RabbitMQ roda em produção?** (Amazon MQ, um serviço no próprio ECS, um broker fora da AWS, …) Sem isso a `Fila de Faturas` não tem instância no deployment, e as setas API → Fila e Worker → Fila não aparecem na view `Deployment-Producao`.
2. **Região AWS** — não modelei um nó de região; se quiser (ex.: `sa-east-1`), acrescento um `deploymentNode` entre a conta e os serviços.
3. **Quantidade de instâncias do Portal e do Worker** — ficaram no padrão (1), já que só a API teve o número informado.
4. **O ALB também fica na frente do Portal?** Modelei apenas o que foi dito: ALB na frente da API. Se o atendente acessa o Portal via outro ALB/CloudFront, é mais um nó.

## Como visualizar e exportar

Preview com live-reload em `http://localhost:8080` (salva o layout manual em `workspace.json`):

```
docker run --rm -it -p 8080:8080 -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_AUTOREFRESHINTERVAL=2000 \
    -e STRUCTURIZR_AUTOSAVEINTERVAL=5000 \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr local
```

Export (ex.: `plantuml`, `mermaid`, `json`, `static`) para `diagrams/`:

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr export -workspace workspace.dsl -format <formato> -output diagrams
```

---

**Arquivos escritos**
- `workspace.dsl` (editado: `!adrs`, ambiente `producao`, views `EmissaoFatura` e `Deployment-Producao`, estilo `Infrastructure Node`, `theme`)

**Referências do skill lidas**
- `SKILL.md`
- `references/dsl-reference.md`
- `references/deployment-patterns.md`
- `references/diagrams.md`

**Validador executado**
- `docker run --rm -u $(id -u):$(id -g) -v "$PWD":/usr/local/structurizr -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes structurizr/structurizr validate -workspace workspace.dsl` — executado na raiz do repositório; resultado: **exit code 0, nenhum erro reportado** (saída vazia). Um canário com um erro proposital no mesmo arquivo falhou com `The destination element "faturamento.naoexiste" does not exist at line 68` (exit 1), confirmando que o validador estava de fato analisando o arquivo. Um export JSON de uma cópia em diretório temporário confirmou 3 decisões importadas, a view dinâmica com 6 passos e a view de deployment com 12 elementos; nenhum arquivo além de `workspace.dsl` foi criado no repositório.
