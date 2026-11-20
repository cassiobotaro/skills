# 2. Gerar PDFs de fatura em background com Sidekiq

Date: 2026-11-20

## Status

Accepted

## Context

Hoje o PDF da fatura é gerado dentro da própria request web, quando o cliente clica em baixar. Em outubro tivemos três incidentes em que a página de faturamento deu timeout: um cliente grande, com cerca de 4 mil itens de linha, pediu um ano de faturas e a request bateu no limite de 30 segundos do load balancer. O suporte contou 41 tickets sobre o problema naquele mês.

Duas alternativas foram discutidas e descartadas. Subir o timeout para 120 segundos só empurra o problema e mantém um web worker preso durante toda a geração. Usar uma API de PDF de terceiros exigiria que dados de fatura saíssem da nossa infraestrutura, o que o jurídico não aceita.

Já existe um Sidekiq em execução para o envio de e-mails, e a fila dele é compartilhada.

## Decision

Vamos tirar a geração de PDF de fatura da request web e executá-la em background, por meio do Sidekiq. O arquivo gerado será colocado no bucket de documentos, e o cliente receberá um e-mail com o link para baixá-lo quando estiver pronto.

Não vamos manter um caminho síncrono para faturas pequenas: haverá um único caminho de código.

## Consequences

A request de download deixa de depender do tempo de geração, então o limite de 30 segundos do load balancer deixa de ser um risco para faturas grandes, e nenhum web worker fica preso durante a geração.

Acaba o download imediato, mesmo para faturas pequenas: o cliente passa a esperar o e-mail com o link. Todos aceitaram essa perda para não termos dois caminhos de código.

Como a fila do Sidekiq é compartilhada, se a geração de PDFs entupir a fila o time de e-mail sentirá o efeito. O time está ciente desse risco.

A infraestrutura continua toda interna, sem enviar dados de fatura a terceiros.
