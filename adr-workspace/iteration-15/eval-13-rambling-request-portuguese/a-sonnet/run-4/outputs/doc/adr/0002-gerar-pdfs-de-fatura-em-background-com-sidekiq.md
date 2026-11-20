# 2. Gerar PDFs de fatura em background com Sidekiq

Date: 2026-11-20

## Status

Accepted

## Context

Hoje os PDFs de fatura são gerados dentro da própria request web, quando o cliente clica em baixar. Em outubro tivemos três incidentes em que a página de faturamento deu timeout: um cliente grande, com cerca de 4 mil itens de linha, pediu um ano de faturas e a request atingiu o limite de 30 segundos do load balancer. O suporte contou 41 tickets sobre o problema naquele mês.

Duas alternativas foram discutidas na sync de plataforma e descartadas. Subir o timeout para 120 segundos apenas empurra o problema e mantém um web worker preso durante toda a geração. Usar uma API de PDF de terceiros foi vetado pelo jurídico, que não quer dados de fatura saindo da nossa infraestrutura.

Já existe um Sidekiq em operação para o envio de e-mails.

## Decision

Vamos tirar a geração de PDF de fatura da request web e executá-la em background, por meio do Sidekiq. O arquivo gerado será colocado no bucket de documentos, e o cliente receberá um e-mail com o link para baixá-lo quando estiver pronto.

## Consequences

O download deixa de ser imediato, mesmo para faturas pequenas. O time aceitou esse custo para não manter dois caminhos de código.

A request web deixa de ser limitada pelos 30 segundos do load balancer na geração do PDF, e os web workers não ficam mais presos durante ela.

A fila do Sidekiq é compartilhada com o envio de e-mails. Se a geração de PDFs entupir a fila, o time de e-mail sentirá o efeito; esse risco é conhecido por eles.
