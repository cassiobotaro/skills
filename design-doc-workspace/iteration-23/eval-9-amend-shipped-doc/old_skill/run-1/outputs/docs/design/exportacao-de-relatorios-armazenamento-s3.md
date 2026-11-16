# Exportação de relatórios: arquivos gerados passam para um bucket S3

| | |
|---|---|
| **Estado** | Rascunho |
| **Autores** | A confirmar |
| **Revisores** | A confirmar |
| **Criado em** | 2026-11-16 |
| **Última atualização** | 2026-11-16 |
| **Altera** | [Exportação de relatórios em background](exportacao-de-relatorios.md) |

## Visão geral

O serviço de exportação de relatórios, em produção desde março, gravava cada CSV no disco local do worker que o gerou. Com um segundo worker, o download às vezes chegava ao worker que não tinha o arquivo e devolvia 404. Os arquivos gerados passaram a ficar num bucket S3. Este documento registra a mudança e o motivo. O design original continua valendo para o restante do serviço.

## O que mudou

O [design original](exportacao-de-relatorios.md) (seção Solução) gravava o arquivo em `/var/exports/<job_id>.csv` no disco do worker, e o endpoint `GET /exports/<job_id>/download` lia desse disco. Agora os arquivos gerados ficam num bucket S3, e não mais no disco local do worker.

O design original assumia um único worker, e o doc listava isso como custo aceito ("A solução assume um único worker"). Ao subir o segundo worker, essa premissa deixou de valer: o arquivo existia só no worker que o gerou, e o download que caía no outro devolvia 404.

## Trade-offs

- ✓ O arquivo deixa de depender de qual worker o gerou, o que elimina o 404 no download com mais de um worker.
- ✓ O custo do original "se o disco do worker se perde, os arquivos dos últimos 7 dias se perdem junto" deixa de ser, em princípio, do disco local. Falta confirmar a retenção no bucket (ver Questões em aberto).
- ✗ Os custos desta mudança ainda não foram informados pelo time (ver Questões em aberto).

## Alternativas consideradas

**Manter o disco local.** Descartada: com dois workers, o download devolve 404 sempre que cai no worker que não gerou o arquivo.

**Bucket de object storage.** Foi a alternativa que o design original descartou porque exigia credenciais e política de retenção novas, com um único worker previsto. A escolha agora é essa alternativa, e o segundo worker é o que muda a conta.

Outras opções que o time tenha avaliado (por exemplo, roteamento do download ao worker dono do arquivo, ou disco compartilhado) não foram informadas e estão em Questões em aberto.

## Questões em aberto

1. Quando a mudança entrou em produção (data)?
2. Como o download funciona hoje: quem serve o arquivo, e o endpoint `GET /exports/<job_id>/download` continua o mesmo?
3. Qual é a retenção dos arquivos no bucket? Os 7 dias e o cron de limpeza do worker continuam valendo, ou a expiração passou para o bucket?
4. Que custos o time aceitou com a mudança (storage, credenciais, transferência, nova dependência, latência)? O original apontava o custo de credenciais e de retenção.
5. Que outras alternativas o time considerou além do bucket?
6. Os arquivos que estavam no disco dos workers na hora da mudança foram migrados ou descartados?
7. Quem são os autores e os revisores deste documento?
