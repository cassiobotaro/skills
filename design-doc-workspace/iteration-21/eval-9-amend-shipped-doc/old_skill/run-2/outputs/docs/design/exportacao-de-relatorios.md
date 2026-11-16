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

A API grava o pedido na tabela `export_jobs` e responde 202 com o id do job. Um worker lê os jobs pendentes, gera o CSV e grava o arquivo num bucket S3. O endpoint `GET /exports/<job_id>/download` lê o arquivo do bucket, então qualquer worker atende o download.

Os arquivos ficam 7 dias; um cron apaga os mais antigos. (A retenção no bucket está em Questões em aberto.)

### Mudança posterior: do disco local para o S3

A versão original gravava o arquivo no disco local do worker, em `/var/exports/<job_id>.csv`, e o próprio worker servia o download. Depois que o time subiu um segundo worker, o download caía às vezes no worker que não tinha o arquivo e devolvia 404. Gravar no S3 tira a dependência do disco de um worker específico.

## Trade-offs da solução escolhida

- ✓ Qualquer worker serve o download, então o 404 por worker errado deixa de acontecer e o serviço escala para mais de um worker.
- ✓ Os arquivos não dependem mais do disco de um worker.
- ✗ O serviço passa a depender do S3 (dependência nova, que a versão original evitava).
- ✗ O desenho original dispensava credenciais e política de retenção novas; agora o serviço precisa de ambas.

## Alternativas consideradas

**Gravar os arquivos num bucket de object storage.** Descartada no desenho original: exigia credenciais e política de retenção novas, e com um único worker previsto o time considerou o custo desnecessário. Adotada depois, quando o segundo worker tornou o disco local inviável.

**Manter o disco local do worker.** Era a solução original. Deixou de funcionar com dois workers, porque o arquivo só existe no worker que o gerou.

**Não fazer nada.** Descartada: as exportações acima de 200 mil linhas falhavam em toda tentativa.

## Questões em aberto

- O cron de 7 dias passa a apagar objetos do bucket, ou a retenção vira uma regra de lifecycle do S3?
- O download continua passando pela API ou o usuário recebe um link direto para o bucket?
