# Armazenamento dos arquivos exportados em bucket S3

| | |
|---|---|
| **Estado** | Implementado |
| **Autores** | Time de Relatórios |
| **Altera** | [Exportação de relatórios em background](exportacao-de-relatorios.md) |
| **Criado em** | 2026-11-16 |
| **Última atualização** | 2026-11-16 |

## Visão geral

Os arquivos gerados pela exportação de relatórios deixaram o disco local do worker e passaram a ficar em um bucket S3. A mudança corrige o 404 no download que apareceu quando o serviço ganhou um segundo worker. Este documento registra a mudança e o motivo. O restante do design original continua valendo.

## Contexto

O [design original](exportacao-de-relatorios.md) grava o CSV no disco do worker que o gerou, em `/var/exports/<job_id>.csv`, e serve o download pelo mesmo worker. Ele assume um único worker e registra isso como custo (✗ "O arquivo só existe no worker que o gerou").

O serviço está em produção desde março. O time subiu um segundo worker, e a requisição de download passou a cair, às vezes, no worker que não tinha o arquivo. Esse worker devolvia 404.

## O que mudou

| | Antes | Agora |
|---|---|---|
| Onde o arquivo fica | Disco local do worker, `/var/exports/<job_id>.csv` | Bucket S3 |

Os pedidos, a tabela `export_jobs` e a geração do CSV pelo worker não fazem parte desta mudança. Como o download é servido e como a retenção de 7 dias funciona agora estão em [Questões em aberto](#questões-em-aberto).

## Trade-offs

- ✓ O arquivo não depende mais do worker que o gerou, que era a causa do 404 com dois workers.
- ✗ O bucket é uma dependência nova. O design original listava como vantagem "nenhuma dependência nova" e descartou o bucket por exigir credenciais e política de retenção novas.

O time ainda não registrou os demais custos aceitos (ver Questões em aberto).

## Alternativas consideradas

**Manter o arquivo no disco do worker.** É o design original. Descartada: com dois workers, o download falha com 404 quando cai no worker errado.

**Gravar em bucket de object storage.** Era a alternativa que o design original descartou, na época por considerar o custo desnecessário para um único worker. É a escolhida agora.

## Questões em aberto

- Em que data a mudança foi para produção?
- Quem serve o download agora (o worker, a API ou um link direto do bucket) e o endpoint `GET /exports/<job_id>/download` mudou?
- A retenção de 7 dias continua? Se sim, como o bucket a aplica (o cron do worker ou uma regra do bucket)?
- O que fazer com os arquivos que ainda estão no disco dos workers? Houve migração ou eles expiram?
- Quais custos o time aceitou (dinheiro, latência, credenciais, acesso aos arquivos)?
- Alguma outra alternativa foi considerada além de manter o disco local (por exemplo, roteamento do download ao worker certo)?
