Criei o `workspace.dsl` na raiz do repositório com o modelo do **Encurtaí** e os três diagramas pedidos. O DSL foi validado no servidor MCP do Structurizr (`validate` → OK).

## O que foi modelado

**Pessoas e sistemas**
- `Colaborador` — funcionário da empresa.
- `Encurtaí` — o sistema do time (escopo do workspace).
- `Google Workspace` — único sistema externo, usado pela API para SSO (tag `External`).

**Containers do Encurtaí**
| Container | Tecnologia | Papel |
|---|---|---|
| SPA | React (servido por nginx) | interface web |
| API | Go (Gin) | cria links, resolve redirecionamentos, publica eventos |
| Worker de Métricas | Go | consome eventos de clique, grava métricas agregadas |
| Banco de Dados | PostgreSQL 16 | links + métricas (tag `Database` → cilindro) |
| Cache | Redis 7 | redirecionamentos em cache (tag `Database` → cilindro) |
| Fila de Eventos de Clique | RabbitMQ | transporte API → worker (tag `Queue` → pipe) |

A fila é modelada como container (a fila em si, não o broker), seguindo a prática do C4. O nginx entra como tecnologia do SPA, não como container próprio — ele serve os estáticos, não é uma unidade separada que você descreveu.

**Views**
- `SystemContext` — Colaborador, Encurtaí e Google Workspace.
- `Containers` — os seis containers com tecnologias e protocolos nas relações.
- `Redirecionamento` (dinâmica) — Colaborador → API → Cache → (miss) Postgres → publica na fila. Todos os passos são respaldados por relações que existem no modelo.

**Estilos** (viram a legenda automática do Structurizr): `Database` → cilindro, `Queue` → pipe, `External` → cinza, `Person` → ícone de pessoa.

## Como visualizar e exportar

Preview com live-reload em http://localhost:8080:

```
docker run --rm -it -p 8080:8080 -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr local
```

Exportar (ex.: PlantUML/Mermaid/PNG estático) para `diagrams/`:

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr export -workspace workspace.dsl -format mermaid -output diagrams
```

## Dois pontos em aberto (não inventei nada)

1. O `inspect` do Structurizr aponta que o sistema tem containers mas não tem **documentação** (`!docs`) nem **decisões** (`!adrs`). O repositório não tem nenhum diretório de ADRs (`doc/adr`, `docs/decisions`, …), então não emiti `!adrs`. Se você quiser começar um log de decisões, dá para linká-lo depois com uma linha só.
2. Não modelei **deployment** — você não descreveu infraestrutura (onde roda, quantas instâncias, load balancer, ambientes). Se quiser um diagrama de deployment, me diga o ambiente e como cada container é executado.
