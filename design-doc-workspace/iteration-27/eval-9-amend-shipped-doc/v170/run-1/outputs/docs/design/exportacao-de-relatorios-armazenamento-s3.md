# Exportação de relatórios: arquivos gerados passam para o S3

| | |
|---|---|
| **Estado** | Implementado |
| **Emenda de** | [Exportação de relatórios em background](exportacao-de-relatorios.md) |
| **Criado em** | 2026-11-22 |
| **Última atualização** | 2026-11-22 |

## Visão geral

O design original gravava o CSV gerado no disco local do worker, em `/var/exports/<job_id>.csv`, e o worker que gerou o arquivo também servia o `GET /exports/<job_id>/download`. Os arquivos gerados agora ficam num bucket S3. Este documento registra a mudança e o motivo. As demais partes do design original continuam valendo.

## Por que mudou

O design original assumia um único worker, e o próprio documento listava isso como trade-off. Quando o time subiu um segundo worker, o download passou a cair, em parte das requisições, no worker que não gerou o arquivo. Esse worker não tinha o arquivo no disco e devolvia 404, mesmo com a exportação concluída.

## O que mudou

| | Design original | Agora |
|---|---|---|
| Onde o arquivo é gravado | Disco local do worker que gerou | Bucket S3 |
| Quem tem acesso ao arquivo | Só o worker que o gerou | Qualquer worker, pelo bucket |

## Trade-offs

- ✓ O download não depende mais de qual worker gerou o arquivo, o que elimina o 404 com mais de um worker.
- ✓ A perda do disco de um worker deixa de apagar os arquivos dos últimos 7 dias, que era um dos trade-offs do design original.
- ✗ O serviço passa a depender do S3. O design original listava como custo desse caminho a necessidade de credenciais e de uma política de retenção novas.

## Questões em aberto

- Como o `GET /exports/<job_id>/download` entrega o arquivo agora: o worker lê do S3 e devolve, ou redireciona para uma URL do bucket?
- A retenção de 7 dias continua? Se sim, o que a aplica agora: o cron do worker ou uma regra de ciclo de vida do bucket?
- O que aconteceu com os arquivos que já estavam no disco do worker quando a mudança entrou?
- Quem são os autores e revisores desta emenda?
