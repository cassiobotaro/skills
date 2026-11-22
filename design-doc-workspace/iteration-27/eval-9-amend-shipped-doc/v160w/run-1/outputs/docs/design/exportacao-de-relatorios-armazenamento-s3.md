# Exportação de relatórios: arquivos gerados passam para o S3

| | |
|---|---|
| **Estado** | Implementado |
| **Autores** | Time de Relatórios |
| **Revisores** | A definir (ver Questões em aberto) |
| **Altera** | [Exportação de relatórios em background](exportacao-de-relatorios.md) |
| **Criado em** | 2026-11-22 |
| **Última atualização** | 2026-11-22 |

## Visão geral

O documento original de exportação de relatórios guardava cada CSV gerado no disco local do worker. Este documento registra a mudança: os arquivos gerados agora ficam num bucket S3. O motivo foi o 404 que o download devolvia depois que o serviço passou a ter dois workers.

## Contexto

O [design original](exportacao-de-relatorios.md) fez uma escolha explícita: o worker gravava o arquivo em `/var/exports/<job_id>.csv` e o próprio worker servia `GET /exports/<job_id>/download`. O documento listava a consequência como custo aceito: "o arquivo só existe no worker que o gerou. A solução assume um único worker." Ele também descartou o bucket de object storage porque, com um único worker previsto, o custo de credenciais e de uma política de retenção nova parecia desnecessário.

O serviço está em produção desde março de 2026. O time subiu um segundo worker. Quando o pedido de download chegava ao worker que não tinha gerado o arquivo, o endpoint devolvia 404.

## O que mudou

- Antes: o worker gravava o CSV no disco local e servia o download a partir dele.
- Agora: o arquivo gerado fica num bucket S3.

Este documento não trata de nenhuma outra parte do design original. Se mais alguma mudou, ver Questões em aberto.

## Trade-offs

- ✓ Os workers passam a ter acesso ao mesmo armazenamento, e não só o que gerou o arquivo. O design original aceitava como custo a premissa de um único worker, e o bucket tira essa premissa do design.
- ✗ O serviço ganha uma dependência de infraestrutura nova, o bucket S3. O design original apontava como custo dessa opção credenciais e política de retenção novas.
- ✗ O design original listava como vantagem "nenhuma dependência nova" e "download sem custo de transferência de storage externo". As duas vantagens deixam de valer na forma em que foram escritas. Se o custo de transferência existe no desenho atual depende de como o download é servido (ver Questões em aberto).

## Alternativas consideradas

**Manter o disco local do worker.** Descartada: com dois workers, parte dos downloads devolve 404.

**Gravar os arquivos num bucket de object storage.** É a opção escolhida. O design original já a havia descartado, sob a premissa de um único worker.

As demais alternativas que o time avaliou entram pela questão 7.

## Questões em aberto

O responsável por responder é o Time de Relatórios, salvo indicação.

Mudança:

1. Em que data a mudança entrou em produção?
2. Quem serve `GET /exports/<job_id>/download` hoje: o worker lendo do S3, a API, ou um link direto para o bucket (por exemplo, URL pré-assinada)? Isso define o fluxo de download e o custo de transferência.
3. A retenção de 7 dias continua? Se sim, quem apaga os arquivos antigos: o cron do worker ou uma regra de ciclo de vida do bucket?
4. O que aconteceu com os arquivos que já estavam no disco dos workers no momento da mudança?
5. O caminho de `/var/exports` e o cron de limpeza do disco foram removidos?

Trade-offs e alternativas:

6. O que o time decidiu aceitar com o S3 (custo, latência, credenciais, acesso ao bucket)?
7. O time considerou outras saídas além do bucket, como volume compartilhado entre workers, roteamento do download para o worker de origem ou um único worker? Se sim, por que perderam?

Revisão:

8. Quem deve revisar este documento? O revisor do original foi Marina Prado (Plataforma). Segurança ou Infraestrutura precisam revisar o acesso ao bucket e as credenciais?
9. Além do local de armazenamento dos arquivos, mais alguma parte do design original mudou?
10. O Time de Relatórios é de fato o autor desta mudança?
