Criei o `workspace.dsl` na raiz do repositório com o modelo C4 do Encurtaí, exatamente com o que você descreveu — nada foi acrescentado além do que está na sua mensagem.

**Modelo**

- Pessoa: *Usuário da empresa*.
- Sistema *Encurtaí* com seis containers: *Aplicação Web* (React, SPA servido por nginx), *API* (Go/Gin, REST), *Banco de Dados* (PostgreSQL 16), *Cache de Redirecionamentos* (Redis 7), *Fila de Eventos de Clique* (RabbitMQ) e *Worker de Métricas* (Go).
- Sistema externo: *Google Workspace*, usado pela API para SSO.
- Relacionamentos com rótulo direcional e protocolo: SPA → API (JSON/HTTPS), API → Postgres e Worker → Postgres (SQL/TCP), API → Redis (RESP/TCP), API → fila e fila → worker (AMQP), API → Google Workspace (HTTPS).

**Views**

- `SystemContext` — contexto do sistema.
- `Containers` — diagrama de containers.
- `RedirecionamentoLink` — diagrama dinâmico com o fluxo pedido: usuário acessa o link curto → API consulta o cache → em caso de miss consulta o Postgres → publica o evento de clique na fila → responde com o redirecionamento (o último passo é uma resposta, renderizada tracejada).

**Estilos** (por tag, então aparecem na legenda): `Database` → cilindro (Postgres e Redis), `Queue` → *pipe* laranja (RabbitMQ), `External` → cinza (Google Workspace); pessoa com forma de pessoa e a SPA com forma de navegador.

**Validação**: rodei `structurizr/structurizr validate` via Docker e o arquivo passou sem erros.

Duas coisas que deixei de fora de propósito, por não estarem na descrição — me diga se quiser incluí-las:

1. No fluxo dinâmico, a API grava o destino no Redis após um cache miss? Modelei só a consulta; o relacionamento "Consulta e armazena redirecionamentos em" já cobre a escrita, então basta acrescentar um passo.
2. O protocolo do SSO com o Google Workspace (OIDC, SAML…). Deixei apenas "HTTPS" para não chutar.

**Para visualizar** (UI em http://localhost:8080, com recarga automática e layout manual salvo em `workspace.json`):

```
docker run --rm -it -p 8080:8080 -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_AUTOREFRESHINTERVAL=2000 \
    -e STRUCTURIZR_AUTOSAVEINTERVAL=5000 \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr local
```

**Para exportar** (ex.: PlantUML, Mermaid, PNG via `static`) para `diagrams/`:

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr export -workspace workspace.dsl -format <formato> -output diagrams
```

Não edite o `workspace.json` à mão — ele é gerado a partir do DSL e guarda o layout arrumado na UI.

---

**Arquivos escritos**
- `workspace.dsl` (raiz do repositório)

**Referências do skill lidas**
- `SKILL.md`
- `references/dsl-reference.md` (sempre)
- `references/diagrams.md` (escolha das views + checklist de revisão)
- `references/modeling-patterns.md` (§2, fila/mensageria)

**Validador**
- `docker run --rm -u $(id -u):$(id -g) -v "$PWD":/usr/local/structurizr -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes structurizr/structurizr validate -workspace workspace.dsl`
- Resultado: exit 0, sem erros reportados (saída vazia). Confirmado que o validador falha em DSL inválido (exit 1) e, via export JSON, que a view dinâmica tem os 5 passos, o último como resposta.
