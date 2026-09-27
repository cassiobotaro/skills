Criei o `workspace.dsl` na raiz do repositório com as três visões pedidas, e ele passou limpo na validação (`structurizr/structurizr validate`, sem erros).

## Como modelei

**Contexto** — `Cliente` (pessoa) usa o sistema `Mercadin`; `Adyen` é um sistema externo (PSP), em cinza.

**Containers** — tudo dentro de um único sistema `Mercadin`, porque o time é um só:

- `App Mobile` (React Native) — fala só com o BFF.
- `BFF` (Node.js) — modelado como **container**, não como infraestrutura: ele tem lógica de negócio (agregação, autorização por perfil, montagem do payload), então é um pedaço do sistema que vocês escreveram e mantêm.
- Três `group`s, um por microsserviço, cada um com a API (Java / Spring Boot) e o seu schema no Postgres como container de dados (`Schema Catálogo`, `Schema Pedidos`, `Schema Pagamentos`, cilindros). O schema é a unidade de dados que cada serviço possui; a instância física do Postgres aparece só no deployment.
- `Serviço de Pagamentos -> Adyen` via HTTPS.

**Deployment de produção** (`Deployment-Producao`) — `Smartphone do cliente` com o app; dentro de `Amazon Web Services`: o `ALB` como `infrastructureNode`, o cluster `Amazon ECS` (Fargate) com uma task Docker por serviço e uma para o BFF, e um nó `PostgreSQL` com os três schemas. As relações lógicas foram reroteadas (`-/>`) para passar pelo ALB: app → ALB → BFF e BFF → ALB → cada serviço. O tema oficial da AWS (`amazon-web-services-2025.07`, embutido na imagem) dá os ícones.

## O que assumi — confira

1. **Protocolos**: usei `JSON/HTTPS` app→BFF e `JSON/HTTP` BFF→serviços. Se os serviços expõem gRPC ou outro formato, é só trocar a string nas relações.
2. **BFF → serviços via ALB**: você disse que cada serviço e o BFF ficam atrás de um ALB, então rotei as chamadas internas por ele também. Se o BFF chega nos serviços por service discovery / rede interna do cluster, remova os três blocos `mercadin.bff -/> …` do ambiente de produção.
3. **Postgres em produção**: você não disse onde ele roda. Deixei um nó genérico `PostgreSQL` dentro da AWS, sem marcar como RDS/Aurora. Se for RDS, adicione a tag `"Amazon Web Services - RDS"` no nó para ganhar o ícone.
4. **Sem réplicas**: não coloquei `instances N` nas tasks porque não sei quantas rodam de cada.

## Para ver e exportar

Preview com live-reload em `http://localhost:8080` (o layout manual é salvo em `workspace.json` — não edite esse arquivo à mão):

```
docker run --rm -it -p 8080:8080 -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_AUTOREFRESHINTERVAL=2000 \
    -e STRUCTURIZR_AUTOSAVEINTERVAL=5000 \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr local
```

Exportar (PlantUML, Mermaid, PNG estático etc.) para `diagrams/`:

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr export -workspace workspace.dsl -format plantuml -output diagrams
```

Revalidar depois de editar:

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr validate -workspace workspace.dsl
```
