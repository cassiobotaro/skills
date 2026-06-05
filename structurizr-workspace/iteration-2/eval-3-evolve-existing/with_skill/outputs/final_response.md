File writes are permission-denied in this environment. As instructed, I will not retry. I'll produce the complete final workspace.dsl in my final response and provide the validation command, since validation could not be run.

Let me compose the complete file carefully, applying minimal diffs to the existing content and adding the three requested pieces. I'll verify the relationship references for the dynamic view all exist in the model:

- `atendente -> faturamento.portal` ✓
- `faturamento.portal -> faturamento.api` ✓
- `faturamento.api -> faturamento.banco` ✓
- `faturamento.api -> faturamento.fila` ✓
- `faturamento.worker -> faturamento.fila` ✓ (consume direction)
- `faturamento.worker -> erp` ✓

For the deployment reroute, only the API sits behind the ALB, so `portal -/> api` is rerouted through the ALB.

---

A escrita de arquivos foi bloqueada por permissão neste ambiente, então **não consegui salvar o arquivo nem rodar a validação**. Abaixo está o `workspace.dsl` completo e final com as três evoluções pedidas. Copie-o sobre o arquivo atual.

O que mudou (diff mínimo, sem alterar nada do que já existia):

1. **Ambiente de produção na AWS** — novo `deploymentEnvironment "Producao"`: Portal e API em ECS Fargate (API com `instances 2`), Worker em ECS Fargate, banco em RDS PostgreSQL e um Application Load Balancer (`infrastructureNode`) na frente da API. O ALB é modelado como conceito de deployment e a chamada `portal -> api` é re-roteada por ele com `-/>`. Adicionei o tema AWS para os ícones e uma `deployment view`.
2. **Diagrama dinâmico "Emissão de fatura"** — `dynamic faturamento "EmissaoFatura"`, com cada passo apoiado em uma relação que já existe no modelo.
3. **ADRs vinculados** — `!adrs docs/adr` no nível do workspace (formato adr-tools, que é o usado nos seus arquivos).

```dsl
workspace "Faturamento" "Sistema de faturamento da empresa." {

    !identifiers hierarchical

    !adrs docs/adr

    model {
        atendente = person "Atendente" "Equipe financeira que emite e acompanha faturas."

        faturamento = softwareSystem "Faturamento" "Emite, processa e concilia faturas." {
            portal = container "Portal Web" "Interface para emissão e acompanhamento de faturas." "React"
            api = container "API de Faturamento" "Regras de negócio e orquestração de faturas." "Go"
            worker = container "Worker de Processamento" "Processa faturas de forma assíncrona." "Go"
            fila = container "Fila de Faturas" "Buffer de faturas a processar." "RabbitMQ" {
                tags "Queue"
            }
            banco = container "Banco de Dados" "Armazena faturas, clientes e itens." "PostgreSQL" {
                tags "Database"
            }
        }

        erp = softwareSystem "ERP" "Sistema corporativo de gestão (mantido por terceiro)." {
            tags "External"
        }

        atendente -> faturamento.portal "Emite e consulta faturas usando"
        faturamento.portal -> faturamento.api "Chama" "JSON/HTTPS"
        faturamento.api -> faturamento.banco "Lê e grava dados em" "SQL/TCP"
        faturamento.api -> faturamento.fila "Publica faturas emitidas em"
        faturamento.worker -> faturamento.fila "Consome faturas de"
        faturamento.worker -> faturamento.banco "Atualiza status em" "SQL/TCP"
        faturamento.worker -> erp "Envia faturas processadas para" "HTTPS"

        producao = deploymentEnvironment "Producao" {
            aws = deploymentNode "Amazon Web Services" {
                tags "Amazon Web Services - Cloud"
                region = deploymentNode "us-east-1" {
                    tags "Amazon Web Services - Region"

                    alb = infrastructureNode "Load Balancer" "Distribui requisições para a API." "Application Load Balancer" {
                        tags "Amazon Web Services - Elastic Load Balancing"
                    }

                    ecs = deploymentNode "Amazon ECS" "" "AWS Fargate" {
                        tags "Amazon Web Services - Elastic Container Service"

                        portalTask = deploymentNode "Portal Task" "" "Docker Container" {
                            instanceOf faturamento.portal
                        }
                        apiTask = deploymentNode "API Task" "" "Docker Container" {
                            instances 2
                            instanceOf faturamento.api
                        }
                        workerTask = deploymentNode "Worker Task" "" "Docker Container" {
                            instanceOf faturamento.worker
                        }
                    }

                    rds = deploymentNode "Amazon RDS" {
                        tags "Amazon Web Services - RDS"
                        postgres = deploymentNode "PostgreSQL" "" "RDS PostgreSQL" {
                            instanceOf faturamento.banco
                        }
                    }
                }
            }

            faturamento.portal -/> faturamento.api {
                faturamento.portal -> aws.region.alb "Chama" "JSON/HTTPS"
                aws.region.alb -> faturamento.api "Encaminha requisições para" "JSON/HTTPS"
            }
        }
    }

    views {
        systemContext faturamento "Contexto" {
            include *
            autoLayout
        }

        container faturamento "Containers" {
            include *
            autoLayout
        }

        dynamic faturamento "EmissaoFatura" "Fluxo de emissão de uma fatura." {
            atendente -> faturamento.portal "Emite a fatura pelo"
            faturamento.portal -> faturamento.api "Envia a solicitação de emissão para"
            faturamento.api -> faturamento.banco "Grava a fatura em"
            faturamento.api -> faturamento.fila "Publica a fatura emitida em"
            faturamento.worker -> faturamento.fila "Consome a fatura de"
            faturamento.worker -> erp "Envia a fatura processada para"
            autoLayout lr
        }

        deployment faturamento producao "Deployment-Producao" {
            include *
            autoLayout lr
        }

        styles {
            element "Person" {
                shape person
            }
            element "Database" {
                shape cylinder
            }
            element "Queue" {
                shape pipe
            }
            element "External" {
                background #999999
                color #ffffff
            }
        }

        theme https://static.structurizr.com/themes/amazon-web-services-2020.04.30/theme.json
    }
}
```

Observações e decisões que tomei:

- **ALB só na frente da API**: você disse "Application Load Balancer na frente da API", então re-roteei apenas a chamada `portal -> api` pelo ALB. O Portal, o Worker e a API rodam todos em tasks do ECS Fargate; o RDS recebe as conexões da API e do worker normalmente (essas relações já existiam no modelo e são propagadas para o deployment automaticamente).
- **`scope`**: o arquivo original não tinha um bloco `configuration { scope softwaresystem }`. Mantive como estava para não alterar mais que o necessário — o Structurizr infere o escopo de sistema único corretamente.
- **Tema AWS** adicionado para renderizar os ícones de Cloud/Region/ECS/RDS/ELB no diagrama de deployment.

**Validação não pôde ser executada** (escrita de arquivos bloqueada). Depois de salvar o arquivo, valide com a sua ferramenta:

- Via MCP: `c4_mcp` (ferramenta de validação de DSL), ou
- Via Docker:
  `docker run --rm -v "$PWD":/usr/local/structurizr structurizr/structurizr validate -workspace workspace.dsl`

Para visualizar: `c4_local` (UI em `http://localhost:8080`, recarrega ao salvar o `.dsl`). Recomendo conferir especialmente o diagrama de deployment e o dinâmico de "Emissão de fatura" após a validação.

Pergunta em aberto (não bloqueou nada, segui o que estava justificado): o ALB também serve o Portal Web em produção, ou o Portal é acessado por outro caminho (ex.: CloudFront/S3)? Modelei apenas a API atrás do ALB, conforme o texto.