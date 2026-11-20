# 2. Gerar PDFs de fatura em background com Sidekiq

Date: 2026-11-20

## Status

Accepted

## Context

Hoje o PDF da fatura é gerado dentro da própria request web, quando o cliente clica em baixar. Em outubro tivemos três incidentes em que a página de faturamento deu timeout: um cliente grande, com cerca de 4 mil itens de linha, pediu um ano de faturas e a request atingiu o limite de 30s do load balancer. O suporte contou 41 tickets sobre o problema naquele mês.

Duas alternativas foram discutidas e descartadas na sync de plataforma. Subir o timeout para 120s apenas adia o problema e mantém um web worker preso durante toda a geração. Usar uma API de PDF de terceiros foi vetado pelo jurídico, que não quer dados de fatura saindo da nossa infraestrutura.

## Decision

Vamos tirar a geração de PDF da request web e executá-la em background, no Sidekiq que já roda para o envio de e-mails. O arquivo gerado será gravado no bucket de documentos, e o cliente receberá um e-mail com o link para baixá-lo quando estiver pronto.

## Consequences

Deixa de existir download imediato, mesmo para faturas pequenas: todo pedido passa a ser assíncrono e o cliente espera o e-mail. O time aceitou isso de propósito, para não manter dois caminhos de código.

A fila do Sidekiq é compartilhada com os e-mails. Se a geração de PDFs entupir a fila, o time de e-mail sentirá o efeito; esse risco é conhecido e foi aceito por todos.

A geração deixa de ocupar web workers e deixa de estar sujeita ao limite de 30s do load balancer, e os dados de fatura continuam dentro da nossa infraestrutura.
