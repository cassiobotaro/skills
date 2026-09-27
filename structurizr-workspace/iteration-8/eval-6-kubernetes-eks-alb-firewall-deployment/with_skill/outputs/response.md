Criei o `workspace.dsl` na raiz do repositório e validei com a imagem `structurizr/structurizr` via Docker — sem erros.

**O que foi modelado**

- **Pessoa:** Paciente.
- **Sistema:** Agenda+, com três containers: SPA (React), API (Kotlin, Spring Boot) e Banco de Dados (PostgreSQL).
- **Relações:** Paciente → SPA (HTTPS); SPA → API (JSON/HTTPS); API → Banco de Dados (JDBC/SQL).
- **Ambiente "Produção":**
  - SPA rodando no navegador do paciente.
  - AWS → EKS → cluster `plataforma` → Pod da API com `instances 3` → contêiner da API.
  - AWS → Amazon RDS → PostgreSQL.
  - WAF e Application Load Balancer como `infrastructureNode` (são infraestrutura, então aparecem só na view de deployment, não na de containers). A relação SPA → API é redirecionada nesse ambiente com `-/>` para SPA → WAF → ALB → API.
- **Views:** `SystemContext`, `Containers` e `Deployment-Producao`, todas com `autoLayout`.
- Tema `amazon-web-services-2025.07` (empacotado na imagem) para os ícones da AWS.

**Dois pontos que não inventei — me diga se quiser que eu complete**

1. **Onde o SPA é servido em produção** (S3 + CloudFront? Dentro do mesmo cluster?). Hoje ele aparece apenas rodando no navegador do paciente.
2. **Região da AWS** — não há nó de região porque você não citou uma. Se quiser, adiciono (ex.: `sa-east-1`).

**Para visualizar** (UI em http://localhost:8080, recarrega a cada edição e salva o layout manual em `workspace.json`):

```
docker run --rm -it -p 8080:8080 -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_AUTOREFRESHINTERVAL=2000 \
    -e STRUCTURIZR_AUTOSAVEINTERVAL=5000 \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr local
```

**Para exportar** (ex.: PlantUML, Mermaid, PNG estático) para `diagrams/`:

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr export -workspace workspace.dsl -format plantuml -output diagrams
```

Não edite o `workspace.json` à mão — ele é gerado a partir do DSL e guarda o layout arrastado na UI.
