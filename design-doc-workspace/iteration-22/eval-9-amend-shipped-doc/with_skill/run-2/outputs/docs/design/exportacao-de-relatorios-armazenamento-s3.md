# Armazenamento dos arquivos exportados em bucket S3

| | |
|---|---|
| **Estado** | Implementado |
| **Autores** | Time de Relatórios |
| **Revisores** | A definir |
| **Criado em** | 2026-11-16 |
| **Última atualização** | 2026-11-16 |
| **Altera** | [Exportação de relatórios em background](exportacao-de-relatorios.md) |

## Glossário

- **S3**: serviço de object storage da AWS; guarda os arquivos num bucket, fora do disco de qualquer worker.

## Visão geral

O serviço de exportação de relatórios passou a guardar os arquivos gerados num bucket S3, em vez do disco local do worker. Este documento altera a seção "Solução" do [design doc original](exportacao-de-relatorios.md), que continua como registro do desenho de março.

## Contexto

O design original gravava o CSV em `/var/exports/<job_id>.csv` no disco do worker que o gerou, e o `GET /exports/<job_id>/download` era servido por esse mesmo worker. O documento assumia um único worker, e registrava isso como custo da solução. O serviço está em produção desde março.

O time subiu um segundo worker. Quando o download caía no worker que não tinha o arquivo, o endpoint devolvia 404.

## Mudança

Os arquivos gerados ficam num bucket S3, não mais no disco local do worker. O worker que gera o arquivo grava no bucket, o que tira a dependência de qual worker atende o download.

## Trade-offs

- ✓ O download deixa de depender do worker que gerou o arquivo, que era a causa do 404 com dois workers.
- ✗ Os custos: veja as questões em aberto. O design original apontava credenciais e política de retenção novas como o preço de usar um bucket.

## Alternativas consideradas

**Não fazer nada.** Descartada: com dois workers, parte dos downloads devolvia 404.

Outras alternativas que o time avaliou: veja as questões em aberto.

## Questões em aberto

- Quando a mudança entrou em produção?
- Quem serve o download agora (a API, um worker, ou o link direto do bucket) e como o acesso ao arquivo é controlado?
- Como ficam a retenção de 7 dias e o cron que apagava os arquivos antigos do disco?
- Quais custos o time aceitou com a mudança (credenciais, política de retenção, custo de storage e transferência, latência)?
- Os arquivos que estavam nos discos locais na hora da mudança foram migrados ou descartados?
- O time avaliou outras saídas além do bucket (por exemplo, disco compartilhado entre workers ou roteamento do download para o worker de origem)? Por que perderam?
- Quem deve revisar este documento (Plataforma, Segurança)?
