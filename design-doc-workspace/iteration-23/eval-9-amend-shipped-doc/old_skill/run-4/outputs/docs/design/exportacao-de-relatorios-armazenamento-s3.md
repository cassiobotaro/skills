# Armazenamento dos arquivos exportados em bucket S3

| | |
|---|---|
| **Estado** | Rascunho |
| **Autores** | Time de Relatórios |
| **Revisores** | A definir (ver Questões em aberto) |
| **Criado em** | 2026-11-16 |
| **Última atualização** | 2026-11-16 |
| **Altera** | [Exportação de relatórios em background](exportacao-de-relatorios.md) |

## Glossário

- **S3**: serviço de object storage da AWS, onde os arquivos exportados ficam agora.
- **Bucket**: o contêiner no S3 que guarda os arquivos.

## Visão geral

O documento original da exportação de relatórios previa um único worker, que gravava o CSV no próprio disco e servia o download. O serviço já está em produção e agora roda com dois workers. Este documento registra a mudança do local dos arquivos gerados: do disco local do worker para um bucket S3.

## Contexto

A solução original gravava cada arquivo em `/var/exports/<job_id>.csv` e servia `GET /exports/<job_id>/download` pelo mesmo worker que o gerou. Isso funcionava porque o design assumia um único worker (trade-off registrado no documento original).

Com a subida de um segundo worker, o pedido de download passou a cair, às vezes, no worker que não gerou o arquivo. Esse worker não encontrava o arquivo no disco e devolvia 404.

## Mudança

Os arquivos gerados saíram do disco local do worker e passaram a ficar num bucket S3. Como o arquivo não depende mais do disco de um worker específico, qualquer worker pode atender o download.

Os detalhes de como o download é servido hoje, do nome do bucket e da retenção estão em Questões em aberto.

## Trade-offs

- ✓ O download deixa de depender de qual worker gerou o arquivo, o que elimina o 404 que motivou a mudança.
- ✗ O serviço ganha uma dependência de infraestrutura que o design original evitava. O documento original já apontava que o bucket exigia credenciais e uma política de retenção novas.
- ✗ Custo aceito pelo time: a confirmar (ver Questões em aberto).

## Alternativas consideradas

- **Manter o disco local** (não fazer nada): descartada, porque com dois workers o download devolve 404 sempre que cai no worker errado.
- Outras alternativas que o time avaliou: a confirmar (ver Questões em aberto).

## Questões em aberto

1. Quando a mudança entrou em produção?
2. Como o download funciona agora: a API ou o worker lê do bucket e devolve o arquivo, ou o usuário recebe um link direto para o bucket? O contrato do endpoint `GET /exports/<job_id>/download` mudou?
3. A retenção de 7 dias continua? Como ela é aplicada no bucket (regra do bucket, cron)?
4. O que aconteceu com os arquivos que estavam no disco do worker na hora da mudança?
5. Que custo ou risco o time aceitou com a mudança (custo de armazenamento, credenciais, dependência do S3)?
6. O time considerou outras saídas, por exemplo direcionar o download ao worker que gerou o arquivo ou usar disco compartilhado? Se sim, por que perderam?
7. Quem fora do time é afetado (Plataforma/Infraestrutura pelo bucket e pelas credenciais, Segurança pelo acesso aos arquivos)? Quem deve revisar este documento?
