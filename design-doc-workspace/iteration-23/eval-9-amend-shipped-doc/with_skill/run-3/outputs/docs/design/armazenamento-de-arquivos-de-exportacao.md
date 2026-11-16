# Arquivos de exportação em bucket S3

| | |
|---|---|
| **Estado** | Implementado |
| **Autores** | Time de Relatórios |
| **Revisores** | A definir |
| **Criado em** | 2026-11-16 |
| **Última atualização** | 2026-11-16 |
| **Altera** | [Exportação de relatórios em background](exportacao-de-relatorios.md) |

## Visão geral

O worker de exportação deixou de gravar os CSVs no disco local e passou a gravá-los num bucket S3. Este documento altera a seção "Solução" do design doc original, que está em produção desde março, e registra por que a mudança foi feita.

## Problema

O design original assumia um único worker (ver "Trade-offs da solução escolhida"), porque o arquivo só existe no disco do worker que o gerou. O time subiu um segundo worker. Quando o `GET /exports/<job_id>/download` cai no worker que não gerou o arquivo, ele não o encontra e devolve 404.

## Mudança

O worker grava o arquivo gerado num bucket S3 em vez de `/var/exports/<job_id>.csv`. Com o arquivo fora do disco de qualquer worker, o download não depende mais de qual worker recebe a request. O restante do design original (tabela `export_jobs`, resposta 202, geração em background) segue como descrito lá.

## Trade-offs

- ✓ O arquivo deixa de pertencer a um worker, o que remove a causa dos 404 com mais de um worker.
- ✗ O design original citou, ao descartar o bucket, credenciais e política de retenção novas como custo. O que o time de fato assumiu em troca está nas questões em aberto.

## Alternativas consideradas

**Não fazer nada.** Com dois workers, parte dos downloads devolve 404. Descartada por isso.

As demais alternativas que o time avaliou (por exemplo, afinidade de download ao worker que gerou o arquivo) não foram informadas e ficam nas questões em aberto.

## Questões em aberto

- Quando a mudança entrou em produção?
- Que custo o time aceitou com o bucket (credenciais, retenção, custo de storage e de transferência, latência de download)?
- Quem serve o download hoje: o worker lendo do S3, ou outro caminho?
- Qual é a política de retenção no bucket? Os 7 dias e o cron de limpeza do worker continuam valendo?
- O que aconteceu com os arquivos que estavam no disco dos workers na hora da mudança?
- Que outras alternativas o time avaliou além de "não fazer nada"?
- Quem revisa este documento?
