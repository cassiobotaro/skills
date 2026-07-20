Criei o `workspace.dsl` na raiz do repositório com o modelo C4 do **Encurtaí** e os três diagramas pedidos.

## O que ficou no modelo

**Pessoa**
- Usuário da empresa — cria links curtos e acessa links curtos.

**Sistema Encurtaí** (tudo do seu time, então um único software system com containers):

| Container | Tecnologia | Papel |
|---|---|---|
| SPA | React (servido por nginx) | Interface onde o usuário cria/consulta links |
| API | Go (Gin) | Cria/consulta links, resolve redirecionamentos, publica eventos de clique |
| Worker de Métricas | Go | Consome eventos de clique e grava métricas agregadas |
| Fila de Eventos de Clique | RabbitMQ | Buffer entre API e worker |
| Cache de Redirecionamentos | Redis 7 | Destino dos links curtos para redirecionar sem ir ao banco |
| Banco de Dados | PostgreSQL 16 | Links curtos + métricas agregadas |

**Sistema externo**
- Google Workspace — provedor de identidade do SSO, usado pela API.

Duas observações de classificação, seguindo o C4:

- O **nginx** não virou um container próprio: ele é o mecanismo de entrega do SPA, então aparece como tecnologia do container SPA. Se um dia ele passar a fazer roteamento/TLS para a API, o lugar dele é um `infrastructureNode` num diagrama de deployment, não no diagrama de containers.
- A **fila** foi modelada como container (a fila em si, tagueada `Queue` e desenhada como pipe); o broker RabbitMQ como infraestrutura também é assunto de deployment.

## Views

- `SystemContext` — Encurtaí, o usuário e o Google Workspace.
- `Containers` — os seis containers, com tecnologias e protocolos nas setas.
- `Redirecionamento` (dynamic) — usuário acessa o link curto → API consulta o cache → em caso de miss busca no Postgres → publica o evento de clique na fila. Cada passo é respaldado por uma relação que existe no modelo.

Todas as views têm chave estável e descritiva (`SystemContext`, `Containers`, `Redirecionamento`) e `autoLayout` — mudar uma chave depois órfã o layout que você arrastar na UI.

## Estilos (viram a legenda automática)

Os tipos são codificados por **tag + style**, nunca por cor solta no elemento:

- `Database` → cilindro (Postgres e Redis)
- `Cache` → cilindro em azul mais claro (Redis)
- `Queue` → pipe roxo (RabbitMQ)
- `External` → cinza (Google Workspace)
- `Person` → boneco, `Browser` → janela de navegador (SPA)

## Validação

O DSL foi validado localmente e passou sem erros:

```
docker run --rm -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    -v "$PWD":/usr/local/structurizr \
    structurizr/structurizr validate -workspace workspace.dsl
```

Não há ADRs no repositório, então não incluí `!adrs`. Quando você começar um log de decisões (ex.: `doc/adr`), basta uma linha `!adrs doc/adr` no workspace para o Structurizr importar o log.

## Para visualizar e exportar

Preview com live-reload em http://localhost:8080 (salva o layout manual em `workspace.json`):

```
docker run --rm -it -p 8080:8080 -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr local
```

Exportar (PlantUML, Mermaid, PNG estático, …) para `diagrams/`:

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr export -workspace workspace.json -format mermaid -output diagrams
```

Abra o preview pelo menos uma vez antes de exportar (o `workspace.json` é onde o layout ajustado à mão fica); ou exporte direto com `-workspace workspace.dsl`.

Se quiser um diagrama de deployment depois (nginx, réplicas do worker, ambiente de produção), me passe como isso roda hoje e eu acrescento — não modelei nada de infra que você não descreveu.
