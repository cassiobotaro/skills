# Armazenamento das exportações em bucket S3

| | |
|---|---|
| **Estado** | Implementado |
| **Autores** | A confirmar (ver Questões em aberto) |
| **Revisores** | A confirmar (ver Questões em aberto) |
| **Criado em** | 2026-11-22 |
| **Última atualização** | 2026-11-22 |
| **Altera** | [Exportação de relatórios em background](exportacao-de-relatorios.md) |

## Visão geral

Este documento altera o design de [Exportação de relatórios em background](exportacao-de-relatorios.md), já em produção desde março. Os arquivos CSV gerados deixaram de ficar no disco local do worker e passaram a ficar num bucket S3. O documento original continua como o registro da decisão anterior e das razões dela.

## Contexto

O design original gravava cada arquivo em `/var/exports/<job_id>.csv`, no disco do worker que o gerou, e servia o download por esse mesmo worker. O documento original registrava essa limitação: "O arquivo só existe no worker que o gerou. A solução assume um único worker."

O time subiu um segundo worker. Quando o pedido de download chegava ao worker que não tinha gerado o arquivo, o endpoint devolvia 404.

## Objetivos e fora de escopo

Objetivo:

- O download de uma exportação pronta não falha com 404 por causa do worker que atende o pedido.

## Solução

O worker grava o CSV gerado num bucket S3, no lugar do disco local (`/var/exports/<job_id>.csv`). Esta mudança trata de onde o arquivo fica. Como o download funciona agora é a pergunta 3.

## Trade-offs da solução escolhida

- ✓ O arquivo gerado não fica mais preso ao disco do worker que o gerou, que era a causa do 404.
- ✗ O documento original apontava, como custo da alternativa do bucket, credenciais e política de retenção novas. O custo que o time aceitou de fato está em Questões em aberto.

## Alternativas consideradas

**Manter os arquivos no disco local.** Era o design original. Com dois workers, o download devolvia 404 sempre que caía no worker que não tinha o arquivo.

**Gravar os arquivos num bucket S3.** Escolhida. O documento original já a havia descartado, com a premissa de um único worker; o segundo worker desfez essa premissa.

Se o time avaliou outras saídas, falta registrá-las (pergunta 8).

## Questões em aberto

Perguntas para quem fez a mudança. Cada resposta entra no corpo do documento e sai desta lista.

1. Quem são os autores e os revisores deste documento? O original tinha Marina Prado (Plataforma) como revisora; ela deve revisar também?
2. Em que data a mudança foi para produção?
3. Quem serve o `GET /exports/<job_id>/download` hoje? Continua sendo o worker (lendo do bucket), a API, ou o cliente baixa direto do S3 (por exemplo com URL pré-assinada)?
4. Como funciona a retenção hoje? Os arquivos continuam expirando em 7 dias? Quem apaga (o cron do worker, uma regra de lifecycle do bucket)?
5. Como o worker se autentica no bucket (credenciais, role)? O bucket é privado? Quem é o dono dele (Plataforma, Relatórios)?
6. O que aconteceu com os arquivos que estavam no disco dos workers na hora da migração? Os links de download de exportações antigas continuam funcionando?
7. O que a mudança piorou ou encareceu, e o que o time decidiu aceitar? Por exemplo: custo de storage e de transferência (o original listava "download sem custo de transferência de storage externo" como vantagem), nova dependência do S3, latência do download.
8. O time avaliou outras saídas para o 404 além do bucket, como roteamento do download para o worker dono do arquivo ou um volume compartilhado entre os workers? Por que o bucket ganhou?
9. Há algo que o time deixou deliberadamente fora desta mudança (outros formatos, agendamento, mudança no limite de 5 minutos)?
10. Alguém fora do time de Relatórios foi impactado (Plataforma, Segurança, Infraestrutura)? Os dados exportados são sensíveis, e isso afeta o acesso ao bucket?
