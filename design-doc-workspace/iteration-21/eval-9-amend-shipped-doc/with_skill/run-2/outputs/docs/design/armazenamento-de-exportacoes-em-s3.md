# Armazenamento dos arquivos exportados em bucket S3

| | |
|---|---|
| **Estado** | Implementado |
| **Autores** | Time de Relatórios |
| **Revisores** | A definir |
| **Criado em** | 2026-11-16 |
| **Última atualização** | 2026-11-16 |
| **Altera** | [Exportação de relatórios em background](exportacao-de-relatorios.md) |

## Visão geral

Este documento altera o design de [Exportação de relatórios em background](exportacao-de-relatorios.md). Os arquivos CSV gerados deixaram de ficar no disco local do worker e passaram a ficar em um bucket S3. O restante do design original continua valendo.

## Contexto e motivo da mudança

O design original gravava o arquivo em `/var/exports/<job_id>.csv` e servia o download pelo próprio worker, e assumia um único worker (ver os trade-offs do documento original). O time subiu um segundo worker. Quando o download caía no worker que não gerou o arquivo, o endpoint `GET /exports/<job_id>/download` devolvia 404.

## O que mudou

| Aspecto | Antes | Agora |
|---|---|---|
| Onde o worker grava o CSV | Disco local, `/var/exports/<job_id>.csv` | Bucket S3 |
| Quem serve o download | O worker que gerou o arquivo | Os arquivos vêm do bucket, então qualquer worker atende |

O restante do design original não muda: a tabela `export_jobs`, a resposta 202 com o id do job e a geração do CSV pelo worker.

## Trade-offs

- ✓ O download funciona qualquer que seja o worker que recebe a requisição, o que elimina o 404.
- ✓ A solução deixa de assumir um único worker, e os arquivos deixam de depender do disco de um worker.
- ✗ O serviço passa a depender de um componente externo (o bucket), que o design original havia evitado.

Os demais custos aceitos estão em Questões em aberto.

## Alternativas consideradas

**Não fazer nada.** Descartada: com dois workers, parte dos downloads continuava devolvendo 404.

As outras alternativas que o time avaliou estão em Questões em aberto.

## Questões em aberto

- Quais outros custos o time aceitou com o bucket (credenciais, política de retenção, custo de storage e de transferência)?
- O período de retenção de 7 dias e a limpeza que o cron do worker fazia continuam valendo, ou o bucket assumiu essa função?
- Que outras alternativas o time considerou para o 404, além de não fazer nada?
- Quem revisou ou deve revisar a mudança?
