# Armazenamento dos relatórios exportados em bucket S3

| | |
|---|---|
| **Estado** | Implementado |
| **Autores** | A confirmar (ver Questões em aberto) |
| **Revisores** | A confirmar (ver Questões em aberto) |
| **Emenda** | [Exportação de relatórios em background](exportacao-de-relatorios.md) |
| **Criado em** | 2026-11-22 |
| **Última atualização** | 2026-11-22 |

## Visão geral

O design original da [exportação de relatórios](exportacao-de-relatorios.md) gravava cada CSV no disco local do worker que o gerou. Este documento registra a mudança desse armazenamento para um bucket S3 e o motivo: com dois workers, o download podia cair no worker que não tinha o arquivo e devolvia 404.

## Contexto

O design original assumia um único worker, e dizia isso entre os seus trade-offs: "o arquivo só existe no worker que o gerou". O serviço está em produção desde março. Depois disso o time subiu um segundo worker, e a premissa deixou de valer. O endpoint `GET /exports/<job_id>/download` é servido pelo worker que recebe a request. Quando esse worker não era o que gerou o arquivo, ele não o encontrava em `/var/exports/<job_id>.csv` e respondia 404.

## Objetivos e fora de escopo

Objetivo:

- O download de uma exportação pronta não falha com 404 por causa do worker que atende a request.

Fora de escopo: a geração do CSV, a tabela `export_jobs` e o fluxo de enfileiramento não mudam com esta emenda, a menos que as questões em aberto digam o contrário.

## Solução

Os arquivos gerados deixam de ficar no disco local do worker e passam a ficar em um bucket S3. O restante do design original continua valendo: a API grava o pedido em `export_jobs`, um worker gera o CSV e o usuário baixa quando fica pronto.

Este documento não descreve, para o bucket, os detalhes que o design original fixava para o disco (caminho do arquivo, retenção de 7 dias, limpeza por cron), nem o caminho do download. Esses pontos estão nas questões em aberto.

## Trade-offs da solução escolhida

- ✓ O arquivo deixa de depender do disco de um worker específico, que era a causa do 404.
- ✗ O serviço passa a depender de um bucket S3, uma dependência que o design original evitava ("nenhuma dependência nova").

O design original previa dois outros custos para essa opção: credenciais novas e uma política de retenção nova. Se o time os pagou, e quais outros custos aceitou, está nas questões em aberto.

## Alternativas consideradas

**Manter o disco local.** O design original escolheu essa opção por assumir um único worker. A premissa deixou de valer quando o segundo worker subiu, e o 404 no download é a consequência.

**Gravar num bucket de object storage.** Era a alternativa que o design original rejeitou pelo custo de credenciais e retenção, com um único worker previsto. É a opção adotada aqui.

As demais alternativas que o time avaliou, se houve, estão nas questões em aberto.

## Questões em aberto

Cada item abaixo precisa de resposta para fechar o documento. O texto acima não afirma nenhum deles.

1. Quando a mudança para o S3 entrou em produção? E quando o segundo worker subiu?
2. Quem são os autores e os revisores desta emenda?
3. O que essa abordagem piorou, e o que o time decidiu aceitar? Por exemplo: custo de armazenamento, latência do download, dependência da disponibilidade do S3.
4. Como funciona o download hoje? O worker lê do bucket e devolve o arquivo, ou o usuário baixa direto do S3 (por exemplo, por link temporário)? O endpoint `GET /exports/<job_id>/download` mudou?
5. A retenção de 7 dias continua? Se sim, quem a aplica hoje (cron do worker, política de ciclo de vida do bucket, outro mecanismo)?
6. Como o worker acessa o bucket (credenciais, permissões), e quem aprovou? O time de Plataforma foi consultado?
7. O que aconteceu com os arquivos que estavam no disco do worker no momento da mudança? Houve migração ou eles expiraram?
8. Quais outras alternativas o time considerou para resolver o 404 (além de manter o disco e adotar o bucket), e por que perderam?
9. Os dois trade-offs do design original (premissa de um único worker, perda dos arquivos se o disco se perde) ainda se aplicam ao desenho com S3?
10. O objetivo de entregar o link em até 5 minutos para relatórios de até 1 milhão de linhas se mantém com o upload para o S3?
