# 2. Gerar PDFs de fatura em background

Date: 2026-11-20

## Status

Accepted

## Context

Os PDFs de fatura são gerados dentro da própria request web quando o cliente clica em baixar. Em outubro, isso causou três incidentes em que a página de faturamento deu timeout: um cliente grande, com cerca de 4 mil itens de linha, pediu um ano de faturas e a request bateu no limite de 30s do load balancer. O suporte registrou 41 tickets sobre o problema naquele mês.

Duas alternativas foram discutidas e descartadas na sync de plataforma. Subir o timeout para 120s apenas empurra o problema e mantém um web worker preso durante toda a geração. Usar uma API de PDF de terceiros foi vetado pelo jurídico, que não quer dados de fatura saindo da nossa infraestrutura.

Já existe um Sidekiq em operação para o envio de e-mails.

## Decision

Vamos tirar a geração de PDF da request web e executá-la em background, por meio do Sidekiq. O arquivo gerado será gravado no bucket de documentos e o cliente receberá um e-mail com o link quando ele estiver pronto.

## Consequences

O download imediato deixa de existir, inclusive para faturas pequenas. A equipe aceitou essa perda para não manter dois caminhos de código.

A fila do Sidekiq é compartilhada com o envio de e-mails. Se a geração de PDFs entupir a fila, o time de e-mail sentirá o impacto; esse risco é conhecido e foi aceito.

As requests de download deixam de depender do limite de 30s do load balancer e deixam de prender um web worker durante a geração.
