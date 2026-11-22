# Exportação de relatórios em background

| | |
|---|---|
| **Estado** | Implementado |
| **Autores** | Time de Relatórios |
| **Revisores** | Marina Prado (Plataforma) |
| **Criado em** | 2026-01-12 |
| **Última atualização** | 2026-11-22 |

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

A API grava o pedido na tabela `export_jobs` e responde 202 com o id do job. Um worker lê os jobs pendentes, gera o CSV e grava o arquivo num bucket S3. Qualquer worker atende `GET /exports/<job_id>/download`, porque o arquivo não fica mais no disco do worker que o gerou.

TODO: informar o nome do bucket e a chave do objeto (antes: `/var/exports/<job_id>.csv` no disco do worker).

TODO: informar quem entrega o arquivo no download (o worker lê do S3 e devolve, ou devolve uma URL pré-assinada) e como o serviço obtém as credenciais do bucket.

TODO: informar a retenção atual. Com o disco, os arquivos ficavam 7 dias e um cron do worker apagava os mais antigos. Não sei se o bucket mantém os 7 dias nem se uma regra de lifecycle ou o cron faz a limpeza.

### Mudança do disco local para o S3

Na primeira versão, o worker gravava o CSV em `/var/exports/<job_id>.csv` e servia o download a partir do próprio disco. Depois que o time subiu um segundo worker, o download caía às vezes no worker que não tinha o arquivo e devolvia 404. O time moveu o armazenamento dos arquivos para o bucket S3 para que todos os workers enxerguem os mesmos arquivos.

TODO: informar a data da mudança e o link do PR ou do ticket.

## Trade-offs da solução escolhida

- ✓ O download funciona em qualquer worker e não devolve mais 404 por cair no worker errado.
- ✓ A solução não assume um número fixo de workers.
- ✗ Dependência nova: o bucket S3, com credenciais e política de retenção para manter.

## Alternativas consideradas

**Manter os arquivos no disco local do worker.** Foi a solução original. Funcionava com um único worker, que era o previsto. Com o segundo worker, o download devolvia 404 quando caía no worker sem o arquivo, e o time a substituiu pelo bucket S3.

**Gravar os arquivos num bucket de object storage.** Descartada na primeira versão porque exigia credenciais e política de retenção novas, um custo que o time considerou desnecessário com um único worker. Adotada depois, quando o segundo worker tornou o disco local inviável.

**Não fazer nada.** Descartada: as exportações acima de 200 mil linhas falhavam em toda tentativa.

## Questões em aberto

Os `TODO` da seção Solução: bucket e chave, quem entrega o download, retenção e data da mudança.
