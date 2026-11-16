# Arquivos de exportação em S3

| | |
|---|---|
| **Estado** | Rascunho |
| **Altera** | [Exportação de relatórios em background](exportacao-de-relatorios.md) |
| **Criado em** | 2026-11-16 |
| **Última atualização** | 2026-11-16 |

## Visão geral

O documento original da exportação de relatórios previa um único worker e guardava os arquivos gerados no disco local dele. Este documento registra a mudança desse ponto: os arquivos agora ficam em um bucket S3.

## Contexto

O serviço descrito no documento original está em produção desde março. Ele gravava cada CSV em `/var/exports/<job_id>.csv` e servia `GET /exports/<job_id>/download` a partir do worker que gerou o arquivo. O trade-off ✗ do original já apontava: "a solução assume um único worker".

## O que mudou e por quê

O time subiu um segundo worker. O pedido de download caía no worker que não tinha o arquivo e devolvia 404. Para resolver, os arquivos gerados saíram do disco local do worker e passaram a ficar em um bucket S3.

## Alternativas consideradas

**Não fazer nada.** Descartada: com dois workers, o download devolvia 404 sempre que caía no worker que não gerou o arquivo.

## Questões em aberto

Perguntas ao time, a responder antes de este documento sair de rascunho (as respostas entram no corpo e saem desta lista):

- Quando a mudança foi para produção?
- O que ela piorou ou encareceu, e o que o time decidiu aceitar (custo de storage, credenciais, dependência nova, latência de download)? Falta a seção de trade-offs.
- Quem serve o download agora, e como o arquivo chega ao usuário?
- A retenção de 7 dias e o cron que apagava os arquivos continuam valendo? Como?
- Que alternativas além de S3 o time avaliou (por exemplo, afinidade do download ao worker, ou disco compartilhado)?
- Quem assina o documento e quem deve revisar (Plataforma, Infraestrutura)?
