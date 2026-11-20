# 2. Gerar PDF de fatura em segundo plano

Date: 2026-11-20

## Status

Accepted

## Context

Hoje o PDF de fatura é gerado dentro da própria request web, quando o cliente clica em baixar. Em outubro, isso causou três incidentes em que a página de faturamento deu timeout: um cliente grande, com cerca de 4 mil itens de linha, pediu um ano de faturas e a request estourou o limite de 30 segundos do load balancer. O suporte registrou 41 tickets sobre o problema naquele mês.

Duas alternativas foram discutidas e descartadas. Aumentar o timeout para 120 segundos só empurraria o problema e manteria um web worker ocupado durante toda a geração. Usar uma API de PDF de terceiros foi rejeitado porque o jurídico não quer dados de fatura fora da nossa infraestrutura.

O Sidekiq já roda na infraestrutura para o envio de e-mails, e sua fila é compartilhada com o time de e-mail.

## Decision

Vamos tirar a geração do PDF de fatura da request web e executá-la em segundo plano, por meio do Sidekiq. O arquivo gerado será gravado no bucket de documentos, e o cliente receberá um e-mail com o link para baixá-lo quando estiver pronto.

Vamos usar esse caminho para todas as faturas, inclusive as pequenas, para não manter dois caminhos de código.

## Consequences

O download imediato deixa de existir, mesmo para faturas pequenas: o cliente passa a esperar o e-mail com o link. O time aceitou essa perda em troca de manter um único caminho de código.

A request web deixa de ser limitada pelo timeout de 30 segundos do load balancer e não prende mais um web worker durante a geração.

Os dados da fatura continuam dentro da nossa infraestrutura.

A fila do Sidekiq é compartilhada com o envio de e-mails. Se a geração de PDFs entupir a fila, o time de e-mail sentirá o efeito, e isso foi reconhecido pelo time.
