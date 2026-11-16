# Arquivos de exportação no S3

| | |
|---|---|
| **Estado** | Implementado |
| **Autores** | Time de Relatórios |
| **Revisores** | A definir |
| **Criado em** | 2026-11-16 |
| **Última atualização** | 2026-11-16 |
| **Altera** | [Exportação de relatórios em background](exportacao-de-relatorios.md) |

## Visão geral

O design original gravava o CSV gerado no disco local do worker. O time subiu um segundo worker, e o download passou a cair, às vezes, no worker que não tinha o arquivo e devolvia 404. Os arquivos gerados agora ficam num bucket S3 em vez do disco local do worker. Este documento registra essa mudança e o motivo.

## Contexto

O design original ([Exportação de relatórios em background](exportacao-de-relatorios.md)) previa um único worker. O endpoint `GET /exports/<job_id>/download` lia o arquivo de `/var/exports/<job_id>.csv` no disco do worker que o serviu. Com dois workers, o arquivo existe só no worker que o gerou, e o pedido de download chega a qualquer um dos dois.

## O que mudou

- Antes: o worker gravava o CSV no disco local, em `/var/exports/<job_id>.csv`.
- Agora: o worker grava o CSV num bucket S3.

O restante do design original não foi alterado por este documento. Como o download funciona hoje, a retenção e a limpeza dos arquivos estão em [Questões em aberto](#questões-em-aberto).

## Trade-offs

- ✓ O download deixa de depender de qual worker gerou o arquivo, o que elimina o 404 causado por ter dois workers.
- ✓ O arquivo deixa de ficar preso ao disco de um worker.
- ✗ Os custos que o time aceitou com o bucket ainda não estão registrados (ver Questões em aberto).

## Alternativas consideradas

**Manter o arquivo no disco local do worker.** Descartada: com dois workers, o download devolve 404 quando cai no worker que não gerou o arquivo.

**Gravar os arquivos num bucket de object storage.** Foi a alternativa que o design original descartou por exigir credenciais e política de retenção novas, com um único worker previsto. O segundo worker mudou essa conta, e o time adotou o bucket.

## Questões em aberto

- Desde quando os arquivos vão para o S3 (data do deploy)?
- Quem serve o download hoje: o worker, a API ou uma URL do próprio S3?
- Os 7 dias de retenção e a limpeza continuam valendo? Quem apaga os arquivos antigos agora?
- O que aconteceu com os arquivos que já estavam em `/var/exports` na migração?
- O que essa abordagem piora e o que o time decidiu aceitar (custo, latência, dependência do S3, credenciais)?
- Quem revisou ou deve revisar esta mudança?
