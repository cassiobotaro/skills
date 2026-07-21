Criei o `workspace.dsl` na raiz do repositório com o **system landscape** da fintech.

## O que ficou no modelo

**Pessoas:** Cliente, Analista de Crédito, Time de Cobrança.

**Sistemas internos** (agrupados em `group "Fintech"`): Portal do Cliente, Motor de Crédito, Cobrança, Data Lake.

**Sistema externo:** Core Bancário — produto terceirizado da Matera, marcado com a tag `External` (cinza no estilo), porque não é desenvolvido nem mantido por vocês.

**Relacionamentos:** Cliente → Portal; Analista → Motor de Crédito (backoffice); Time de Cobrança → Cobrança; Motor de Crédito → Core Bancário (contratos a partir de propostas aprovadas); Cobrança → Core Bancário (leitura de contratos); Portal, Motor e Cobrança → Data Lake (eventos).

Decisões de modelagem que vale registrar:

- É um workspace **landscape** (`configuration { scope landscape }`) com uma única view `systemLandscape`. Por definição um landscape não tem containers, então "web e app" do Portal e o "backoffice" do Motor de Crédito aparecem só na descrição dos sistemas — eles viram containers quando/se vocês criarem o workspace específico de cada sistema.
- O Data Lake é um sistema interno (time de dados), não um sistema externo — só o Core Bancário está marcado como externo.

## Pontos em aberto (não inventei nada aqui)

1. **Portal do Cliente → Motor de Crédito**: você disse que clientes usam o Portal e que o Motor avalia as propostas, mas não disse quem envia a proposta pro Motor. Hoje o Portal está ligado só ao Data Lake. A proposta sai do Portal direto pro Motor? Passa por outro sistema?
2. **Portal × Core Bancário**: o cliente consegue ver saldo/parcelas dos contratos no Portal? Se sim, falta a leitura Portal → Core (ou Portal → algum sistema que agrega isso).
3. **Cobrança → Cliente**: existe contato ativo com o cliente (e-mail, SMS, WhatsApp) modelado como relação? Não incluí.
4. **Tecnologias/protocolos das integrações**: o inspetor do Structurizr sinaliza que os relacionamentos não têm tecnologia (ex.: "REST/HTTPS", "Kafka", "batch"). Não preenchi para não inventar — me diga como cada integração acontece (principalmente Motor → Core, Cobrança → Core e os eventos pro Data Lake) e eu completo. Num diagrama de landscape esse detalhe é opcional, mas ajuda.
5. **Ownership**: o Motor de Crédito e o backoffice são do mesmo time? Se o backoffice for de outro time/produto, ele vira um sistema separado no landscape.

## Validação

O DSL foi validado com sucesso pelo servidor MCP do Structurizr (`validate` → OK). O `inspect` só retornou os avisos de tecnologia ausente nos relacionamentos, citados no ponto 4.

## Como visualizar e exportar

Preview (live-reload, salva layout manual em `workspace.json`):

```
docker run --rm -it -p 8080:8080 -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr local
```

Depois acesse http://localhost:8080.

Exportar (por exemplo para PlantUML ou Mermaid):

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr export -workspace workspace.json -format plantuml -output diagrams
```

Como o export lê o `workspace.json` (onde fica o layout salvo), abra o preview pelo menos uma vez antes — ou exporte direto do DSL com `-workspace workspace.dsl`.
