# Judge packet

Decide each check below as met or unmet from this packet alone.
- A met check of kind `reply` must quote the literal words that satisfy it.
- An unmet check records what you searched for and where.
- A met check of kind `invention` has nothing to quote: record what you searched for.
- Borderline is unmet. More text or more files never raise a verdict.

## The user's message

O design doc docs/design/exportacao-de-relatorios.md foi aprovado e o serviço tá em produção desde março. A gente mudou onde os arquivos gerados ficam: saíram do disco local do worker e foram pra um bucket S3, porque subimos um segundo worker e o download caía no worker que não tinha o arquivo e devolvia 404. Atualiza a documentação.

## The document as it was before the run (docs/design/exportacao-de-relatorios.md)

```
   1  # Exportação de relatórios em background
   2  
   3  | | |
   4  |---|---|
   5  | **Estado** | Implementado |
   6  | **Autores** | Time de Relatórios |
   7  | **Revisores** | Marina Prado (Plataforma) |
   8  | **Criado em** | 2026-01-12 |
   9  | **Última atualização** | 2026-03-03 |
  10  
  11  ## Visão geral
  12  
  13  Relatórios grandes eram gerados dentro da request da API e estouravam o timeout de 30s do gateway. Este documento descreve o serviço que gera esses relatórios fora da request: a API enfileira o pedido, um worker gera o arquivo e o usuário baixa quando fica pronto.
  14  
  15  ## Objetivos e fora de escopo
  16  
  17  Objetivos:
  18  
  19  - Nenhuma exportação falha por timeout do gateway.
  20  - O usuário recebe o link de download em até 5 minutos para relatórios de até 1 milhão de linhas.
  21  
  22  Fora de escopo:
  23  
  24  - Agendamento recorrente de relatórios.
  25  - Formatos além de CSV.
  26  
  27  ## Solução
  28  
  29  A API grava o pedido na tabela `export_jobs` e responde 202 com o id do job. Um worker lê os jobs pendentes, gera o CSV e grava o arquivo no disco local dele, em `/var/exports/<job_id>.csv`. O endpoint `GET /exports/<job_id>/download` é servido pelo próprio worker, que lê o arquivo do disco e devolve.
  30  
  31  Os arquivos ficam 7 dias no disco; um cron do worker apaga os mais antigos.
  32  
  33  ## Trade-offs da solução escolhida
  34  
  35  - ✓ Nenhuma dependência nova: só a tabela de jobs e o disco que o worker já tem.
  36  - ✓ Download sem custo de transferência de storage externo.
  37  - ✗ O arquivo só existe no worker que o gerou. A solução assume um único worker.
  38  - ✗ Se o disco do worker se perde, os arquivos dos últimos 7 dias se perdem junto.
  39  
  40  ## Alternativas consideradas
  41  
  42  **Gravar os arquivos num bucket de object storage.** Tiraria a dependência do disco do worker, mas exigia credenciais e política de retenção novas. Com um único worker previsto, o time considerou o custo desnecessário.
  43  
  44  **Não fazer nada.** Descartada: as exportações acima de 200 mil linhas falhavam em toda tentativa.
  45  
  46  ## Questões em aberto
  47  
  48  Nenhuma.
```

## The reply given to the user

```
   1  Como o serviço está em produção desde março, não mexi no corpo do design doc original: ele é o registro de por que o sistema foi construído daquele jeito. Fiz duas coisas:
   2  
   3  1. Criei `docs/design/armazenamento-de-arquivos-de-exportacao.md`, um mini-doc que aponta para o original, descreve o problema (segundo worker, download caindo no worker sem o arquivo e devolvendo 404) e a mudança (arquivos do disco local para um bucket S3).
   4  2. No `docs/design/exportacao-de-relatorios.md`, só o cabeçalho mudou: `Última atualização` agora é 2026-11-16 e entrou a linha `Alterado por`, com link para o mini-doc.
   5  
   6  O mini-doc só afirma o que você contou. Ficou como questões em aberto, e preciso das respostas para fechá-las:
   7  
   8  - Quando a mudança entrou em produção?
   9  - Qual custo o time aceitou com o bucket (credenciais, retenção, custo de storage e transferência, latência)? Hoje a seção de trade-offs tem só o ganho e a menção ao custo que o doc original previa.
  10  - Quem serve o download agora: o worker lendo do S3 ou outro caminho?
  11  - A retenção de 7 dias e o cron de limpeza do worker continuam valendo, ou a retenção passou para o bucket?
  12  - O que aconteceu com os arquivos que estavam no disco dos workers na hora da troca?
  13  - Além de "não fazer nada", que outras alternativas vocês avaliaram (por exemplo, direcionar o download ao worker que gerou o arquivo)?
  14  - Quem revisa o mini-doc?
```

## Files under the project root after the run

### docs/design/armazenamento-de-arquivos-de-exportacao.md

```
   1  # Arquivos de exportação em bucket S3
   2  
   3  | | |
   4  |---|---|
   5  | **Estado** | Implementado |
   6  | **Autores** | Time de Relatórios |
   7  | **Revisores** | A definir |
   8  | **Criado em** | 2026-11-16 |
   9  | **Última atualização** | 2026-11-16 |
  10  | **Altera** | [Exportação de relatórios em background](exportacao-de-relatorios.md) |
  11  
  12  ## Visão geral
  13  
  14  O worker de exportação deixou de gravar os CSVs no disco local e passou a gravá-los num bucket S3. Este documento altera a seção "Solução" do design doc original, que está em produção desde março, e registra por que a mudança foi feita.
  15  
  16  ## Problema
  17  
  18  O design original assumia um único worker (ver "Trade-offs da solução escolhida"), porque o arquivo só existe no disco do worker que o gerou. O time subiu um segundo worker. Quando o `GET /exports/<job_id>/download` cai no worker que não gerou o arquivo, ele não o encontra e devolve 404.
  19  
  20  ## Mudança
  21  
  22  O worker grava o arquivo gerado num bucket S3 em vez de `/var/exports/<job_id>.csv`. Com o arquivo fora do disco de qualquer worker, o download não depende mais de qual worker recebe a request. O restante do design original (tabela `export_jobs`, resposta 202, geração em background) segue como descrito lá.
  23  
  24  ## Trade-offs
  25  
  26  - ✓ O arquivo deixa de pertencer a um worker, o que remove a causa dos 404 com mais de um worker.
  27  - ✗ O design original citou, ao descartar o bucket, credenciais e política de retenção novas como custo. O que o time de fato assumiu em troca está nas questões em aberto.
  28  
  29  ## Alternativas consideradas
  30  
  31  **Não fazer nada.** Com dois workers, parte dos downloads devolve 404. Descartada por isso.
  32  
  33  As demais alternativas que o time avaliou (por exemplo, afinidade de download ao worker que gerou o arquivo) não foram informadas e ficam nas questões em aberto.
  34  
  35  ## Questões em aberto
  36  
  37  - Quando a mudança entrou em produção?
  38  - Que custo o time aceitou com o bucket (credenciais, retenção, custo de storage e de transferência, latência de download)?
  39  - Quem serve o download hoje: o worker lendo do S3, ou outro caminho?
  40  - Qual é a política de retenção no bucket? Os 7 dias e o cron de limpeza do worker continuam valendo?
  41  - O que aconteceu com os arquivos que estavam no disco dos workers na hora da mudança?
  42  - Que outras alternativas o time avaliou além de "não fazer nada"?
  43  - Quem revisa este documento?
```

### docs/design/exportacao-de-relatorios.md

```
   1  # Exportação de relatórios em background
   2  
   3  | | |
   4  |---|---|
   5  | **Estado** | Implementado |
   6  | **Autores** | Time de Relatórios |
   7  | **Revisores** | Marina Prado (Plataforma) |
   8  | **Criado em** | 2026-01-12 |
   9  | **Última atualização** | 2026-11-16 |
  10  | **Alterado por** | [Arquivos de exportação em bucket S3](armazenamento-de-arquivos-de-exportacao.md) |
  11  
  12  ## Visão geral
  13  
  14  Relatórios grandes eram gerados dentro da request da API e estouravam o timeout de 30s do gateway. Este documento descreve o serviço que gera esses relatórios fora da request: a API enfileira o pedido, um worker gera o arquivo e o usuário baixa quando fica pronto.
  15  
  16  ## Objetivos e fora de escopo
  17  
  18  Objetivos:
  19  
  20  - Nenhuma exportação falha por timeout do gateway.
  21  - O usuário recebe o link de download em até 5 minutos para relatórios de até 1 milhão de linhas.
  22  
  23  Fora de escopo:
  24  
  25  - Agendamento recorrente de relatórios.
  26  - Formatos além de CSV.
  27  
  28  ## Solução
  29  
  30  A API grava o pedido na tabela `export_jobs` e responde 202 com o id do job. Um worker lê os jobs pendentes, gera o CSV e grava o arquivo no disco local dele, em `/var/exports/<job_id>.csv`. O endpoint `GET /exports/<job_id>/download` é servido pelo próprio worker, que lê o arquivo do disco e devolve.
  31  
  32  Os arquivos ficam 7 dias no disco; um cron do worker apaga os mais antigos.
  33  
  34  ## Trade-offs da solução escolhida
  35  
  36  - ✓ Nenhuma dependência nova: só a tabela de jobs e o disco que o worker já tem.
  37  - ✓ Download sem custo de transferência de storage externo.
  38  - ✗ O arquivo só existe no worker que o gerou. A solução assume um único worker.
  39  - ✗ Se o disco do worker se perde, os arquivos dos últimos 7 dias se perdem junto.
  40  
  41  ## Alternativas consideradas
  42  
  43  **Gravar os arquivos num bucket de object storage.** Tiraria a dependência do disco do worker, mas exigia credenciais e política de retenção novas. Com um único worker previsto, o time considerou o custo desnecessário.
  44  
  45  **Não fazer nada.** Descartada: as exportações acima de 200 mil linhas falhavam em toda tentativa.
  46  
  47  ## Questões em aberto
  48  
  49  Nenhuma.
```

## Anchor cases for checks of kind `invention`

Decide by analogy with these; they come from another run of the same task.

- MET: User: 'subimos um segundo worker e o download caía no worker que não tinha o arquivo e devolvia 404'. Document, under Alternativas consideradas: 'Não fazer nada. Descartada: com dois workers, o download caía no worker que não tinha o arquivo e devolvia 404.' Why: The status quo the user described, with the user's own reason for leaving it. Listing it under alternatives asserts nothing the user did not say.
- UNMET: Same user message. Document: 'Não fazer nada. Descartada: os 404 geravam chamados no suporte e o time avaliou que o custo de manter o disco local era maior.' Why: Support tickets, an evaluation by the team and a cost comparison are not in the user's message. The entry now reports a deliberation that was never described.
- UNMET: User states a solution and no problem. Document: 'Não fazer nada. Descartada: o cadastro ficaria incompleto.' Why: The user described no pain, so there is nothing to build the entry from. Its reason is composed, and belongs in a question.

## Checks

- `9.6` (reply): The documentation written in this run (the new document, or the edits to the original when there is no new document) states that the generated files moved from the worker's local disk to an S3 bucket
- `9.7` (reply): The documentation written in this run gives the user's reason: a second worker was added and the download reached the worker that did not have the file, returning 404
- `9.8` (reply): At least one of these gaps is asked of the user or recorded as an open question, in the reply or in the documentation: what got worse with S3, what happens to the 7-day retention or its cleanup cron, who or what serves the download now
- `9.9` (reply): The reply and the text written in this run are in Portuguese
- `9.10` (invention): Neither the reply nor any text written in this run asserts, as a fact about the team or the system, a cost, retention policy, credential or access setup, download mechanism or URL scheme, metric, date of the change, outcome, or alternative that neither the user's message nor the original document established. Restating what the original document says, attributed to it, is not an invention; questions and entries listed as open questions are not assertions
- `9.11` (invention): No text written in this run states as fact who or what serves the download after the change (for example that any worker serves it, or that the endpoint reads the file from the bucket). Asking it, or listing it as an open question, is not stating it
- `9.12` (invention): If the text written in this run lists a 'do nothing' or keep-as-is alternative, the reason given for discarding it contains only what the user's message said (a second worker, the download reaching the worker without the file, the 404). The check is met when there is no such entry
