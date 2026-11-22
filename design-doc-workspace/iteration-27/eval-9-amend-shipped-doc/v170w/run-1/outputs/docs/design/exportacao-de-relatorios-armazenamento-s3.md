# Exportação de relatórios: arquivos gerados passam para um bucket S3

| | |
|---|---|
| **Estado** | Implementado |
| **Autores** | Time de Relatórios |
| **Revisores** | A definir (ver Questões em aberto) |
| **Criado em** | 2026-11-22 |
| **Última atualização** | 2026-11-22 |
| **Altera** | [Exportação de relatórios em background](exportacao-de-relatorios.md) |

## Visão geral

Este documento registra uma mudança no serviço de exportação de relatórios: os arquivos gerados saíram do disco local do worker e passaram para um bucket S3. O time subiu um segundo worker, e o worker que recebia um download sem ter o arquivo devolvia 404.

O documento original continua valendo para o resto do serviço. Este registra só o que mudou, o motivo e o custo.

## Contexto

O [documento original](exportacao-de-relatorios.md) assumia um único worker. O worker gravava cada CSV em `/var/exports/<job_id>.csv` e servia o endpoint `GET /exports/<job_id>/download` lendo esse arquivo do próprio disco. O documento listava a suposição de um único worker como custo aceito.

O time subiu um segundo worker. Quando o download caía no worker que não gerou o arquivo, esse worker não o encontrava no disco e devolvia 404.

## Mudança

Os arquivos gerados ficam agora num bucket S3, e não mais no disco local do worker. Essa mudança substitui o trecho da seção Solução do documento original que descrevia o disco local em `/var/exports`.

## Trade-offs

- ✓ Os arquivos ficam fora dos workers, então o download deixa de depender de qual worker gerou o arquivo, e o segundo worker não causa mais 404.
- ✗ O serviço passa a depender do S3. O documento original contava "nenhuma dependência nova" como vantagem de usar o disco do worker.

O restante do custo aceito está em Questões em aberto.

## Alternativas consideradas

**Não fazer nada.** Descartada: com dois workers, o download devolvia 404 quando caía no worker que não tinha o arquivo.

**Gravar os arquivos num bucket de object storage (escolhida).** O documento original descartou essa opção porque exigia credenciais e política de retenção novas, e porque previa um único worker. Com o segundo worker, a premissa do worker único deixou de valer.

Outras alternativas que o time possa ter avaliado estão em Questões em aberto.

## Questões em aberto

O autor não estava disponível para responder durante a escrita. As perguntas abaixo ficaram sem resposta, e nenhuma seção acima afirma o que elas perguntam.

1. Quando o segundo worker subiu e quando os arquivos passaram a ir para o S3? Os arquivos que já estavam em `/var/exports` foram migrados ou descartados?
2. Como o download funciona agora? O worker lê do bucket e devolve o arquivo, ou o usuário baixa direto do S3? O endpoint `GET /exports/<job_id>/download` mudou?
3. Os arquivos ainda ficam 7 dias? Quem apaga os antigos agora: o cron do worker ou uma regra de ciclo de vida do bucket?
4. Quem cria e mantém as credenciais do bucket, e quem tem acesso aos arquivos? O documento original citava credenciais novas como custo dessa opção.
5. O que a mudança piorou e o time decidiu aceitar? O documento original listava "download sem custo de transferência de storage externo" como vantagem do disco local. O custo de armazenamento e de transferência do S3 entra aqui?
6. O risco do documento original de perder os arquivos dos últimos 7 dias com o disco do worker deixa de existir com o bucket?
7. O time considerou outras saídas além do bucket, como direcionar o download ao worker que gerou o arquivo ou usar um volume compartilhado? Se sim, por que perderam?
8. Quem revisa este documento? A Marina Prado (Plataforma) revisou o original. Ela ou outra pessoa precisa revisar as credenciais e o acesso ao bucket?
