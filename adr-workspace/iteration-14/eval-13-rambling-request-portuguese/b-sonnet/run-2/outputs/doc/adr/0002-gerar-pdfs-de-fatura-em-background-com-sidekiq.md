# 2. Gerar PDFs de fatura em background com Sidekiq

Date: 2026-11-20

## Status

Accepted

## Context

Hoje os PDFs de fatura são gerados dentro da própria request web, quando o cliente clica em baixar. Em outubro tivemos três incidentes em que a página de faturamento deu timeout: um cliente grande, com cerca de 4 mil itens de linha, pediu um ano de faturas e a request atingiu o limite de 30s do load balancer. O suporte registrou 41 tickets sobre o problema naquele mês.

Duas alternativas foram discutidas na sync de plataforma e descartadas. Aumentar o timeout para 120s apenas empurraria o problema e manteria um web worker ocupado durante toda a geração. Usar uma API de PDF de terceiros foi vetado pelo jurídico, que não quer dados de fatura saindo da nossa infraestrutura.

Já existe um Sidekiq em execução para o envio de e-mails.

## Decision

Vamos tirar a geração de PDF de fatura da request web e executá-la em background, por meio do Sidekiq. O arquivo gerado será colocado no bucket de documentos, e o cliente receberá um e-mail com o link de download quando o PDF estiver pronto.

## Consequences

O download deixa de ser imediato para todas as faturas, inclusive as pequenas. A equipe aceitou essa perda para não manter dois caminhos de código.

A fila do Sidekiq é compartilhada com o envio de e-mails. Se a geração de PDFs entupir a fila, o time de e-mail sentirá o efeito; esse risco é conhecido e foi aceito por todos.

A geração deixa de ocupar um web worker durante a request e deixa de estar sujeita ao limite de 30s do load balancer.
