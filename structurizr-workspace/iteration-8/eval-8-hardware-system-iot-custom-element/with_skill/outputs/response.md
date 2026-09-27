Criei o `workspace.dsl` na raiz do repositório com o modelo da FabricaViva e as duas visões pedidas (contexto e containers). O arquivo passou limpo na validação do Structurizr (`structurizr/structurizr validate`, via Docker).

## Como classifiquei

| O que você descreveu | No modelo | Por quê |
|---|---|---|
| Operadores | `person "Operador"` | Pessoas que usam a plataforma pelo painel |
| FabricaViva | `softwareSystem` (o sistema em foco) | É a plataforma que o time constrói e opera |
| Painel (Vue), Serviço de Ingestão (Go), Serviço de Comandos (Go), TimescaleDB | quatro `container` dentro da FabricaViva | Cada um roda (ou armazena dados) separadamente; TimescaleDB com tag `Database` (cilindro) |
| Câmeras Basler, braços KUKA | elemento customizado `hardwareSystem` (arquétipo `element`, metadata "Sistema de Hardware", tag `Hardware`) | Não são software systems (ninguém do time implanta código neles, o firmware é fechado) nem pessoas; o C4 não tem caixa própria para hardware, então uso um tipo customizado estilizado como robô, em cinza |

Relacionamentos gravados (só os que você estabeleceu):

- `Operador -> Painel` "Acompanha o chão de fábrica usando" (HTTPS)
- `Câmeras Industriais -> Serviço de Ingestão` "Envia frames de vídeo para" (RTSP)
- `Serviço de Comandos -> Braços Robóticos` "Envia comandos para" (OPC UA)

Único palpite meu: o **HTTPS** entre operador e painel (é um painel web). Se for HTTP interno, troque o rótulo.

## O que ficou em aberto (não inventei)

A ligação interna entre os containers não foi descrita, então a visão de containers hoje mostra o Painel e o TimescaleDB sem arestas internas. Para fechar o diagrama preciso de:

1. **Quem escreve no TimescaleDB?** O Serviço de Ingestão (telemetria extraída dos frames), o Serviço de Comandos (registro dos comandos enviados), os dois?
2. **De onde o Painel lê?** Direto do TimescaleDB, de uma API do Serviço de Ingestão, ou de outro lugar? E por qual protocolo (REST/JSON sobre HTTPS, WebSocket, SQL)?
3. **O operador dispara comandos aos robôs pelo Painel?** Se sim, o Painel fala com o Serviço de Comandos (por qual protocolo?) ou existe outro caminho?
4. **Ingestão e Comandos se falam?** Por exemplo, a ingestão detecta algo nos frames e aciona um comando, ou os dois são independentes?

Com as respostas eu adiciono as relações (só mais linhas `->` no `model`, sem mexer nos identificadores nem nas chaves das views, para não perder layout salvo).

## Para ver e exportar

Preview com live reload em `http://localhost:8080` (o layout que você arrastar é salvo em `workspace.json`, que não deve ser editado à mão):

```
docker run --rm -it -p 8080:8080 -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_AUTOREFRESHINTERVAL=2000 \
    -e STRUCTURIZR_AUTOSAVEINTERVAL=5000 \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr local
```

Exportar (por exemplo para PlantUML ou Mermaid) para a pasta `diagrams/`:

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr export -workspace workspace.dsl -format plantuml -output diagrams
```

Não encontrei ADRs no repositório, então não incluí `!adrs`; se o time tiver um log de decisões, me diga o caminho e eu ligo ele ao workspace.
