# Armazenamento dos arquivos exportados em bucket S3

| | |
|---|---|
| **Estado** | Implementado |
| **Autores** | Time de Relatórios |
| **Criado em** | 2026-11-16 |
| **Última atualização** | 2026-11-16 |
| **Altera** | [Exportação de relatórios em background](exportacao-de-relatorios.md) |

## Visão geral

Os arquivos de exportação deixaram de ficar no disco local do worker e passaram a ficar num bucket S3. Este documento registra a mudança no desenho original e o motivo dela. O restante do desenho de [Exportação de relatórios em background](exportacao-de-relatorios.md) continua valendo.

## Contexto

O desenho original gravava o CSV em `/var/exports/<job_id>.csv` no disco do worker, e o próprio worker servia `GET /exports/<job_id>/download`. O documento original assumia um único worker e listava isso como custo aceito.

O time subiu um segundo worker. Quando o download caía no worker que não gerou o arquivo, o arquivo não existia ali e o endpoint devolvia 404.

## Solução

O worker grava o arquivo gerado num bucket S3, em vez de no disco local. Com isso, qualquer worker acessa o arquivo, e o download deixa de depender de qual worker gerou o relatório.

## Trade-offs

- ✓ O download funciona em qualquer worker, então o 404 causado pelo segundo worker desaparece.
- ✓ Os arquivos não se perdem junto com o disco de um worker, o segundo custo aceito no documento original.
- ✗ O serviço passa a depender de um object storage, de credenciais e de uma política de retenção, custos que o documento original citou ao descartar o bucket.

## Alternativas consideradas

**Manter o disco local.** Com dois workers, o download falha sempre que cai no worker errado. Foi o motivo da mudança.

## Questões em aberto

- O que mais ficou pior com o bucket (latência de download, custo de armazenamento e transferência, permissões)?
- A retenção de 7 dias continua? Quem a aplica agora, o cron do worker ou uma regra de lifecycle do bucket?
- O download continua passando pelo worker ou o cliente recebe uma URL do bucket?
- Os arquivos antigos do disco foram migrados ou descartados?
- Alguma alternativa além do bucket foi considerada (por exemplo, disco compartilhado ou roteamento do download ao worker de origem)?
