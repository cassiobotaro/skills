# Exportação de relatórios em background

| | |
|---|---|
| **Estado** | Implementado |
| **Autores** | Time de Relatórios |
| **Revisores** | Marina Prado (Plataforma) |
| **Criado em** | 2026-01-12 |
| **Última atualização** | 2026-11-16 |
| **Amended by** | [Arquivos gerados passam para um bucket S3](exportacao-de-relatorios-armazenamento-s3.md) (2026-11-16) |

## Visão geral

Relatórios grandes eram gerados dentro da request da API e estouravam o timeout de 30s do gateway. Este documento descreve o serviço que gera esses relatórios fora da request: a API enfileira o pedido, um worker gera o arquivo e o usuário baixa quando fica pronto.

## Objetivos e fora de escopo

Objetivos:

- Nenhuma exportação falha por timeout do gateway.
- O usuário recebe o link de download em até 5 minutos para relatórios de até 1 milhão de linhas.

Fora de escopo:

- Agendamento recorrente de relatórios.
- Formatos além de CSV.

## Solução

A API grava o pedido na tabela `export_jobs` e responde 202 com o id do job. Um worker lê os jobs pendentes, gera o CSV e grava o arquivo no disco local dele, em `/var/exports/<job_id>.csv`. O endpoint `GET /exports/<job_id>/download` é servido pelo próprio worker, que lê o arquivo do disco e devolve.

Os arquivos ficam 7 dias no disco; um cron do worker apaga os mais antigos.

## Trade-offs da solução escolhida

- ✓ Nenhuma dependência nova: só a tabela de jobs e o disco que o worker já tem.
- ✓ Download sem custo de transferência de storage externo.
- ✗ O arquivo só existe no worker que o gerou. A solução assume um único worker.
- ✗ Se o disco do worker se perde, os arquivos dos últimos 7 dias se perdem junto.

## Alternativas consideradas

**Gravar os arquivos num bucket de object storage.** Tiraria a dependência do disco do worker, mas exigia credenciais e política de retenção novas. Com um único worker previsto, o time considerou o custo desnecessário.

**Não fazer nada.** Descartada: as exportações acima de 200 mil linhas falhavam em toda tentativa.

## Questões em aberto

Nenhuma.
