Criei o `workspace.dsl` na raiz do repositório com o modelo C4 do Agenda+ e as três views pedidas. O arquivo foi validado com `structurizr/structurizr validate` (Docker) e passou sem erros.

## O que está no modelo

**Pessoa e sistema**
- `Paciente` → usa o `Agenda+`.

**Containers do Agenda+**
- `SPA` (React) — interface usada pelos pacientes.
- `API` (Kotlin, Spring Boot) — expõe as operações de agendamento.
- `Banco de Dados` (PostgreSQL) — armazena os dados de agendamento.

**Relacionamentos**
- Paciente → SPA: "Agenda consultas usando" (HTTPS)
- SPA → API: "Faz chamadas de API para" (JSON/HTTPS)
- API → Banco de Dados: "Lê e grava dados de agendamento em" (SQL/TCP)

**Ambiente de deployment `Produção`**
- `Computador do Paciente` › `Navegador Web` › instância da SPA.
- `Amazon Web Services`
  - `AWS WAF` (infrastructureNode) — firewall na frente do ALB.
  - `Application Load Balancer` (infrastructureNode) — na frente da API.
  - `plataforma` (Amazon EKS) › `Pod da API` (Kubernetes Pod, **3 instâncias**) › instância da API.
  - `Amazon RDS` › `PostgreSQL` › instância do Banco de Dados.
- A relação SPA → API é reroteada no deployment com `-/>` para passar por **WAF → ALB → API**. Isso mantém WAF e ALB fora da view de containers (são preocupações de deployment) e os mostra apenas na view de produção.

**Views**: `SystemContext`, `Containers` e `Deployment-Producao`. Os temas embutidos `amazon-web-services-2025.07` e `kubernetes` dão os ícones de WAF, ALB, EKS, RDS e Pod.

## Dois pontos que não modelei, porque você não os descreveu

1. **Onde a SPA é servida em produção** (S3 + CloudFront? o próprio EKS?). Hoje só aparece rodando no navegador do paciente. Se quiser, me diga onde os arquivos estáticos ficam hospedados e eu adiciono o nó.
2. **Região da AWS** (ex.: `sa-east-1`). Não coloquei um nó de região para não inventar; é uma linha a acrescentar se você quiser.

## Como visualizar

Preview com live-reload em `http://localhost:8080` (o layout manual fica salvo em `workspace.json`, que não deve ser editado à mão):

```
docker run --rm -it -p 8080:8080 -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_AUTOREFRESHINTERVAL=2000 \
    -e STRUCTURIZR_AUTOSAVEINTERVAL=5000 \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr local
```

Para revalidar depois de editar:

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr validate -workspace workspace.dsl
```

Para exportar (`plantuml`, `mermaid`, `json`, `dot`, `ilograph`, `d2`, `static`) para a pasta `diagrams/`:

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr export -workspace workspace.dsl -format <formato> -output diagrams
```
