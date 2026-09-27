Criei o `workspace.dsl` na raiz do repositório com as três visões pedidas e validei com a imagem `structurizr/structurizr` (Docker) — saiu limpo, sem erros.

## Como modelei

**Contexto** — `Cliente` (pessoa) usa o sistema `Mercadin`; `Adyen` é um sistema externo (terceiro), em cinza.

**Containers** — tudo é do time, então tudo fica dentro do sistema `Mercadin`:

- `App Mobile` (React Native) — fala só com o BFF.
- `BFF` (Node.js) — é um container, não um nó de infraestrutura: vocês escreveram e ele tem lógica de negócio (agregação, autorização por perfil, montagem do payload). Se fosse um API Gateway gerenciado, iria só no deployment.
- Três `group`s, um por microsserviço (Catálogo, Pedidos, Pagamentos), cada um com a API (Java / Spring Boot) e o seu schema no Postgres como container de dados (cilindro). Modelei os *schemas* como containers separados porque é essa a fronteira de dados que cada serviço enxerga.
- `Pagamentos API -> Adyen` (HTTPS).

**Deployment de produção** (`Deployment-Producao`) — `Dispositivo do cliente` com o app; `Amazon Web Services` → `ALB` (infrastructureNode) → `Amazon ECS` (AWS Fargate) com uma task Docker para o BFF e para cada serviço; um nó `PostgreSQL` com os três schemas. A relação `App Mobile -> BFF` é reroteada pelo ALB nessa visão (`-/>`), então o ALB só aparece no deployment, como manda o C4. Tema AWS oficial aplicado para os ícones.

## O que ficou em aberto (não inventei)

1. **Protocolo BFF → serviços**: REST/JSON sobre HTTP? gRPC? A relação está sem tecnologia até você confirmar.
2. **BFF → serviços passa pelo ALB?** Você disse que todos rodam atrás de um ALB; hoje só o tráfego do app está roteado pelo ALB. Se as chamadas internas também passam por ele (ou por um ALB interno / service discovery do ECS), me diga e eu ajusto o reroute.
3. **Onde roda o Postgres em produção** (RDS, Aurora, outro)? Deixei um nó `PostgreSQL` genérico dentro da AWS com a nota "hospedagem a confirmar".
4. **Número de tasks** por serviço no Fargate — não coloquei `instances` porque não foi informado.

Respondendo essas quatro, ajusto o arquivo sem mexer em identificadores nem chaves de view (o layout que vocês salvarem fica preservado).

## Para ver e exportar

Preview com live-reload em `http://localhost:8080` (salva o layout manual em `workspace.json`):

```
docker run --rm -it -p 8080:8080 -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_AUTOREFRESHINTERVAL=2000 \
    -e STRUCTURIZR_AUTOSAVEINTERVAL=5000 \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr local
```

Exportar (por exemplo `plantuml`, `mermaid`, `static`) para `diagrams/`:

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr export -workspace workspace.dsl -format <formato> -output diagrams
```

Não há ADRs no repositório, então não incluí `!adrs`; quando existirem, é uma linha para linkar.
