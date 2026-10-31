Criei o `workspace.dsl` na raiz do repositório com o modelo C4 do Encurtaí e as três visões pedidas. Validei com `structurizr/structurizr validate` (Docker) e o arquivo passou sem erros.

## O que foi modelado

**Pessoa:** Usuário interno (colaborador da empresa).

**Sistema Encurtaí** (seu time), com seis containers:

| Container | Tecnologia | Tag/estilo |
|---|---|---|
| Aplicação Web | React, servido por nginx | navegador |
| API | Go (Gin) | — |
| Worker de Métricas | Go | — |
| Banco de Dados | PostgreSQL 16 | `Database` → cilindro |
| Cache de Redirecionamentos | Redis 7 | `Database` → cilindro |
| Fila de Eventos de Clique | RabbitMQ | `Queue` → pipe |

**Sistema externo:** Google Workspace, com tag `External` (cinza), usado pela API para autenticação SSO.

Relacionamentos: usuário → SPA (HTTPS) e usuário → API (acesso ao link curto, HTTPS); SPA → API (JSON/HTTPS); API → PostgreSQL (grava e lê links, SQL/TCP); API → Redis (consulta o destino dos links); API → fila (publica eventos de clique, AMQP); fila → worker (entrega eventos, AMQP); worker → PostgreSQL (grava métricas agregadas, SQL/TCP); API → Google Workspace (SSO, HTTPS).

## Visões

- `SystemContext` — contexto do sistema.
- `Containers` — containers do Encurtaí.
- `Redirecionamento` — visão dinâmica com os quatro passos que você descreveu: usuário acessa o link curto → API consulta o cache → em caso de miss, consulta o PostgreSQL → API publica o evento de clique na fila.

## Dois pontos que deixei exatamente como você descreveu

1. **Protocolo do SSO** — você disse "SSO" sem nomear o protocolo (OIDC, SAML…), então a relação com o Google Workspace ficou só com `HTTPS`. Se quiser, me diga qual é e eu adiciono.
2. **Fluxo de redirecionamento** — não incluí um passo "API grava o destino no cache após o miss" nem o redirect de volta ao usuário, porque não estavam na descrição. É só pedir para acrescentar.

## Avisos do `inspect`

O `structurizr inspect` apontou dois itens, ambos sobre coisas que o repositório ainda não tem: o sistema não tem documentação (`!docs`) nem registros de decisão (`!adrs`) anexados. Não criei nenhum dos dois — se o time mantiver um diretório de ADRs (por exemplo `docs/adr`), eu conecto com uma linha `!adrs docs/adr`.

## Como visualizar e exportar

Preview com live-reload em `http://localhost:8080` (salva o layout manual em `workspace.json`):

```bash
docker run --rm -it -p 8080:8080 -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_AUTOREFRESHINTERVAL=2000 \
    -e STRUCTURIZR_AUTOSAVEINTERVAL=5000 \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr local
```

Exportar para `diagrams/` em formato texto (ex.: `mermaid`, `plantuml`, `plantuml/c4plantuml`, `json`):

```bash
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr export -workspace workspace.dsl -format mermaid -output diagrams
```

Para PNG/SVG é preciso a variante `structurizr/structurizr:<versão>-playwright` (a imagem comum não renderiza imagens); descubra a versão com `docker run --rm structurizr/structurizr version` e troque a imagem e o `-format svg` no comando acima.
