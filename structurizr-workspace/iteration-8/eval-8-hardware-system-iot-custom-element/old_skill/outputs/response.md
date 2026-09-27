Criei o `workspace.dsl` na raiz do repositório com o modelo C4 da FabricaViva e as duas views pedidas (contexto e containers). O arquivo passou limpo na validação (`structurizr/structurizr validate`, via Docker).

## Como classifiquei

| Elemento | Nível C4 | Por quê |
|---|---|---|
| Operador | Pessoa | Humano que usa o painel |
| FabricaViva | Sistema de software (o seu) | Vocês constroem e enxergam por dentro |
| Painel (Vue), Serviço de Ingestão (Go), Serviço de Comandos (Go), Banco de Telemetria (TimescaleDB) | Containers da FabricaViva | Cada um roda como processo próprio ou armazena dados |
| Câmeras Industriais (Basler) e Braços Robóticos (KUKA) | Sistemas externos, tags `External` + `Hardware` | Hardware de terceiros com firmware fechado: caixa fechada que vocês não abrem, exatamente o que o C4 chama de sistema externo. A tag `Hardware` dá a eles um hexágono cinza no diagrama para se distinguirem de um SaaS |

Relações registradas (só as que você descreveu):

- Operador → Painel: "Acompanha o chão de fábrica usando" (HTTPS)
- Câmeras → Serviço de Ingestão: "Envia frames de vídeo para" (RTSP)
- Serviço de Comandos → Braços Robóticos: "Envia comandos para" (OPC UA)

## O que ficou em aberto (não inventei)

Duas lacunas aparecem no diagrama de containers e deixei um `// TODO` no DSL apontando para elas. Preciso de você para fechar:

1. **Banco de Telemetria**: quem grava nele e quem lê? (Ex.: o Serviço de Ingestão grava telemetria extraída dos frames e o Painel lê.) Hoje ele está sem nenhuma seta.
2. **Painel ↔ serviços**: como o painel chega aos dados e aos comandos? Ele chama a Ingestão e/ou o Serviço de Comandos (HTTP? WebSocket?), ou lê direto do banco? E o operador dispara comandos aos robôs pelo painel, ou os comandos nascem em outro lugar?
3. **Câmeras e robôs**: modelei como sistemas externos. Se preferir tratá-los como dispositivos físicos fora do C4 (custom `element` com metadata "Hardware"), consigo trocar, mas eles deixam de aparecer no contexto como sistemas com os quais a plataforma se integra.

Me responda essas e eu completo as setas (e re-valido).

## Para ver e exportar

Preview com live-reload em `http://localhost:8080` (o layout manual é salvo em `workspace.json`; não edite esse arquivo à mão):

```
docker run --rm -it -p 8080:8080 -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_AUTOREFRESHINTERVAL=2000 \
    -e STRUCTURIZR_AUTOSAVEINTERVAL=5000 \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr local
```

Exportar (por exemplo PlantUML ou Mermaid) para `diagrams/`:

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr export -workspace workspace.dsl -format plantuml -output diagrams
```

Re-validar depois de editar:

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr validate -workspace workspace.dsl
```
