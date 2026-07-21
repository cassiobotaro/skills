Evoluí o `workspace.dsl` com as três coisas pedidas, sem tocar em nada do modelo que já existia (pessoas, containers, relacionamentos, views de contexto/containers, styles e chaves de view continuam idênticos).

## 1. Ambiente de produção na AWS

Novo `deploymentEnvironment "Produção"` no final do `model`:

- `Amazon Web Services` → `Região AWS`
- `Amazon ECS` (AWS Fargate) com três tasks: **Portal** (1 instância), **API** (`instances 2`) e **Worker** (1 instância)
- `Amazon RDS` → `PostgreSQL` hospedando o Banco de Dados
- `Application Load Balancer` como `infrastructureNode` (load balancer é conceito de deployment — por isso ele aparece só na view de deployment, nunca na view de containers)
- O ALB foi colocado "na frente da API" reencaminhando a chamada do Portal:

  ```
  faturamento.portal -/> faturamento.api {
      faturamento.portal -> aws.region.alb "Chama" "JSON/HTTPS"
      aws.region.alb -> faturamento.api "Encaminha requisições para" "JSON/HTTPS"
  }
  ```

  O `-/>` remove a seta direta Portal→API *só dentro do ambiente de produção*; no modelo lógico ela continua como estava.

Nova view: `deployment faturamento producao "Deployment-Producao"`, mais o tema `amazon-web-services-2025.07` (ícones AWS) e as tags de tema nos nós.

**Ponto em aberto:** você não disse onde a fila RabbitMQ roda em produção (Amazon MQ? um broker em ECS? RabbitMQ gerenciado por outro time?). Como a regra aqui é não inventar infraestrutura, deixei a fila **fora** da view de deployment. Me diga onde ela roda que eu acrescento o nó — é uma linha.

## 2. Diagrama dinâmico "emissão de fatura"

Nova view `dynamic faturamento "Emissao-Fatura"`, com os passos na ordem que você descreveu:

1. Atendente → Portal Web
2. Portal Web → API (JSON/HTTPS)
3. API → Banco de Dados (grava a fatura)
4. API → Fila de Faturas (publica)
5. Worker → Fila de Faturas (consome)
6. Worker → ERP (HTTPS)

Todos os passos usam relacionamentos que já existiam no modelo — nenhum relacionamento novo foi criado. O passo 5 está escrito na direção Worker→Fila porque é assim que o relacionamento existe no modelo ("Consome faturas de"); a leitura do fluxo continua correta.

## 3. ADRs

Seus ADRs estão no formato adr-tools (`0001-…md`, `Date:`, `## Status/Context/Decision/Consequences`), então bastou uma linha no escopo do workspace:

```
!adrs docs/adr
```

Os três ADRs passam a aparecer na aba de decisões do Structurizr, na ordem numérica.

## Validação

`docker run --rm -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes -v "$PWD":/usr/local/structurizr structurizr/structurizr validate -workspace workspace.dsl` → **exit 0, sem erros**.

(O MCP do Structurizr conectado também validou o modelo, mas nele o recurso `!adrs` está desabilitado — por isso a validação final foi feita pelo CLI, que enxerga o diretório `docs/adr`.)

## Ver o resultado

```
docker run --rm -it -p 8080:8080 -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr local
```

E, se quiser exportar as imagens:

```
docker run --rm -u $(id -u):$(id -g) \
    -v "$PWD":/usr/local/structurizr \
    -e STRUCTURIZR_THEMES=/usr/local/structurizr-themes \
    structurizr/structurizr export -workspace workspace.dsl -format plantuml -output diagrams
```

## Sugestão opcional (não apliquei, para manter o diff mínimo)

O workspace não tem bloco `configuration { scope softwaresystem }`. Como ele descreve um único sistema, essa linha deixaria o escopo explícito. Quer que eu adicione?
