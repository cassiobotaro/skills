# Exportação de relatórios: arquivos gerados em bucket S3

| | |
|---|---|
| **Estado** | Implementado |
| **Autores** | Time de Relatórios |
| **Altera** | [Exportação de relatórios em background](exportacao-de-relatorios.md) |
| **Criado em** | 2026-11-16 |
| **Última atualização** | 2026-11-16 |

## Visão geral

O [design original](exportacao-de-relatorios.md) gravava o CSV gerado no disco local do worker e servia o download a partir dele. Os arquivos gerados agora ficam num bucket S3. Este documento registra a mudança e o motivo. O resto do design original continua valendo, exceto onde este documento diz o contrário.

## O que mudou

| | Antes (design original) | Agora |
|---|---|---|
| Onde o worker grava o CSV | Disco local do worker, em `/var/exports/<job_id>.csv` | Bucket S3 |

## Por que mudou

O time subiu um segundo worker. O arquivo existe só onde foi gerado, então quando o `GET /exports/<job_id>/download` caía no worker que não tinha o arquivo, a resposta era 404. O design original assumia um único worker (está nos trade-offs dele), e essa premissa deixou de valer.

## Alternativas consideradas

**Não fazer nada.** Descartada: com dois workers, o download devolvia 404 sempre que a request caía no worker que não gerou o arquivo.

As demais alternativas que o time pesou estão nas questões em aberto.

## Trade-offs

O que o time aceitou em troca está nas questões em aberto. O design original já apontava o que o bucket exigiria: credenciais e política de retenção novas.

## Questões em aberto

- Quando a mudança entrou em produção?
- Quem serve o `GET /exports/<job_id>/download` hoje, e como ele entrega o arquivo ao usuário?
- Como funciona a retenção hoje? O design original previa 7 dias, com um cron do worker apagando os arquivos mais antigos.
- O que acontece com os arquivos que estavam no disco dos workers quando a mudança entrou?
- Que outras alternativas o time considerou para o 404 (por exemplo, um volume compartilhado entre os workers), e por que o bucket venceu?
- O que essa abordagem piora, e o que o time decidiu aceitar (custo, nova dependência, credenciais, latência)?
