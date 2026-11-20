# 2. Gerar PDFs de fatura em background com Sidekiq

Date: 2026-11-20

## Status

Accepted

## Context

Hoje os PDFs de fatura são gerados dentro da própria request web, quando o cliente clica em baixar. Em outubro tivemos três incidentes em que a página de faturamento deu timeout: um cliente grande, com cerca de 4 mil itens de linha, pediu um ano de faturas e a request atingiu o limite de 30s do load balancer. O suporte registrou 41 tickets sobre o problema naquele mês.

Duas alternativas foram discutidas na sync de plataforma e descartadas. Aumentar o timeout para 120s apenas empurraria o problema e manteria um web worker ocupado durante todo esse tempo. Usar uma API de PDF de terceiros foi rejeitado porque o jurídico não quer dados de fatura saindo da nossa infraestrutura.

Já existe um Sidekiq em operação para o envio de e-mails.

## Decision

Vamos tirar a geração de PDF de fatura da request web e executá-la em background, por meio do Sidekiq que já existe. O arquivo gerado será gravado no bucket de documentos, e o cliente receberá um e-mail com o link para download quando o PDF estiver pronto.

## Consequences

Acaba o download imediato, inclusive para faturas pequenas. Aceitamos essa perda de propósito, porque não queremos manter dois caminhos de código (síncrono e assíncrono). Todo cliente passa a esperar o e-mail com o link, mesmo quando a fatura é pequena.

A geração deixa de ocupar um web worker e deixa de depender do limite de 30s do load balancer.

A fila do Sidekiq é compartilhada com o envio de e-mails. Se a geração de PDFs entupir a fila, o time de e-mail sentirá o efeito. O time está ciente desse risco.

Os PDFs continuam dentro da nossa infraestrutura, sem enviar dados de fatura a terceiros.
