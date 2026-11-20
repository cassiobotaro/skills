# 2. Gerar PDFs de fatura em background com Sidekiq

Date: 2026-11-20

## Status

Accepted

## Context

Hoje o PDF da fatura é gerado dentro da própria request web, quando o cliente clica em baixar. Em outubro tivemos três incidentes em que a página de faturamento deu timeout: um cliente grande, com cerca de 4 mil itens de linha, pediu um ano de faturas e a request estourou o limite de 30s do load balancer. O suporte registrou 41 tickets sobre o problema naquele mês.

Duas alternativas foram discutidas e descartadas na sync de plataforma. Aumentar o timeout para 120s apenas empurra o problema e mantém um web worker preso durante toda a geração. Usar uma API de PDF de terceiros foi vetado pelo jurídico, que não aceita dados de fatura saindo da nossa infraestrutura.

Já existe um Sidekiq em operação para o envio de e-mails, e a fila dele é compartilhada.

## Decision

Vamos tirar a geração de PDF de fatura da request web e executá-la em background, por meio do Sidekiq existente. O arquivo gerado será gravado no bucket de documentos, e o cliente receberá um e-mail com o link para baixá-lo quando estiver pronto.

## Consequences

O download imediato deixa de existir, inclusive para faturas pequenas. O time aceitou essa perda para não manter dois caminhos de código.

A geração deixa de ocupar um web worker e deixa de estar sujeita ao limite de 30s do load balancer.

Como a fila do Sidekiq é compartilhada, um acúmulo de jobs de PDF pode atrasar os e-mails, e o time de e-mail vai sentir o efeito. Esse risco foi reconhecido pelo time.
