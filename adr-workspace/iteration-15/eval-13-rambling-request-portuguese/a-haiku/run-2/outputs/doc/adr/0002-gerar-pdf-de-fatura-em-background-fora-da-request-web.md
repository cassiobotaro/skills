# 2. Gerar PDF de fatura em background, fora da request web

Date: 2026-11-20

## Status

Accepted

## Context

Hoje o PDF da fatura é gerado dentro da própria request web, no momento em que o cliente clica em baixar. Em outubro tivemos três incidentes de timeout na página de faturamento: um cliente grande, com cerca de 4 mil itens de linha, pediu um ano de faturas, e a request ultrapassou o limite de 30 segundos do load balancer. O suporte registrou 41 tickets sobre o problema naquele mês.

Duas alternativas foram consideradas e descartadas. Aumentar o timeout para 120 segundos foi descartado porque só empurra o problema e mantém um web worker preso durante toda a geração. Uma API de PDF de terceiros foi descartada porque o jurídico não permite que dados de fatura saiam da nossa infraestrutura.

## Decision

Vamos tirar a geração do PDF da request web e executá-la em background, usando o Sidekiq que já processa os e-mails. Quando o arquivo fica pronto, ele é colocado no bucket de documentos e o cliente recebe um e-mail com o link para download.

## Consequences

O download imediato deixa de existir, inclusive para faturas pequenas. Aceitamos isso para não manter dois caminhos de código, um síncrono para faturas pequenas e outro assíncrono para as grandes.

A fila do Sidekiq é compartilhada com o envio de e-mails. Se a geração de PDFs sobrecarregar a fila, o envio de e-mails será afetado; o time de e-mail está ciente desse risco.

O cliente passa a depender do e-mail para obter a fatura, porque o link só chega depois que o arquivo está pronto.
