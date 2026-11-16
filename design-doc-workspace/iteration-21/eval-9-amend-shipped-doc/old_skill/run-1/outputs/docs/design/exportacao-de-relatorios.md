# Exportação de relatórios em background

| | |
|---|---|
| **Estado** | Implementado |
| **Autores** | Time de Relatórios |
| **Revisores** | Marina Prado (Plataforma) |
| **Criado em** | 2026-01-12 |
| **Última atualização** | 2026-11-16 |

## Visão geral

Relatórios grandes eram gerados dentro da request da API e estouravam o timeout de 30s do gateway. Este documento descreve o serviço que gera esses relatórios fora da request: a API enfileira o pedido, um worker gera o arquivo e o usuário baixa quando fica pronto.

## Objetivos e fora de escopo

Objetivos:

- Nenhuma exportação falha por timeout do gateway.
- O usuário recebe o link de download em até 5 minutos para relatórios de até 1 milhão de linhas.

Fora de escopo:

- Agendamento recorrente de relatórios.
- Formatos além de CSV.

## Solução

A API grava o pedido na tabela `export_jobs` e responde 202 com o id do job. Um worker lê os jobs pendentes, gera o CSV e grava o arquivo num bucket S3.

Os arquivos ficam num bucket S3 desde a atualização de 2026-11-16. Até então o worker gravava o CSV no disco local, em `/var/exports/<job_id>.csv`, e o endpoint `GET /exports/<job_id>/download` era servido pelo próprio worker. Com a entrada de um segundo worker, o download caía no worker que não tinha o arquivo e devolvia 404. Com o bucket, qualquer worker acessa o arquivo.

Retenção, nome do bucket e o caminho do download após a mudança: ver Questões em aberto.

## Trade-offs da solução escolhida

- ✓ Qualquer worker serve o download, então o time pode rodar mais de um worker sem 404.
- ✓ Os arquivos não dependem mais do disco de um worker.
- ✗ Dependência nova de um bucket S3 (credenciais e acesso para os workers).

Versão original (2026-03-03, disco local): a solução tinha como vantagem não ter dependência nova e como custo assumir um único worker e perder os arquivos se o disco se perdesse. A premissa do worker único não se sustentou em produção.

## Alternativas consideradas

**Gravar os arquivos num bucket de object storage.** Tiraria a dependência do disco do worker, mas exigia credenciais e política de retenção novas. Com um único worker previsto, o time considerou o custo desnecessário. **Adotada em 2026-11-16**, depois que o segundo worker tornou o disco local inviável.

**Manter o disco local.** Era a solução original. Foi abandonada porque, com dois workers, o download caía no worker sem o arquivo e devolvia 404.

**Não fazer nada.** Descartada: as exportações acima de 200 mil linhas falhavam em toda tentativa.

## Questões em aberto

- Por quanto tempo os arquivos ficam no bucket? Os 7 dias e o cron do worker continuam valendo, ou a retenção passou para uma regra do bucket?
- Quem serve o download agora: o worker lendo do bucket, ou a API devolvendo um link direto para o bucket?
- Quais os custos aceitos além da dependência nova (por exemplo, custo de storage e transferência)?
