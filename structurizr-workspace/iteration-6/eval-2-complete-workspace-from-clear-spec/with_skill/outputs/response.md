Criei o `workspace.dsl` na raiz do repositório com o modelo do **Encurtaí** e as três visões que você pediu.

## Como classifiquei as peças (C4)

| Elemento | Nível C4 | Por quê |
|---|---|---|
| Usuário da empresa | Person | Quem usa o sistema |
| Encurtaí | Software System | Tudo é do seu time, então é um único sistema |
| SPA (React/nginx) | Container | Precisa estar no ar para o sistema funcionar |
| API (Go/Gin) | Container | Processo executável |
| Worker de Métricas (Go) | Container | Processo executável independente |
| Banco de Dados (PostgreSQL 16) | Container | Data store |
| Cache de Redirecionamentos (Redis 7) | Container | Data store |
| Fila de Eventos de Clique (RabbitMQ) | Container | A fila é modelada como container; o broker em si seria uma preocupação de deployment |
| Google Workspace | Software System externo | Terceiro, fora do seu controle |

## O que ficou no arquivo

- **Contexto (`SystemContext`)** — usuário, Encurtaí e Google Workspace.
- **Containers (`Containers`)** — os seis containers, com tecnologia e protocolo em cada relacionamento.
- **Dinâmico (`RedirecionamentoDeLink`)** — usuário acessa o link curto → API consulta o Redis → em caso de miss busca no PostgreSQL → publica o evento de clique no RabbitMQ.
- **Estilos** — `Database` (cilindro, verde) para PostgreSQL e Redis, `Queue` (pipe, laranja) para o RabbitMQ e `External` (cinza) para o Google Workspace. Os estilos viram automaticamente a legenda dos diagramas.

Detalhes que deixei propositalmente genéricos porque você não especificou: o protocolo do SSO com o Google Workspace está só como `HTTPS` (não assumi OAuth 2.0 nem SAML) — se você me disser qual é, ajusto em um minuto. Também não criei diagrama de deployment, porque você não descreveu a infraestrutura (onde roda, quantas instâncias, load balancer etc.); quando quiser, é só me passar os ambientes.

Não encontrei diretório de ADRs no repositório, então não incluí `!adrs`. Se vocês tiverem um log de decisões em outro lugar, dá para plugar depois.

## Validação

Validei o arquivo de verdade, com a imagem oficial (não há MCP do Structurizr conectado nesta sessão):

```
docker run --rm -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    -v "$PWD":/usr/local/structurizr \
    structurizr/structurizr validate -workspace workspace.dsl
```

Resultado: **sem erros** (exit code 0, nenhuma mensagem de erro — Structurizr CLI 2026.06.28 / DSL 6.2.2).

## Para visualizar e exportar

Preview com live-reload em `http://localhost:8080`:

```
docker run --rm -it -p 8080:8080 -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr local
```

O ajuste manual de layout que você fizer na UI é salvo em `workspace.json` — nunca edite esse arquivo à mão, ele é gerado a partir do DSL.

Exportar para outro formato (`plantuml`, `mermaid`, `png` via `static`, `json`, `dot`, `d2`, `ilograph`):

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr export -workspace workspace.json -format mermaid -output diagrams
```

(Rode o preview pelo menos uma vez antes, para o `workspace.json` existir com o layout; ou exporte direto do DSL com `-workspace workspace.dsl`.)
