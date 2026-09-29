Criei o `workspace.dsl` na raiz do repositório com o modelo C4 do Encurtaí e validei o arquivo com a imagem Docker `structurizr/structurizr` (sem erros).

## O que foi modelado

**Pessoa**
- Usuário da empresa

**Sistema Encurtaí** (tudo do seu time, portanto um único software system com seis containers):
- Aplicação Web — React (SPA servido por nginx)
- API — Go (Gin)
- Banco de dados — PostgreSQL 16 (tag `Database`, cilindro)
- Cache de redirecionamentos — Redis 7 (tag `Cache`, cilindro em tom mais claro para diferenciar do banco)
- Fila de eventos de clique — RabbitMQ (tag `Queue`, forma de tubo)
- Worker de métricas — Go

**Sistema externo**
- Google Workspace (tag `External`, cinza) — autenticação SSO usada pela API

**Relações** (todas com rótulo direcional e protocolo): usuário → SPA e usuário → API; SPA → API; API → PostgreSQL, Redis, RabbitMQ e Google Workspace; RabbitMQ → Worker; Worker → PostgreSQL.

## Views

| Chave | Tipo | Conteúdo |
|---|---|---|
| `SystemContext` | Contexto | Usuário, Encurtaí, Google Workspace |
| `Containers` | Containers | Os seis containers + usuário + Google Workspace |
| `Redirecionamento` | Dinâmica | 1. usuário acessa o link curto → 2. API consulta o cache → 3. em caso de miss, API consulta o Postgres → 4. API publica o evento de clique na fila → 5. API responde com o redirecionamento |

Os estilos ficam em `styles` por tag (`Database`, `Cache`, `Queue`, `External`, `Person`, `WebBrowser`), então a legenda do diagrama explica cada forma/cor.

## Pontos que registrei sem confirmação sua — ajuste se estiverem errados

1. **Protocolos nas relações**: usei `HTTPS` para usuário → SPA/API e API → Google Workspace, `REST/JSON sobre HTTPS` para SPA → API, `SQL/TCP` para o Postgres, `Redis/TCP` para o Redis e `AMQP` para o RabbitMQ. Você descreveu a stack, mas não os protocolos; se algo for HTTP simples ou outro protocolo, é só editar o terceiro argumento da relação.
2. **Passo de preenchimento do cache**: o fluxo que você descreveu não menciona a API gravar o destino no Redis após o miss, então não incluí esse passo na view dinâmica (a relação API → Redis existe no modelo com o rótulo "Consulta e armazena"). Se esse passo acontece, basta adicionar uma linha `encurtai.api -> encurtai.cache "Armazena o destino no cache"` entre os passos 3 e 4.
3. **Código HTTP do redirecionamento** (301/302) não foi informado, então o passo final diz apenas "Responde com o redirecionamento para a URL de destino".
4. O **nginx** ficou registrado na tecnologia da Aplicação Web, não como container próprio: em C4 ele é um detalhe de execução/deploy, que caberia num diagrama de deployment se você quiser um depois.

## Como visualizar e exportar

Preview com live-reload em `http://localhost:8080` (arrastar elementos salva o layout em `workspace.json`, que não deve ser editado à mão):

```
docker run --rm -it -p 8080:8080 -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_AUTOREFRESHINTERVAL=2000 \
    -e STRUCTURIZR_AUTOSAVEINTERVAL=5000 \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr local
```

Exportar para `diagrams/` (formatos: `plantuml`, `mermaid`, `json`, `dot`, `ilograph`, `d2`, `static`):

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr export -workspace workspace.dsl -format <formato> -output diagrams
```

Para revalidar depois de editar:

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr validate -workspace workspace.dsl
```

---

**Arquivos escritos**
- `workspace.dsl` (raiz do repositório)

**Arquivos de referência do skill lidos**
- `SKILL.md`
- `references/dsl-reference.md` (sempre, sintaxe base + template §15)
- `references/modeling-patterns.md` (§2, fila/mensageria assíncrona)

**Validador executado**
- `docker run --rm -u $(id -u):$(id -g) -v "$PWD":/usr/local/structurizr -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes structurizr/structurizr validate -workspace workspace.dsl`, executado na raiz do repositório.
- Resultado exato: exit code 0, nenhuma saída (sem erros nem avisos). Um arquivo propositalmente quebrado, validado com o mesmo comando como controle, retornou exit code 1 com `ERROR ... The destination element "missing" does not exist`, confirmando que o validador estava ativo.
- Verificação adicional: `structurizr/structurizr export -format json` a partir do DSL (em diretório temporário) confirmou as três views (`SystemContext`, `Containers`, `Redirecionamento`) e os 5 passos da view dinâmica, com o passo final reconhecido como resposta.
