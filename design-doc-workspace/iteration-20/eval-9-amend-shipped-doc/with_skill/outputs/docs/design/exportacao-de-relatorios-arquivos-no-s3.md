# Exportação de relatórios: arquivos gerados no S3

| | |
|---|---|
| **Estado** | Implementado |
| **Emenda a** | [Exportação de relatórios em background](exportacao-de-relatorios.md) |
| **Autores** | A confirmar (ver [Questões em aberto](#questões-em-aberto)) |
| **Revisores** | A confirmar (ver [Questões em aberto](#questões-em-aberto)) |
| **Criado em** | 2026-11-16 |
| **Última atualização** | 2026-11-16 |

## Visão geral

O [design original](exportacao-de-relatorios.md) guardava cada arquivo gerado no disco local do worker que o gerou e assumia um único worker. O time subiu um segundo worker, e o download passou a cair às vezes no worker que não tinha o arquivo, que devolvia 404.

Esta emenda registra a mudança que o time fez para resolver isso: os arquivos gerados saíram do disco local do worker e foram para um bucket S3. O restante do design original continua valendo.

## Objetivos e fora de escopo

Objetivos:

- O download de um arquivo gerado funciona com mais de um worker em produção: a resposta não depende de qual worker gerou o arquivo.

Fora de escopo:

- O time ainda não informou o que esta mudança deixou de fora de propósito (ver [Questões em aberto](#questões-em-aberto)).

## Solução

O worker deixou de gravar o CSV em `/var/exports/<job_id>.csv` e passou a gravá-lo em um bucket S3. O arquivo não fica mais preso ao worker que o gerou.

Esta emenda muda apenas o lugar onde os arquivos ficam. O enfileiramento do pedido na tabela `export_jobs` e a geração do CSV pelo worker seguem como descritos no documento original.

Dois pontos do design original dependiam do disco local e ainda precisam ser descritos aqui: como o endpoint `GET /exports/<job_id>/download` entrega o arquivo agora, e como funciona a retenção de 7 dias, que era feita por um cron do worker. Os dois estão em [Questões em aberto](#questões-em-aberto).

## Trade-offs da solução escolhida

- ✓ O arquivo não existe mais só no worker que o gerou. O serviço roda com dois workers sem o 404 no download.
- ✓ A perda do disco de um worker não leva junto os arquivos gerados, risco que o documento original listava.
- ✗ O serviço ganhou uma dependência nova. O documento original listava como vantagem não ter nenhuma além da tabela de jobs e do disco do worker.
- ✗ Os arquivos agora ficam em storage externo. O documento original listava como vantagem do disco local o download sem custo de transferência de storage externo.
- ✗ O documento original apontava que um bucket exigia credenciais e política de retenção novas. Era o custo que o time evitou enquanto previa um único worker.

Os três custos acima vêm do documento original. Falta o time confirmar quais deles pesaram na prática e se apareceu algum outro (ver [Questões em aberto](#questões-em-aberto)).

## Alternativas consideradas

**Gravar os arquivos num bucket de object storage (escolhida).** O documento original já descrevia esta opção e a descartou porque, com um único worker previsto, o custo de credenciais e política de retenção novas era desnecessário. Com o segundo worker, a premissa que sustentava o descarte deixou de valer.

**Não fazer nada.** Descartada: com dois workers e os arquivos no disco local de cada um, o download caía no worker que não tinha o arquivo e devolvia 404.

O time ainda não registrou se avaliou outras saídas antes de ir para o S3 (ver [Questões em aberto](#questões-em-aberto)).

## Questões em aberto

1. Como o endpoint `GET /exports/<job_id>/download` entrega o arquivo agora?
2. Como funciona a retenção de 7 dias agora que o arquivo não está mais no disco do worker? O prazo continua o mesmo?
3. O que aconteceu com os arquivos que já estavam no disco dos workers no momento da mudança?
4. Quais custos o time aceitou ao ir para o S3, além dos que o documento original já previa?
5. O time avaliou outras alternativas antes de escolher o S3? Quais, e por que perderam?
6. O que motivou subir o segundo worker?
7. O que ficou deliberadamente fora de escopo nesta mudança?
8. Quando a mudança entrou em produção?
9. Quem são os autores desta emenda e quem a revisou?
