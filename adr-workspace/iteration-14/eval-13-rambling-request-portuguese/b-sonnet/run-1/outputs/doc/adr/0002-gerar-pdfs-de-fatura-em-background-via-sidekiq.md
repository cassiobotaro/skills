# 2. Gerar PDFs de fatura em background via Sidekiq

Date: 2026-11-20

## Status

Accepted

## Context

Hoje o PDF da fatura é gerado dentro da própria request web, quando o cliente clica em baixar. Em outubro tivemos três incidentes em que a página de faturamento deu timeout: um cliente grande, com cerca de 4 mil itens de linha, pediu um ano de faturas e a request bateu no limite de 30s do load balancer. O suporte registrou 41 tickets sobre isso naquele mês.

Duas alternativas foram descartadas. Subir o timeout para 120s apenas empurra o problema e mantém um web worker preso durante toda a geração. Usar uma API de PDF de terceiros foi vetado pelo jurídico, que não quer dados de fatura saindo da nossa infraestrutura.

## Decision

Vamos tirar a geração do PDF da request e executá-la em background, por meio do Sidekiq que já roda para o envio de e-mails. O arquivo gerado será gravado no bucket de documentos e o cliente receberá um e-mail com o link quando estiver pronto.

## Consequences

Deixa de existir o download imediato, mesmo para faturas pequenas: o cliente sempre espera o e-mail com o link. A equipe aceitou essa perda porque não quer manter dois caminhos de código.

A fila do Sidekiq é compartilhada com os e-mails, então um acúmulo de geração de PDFs pode atrasar o time de e-mail. Esse time está ciente do risco.

A página de faturamento deixa de ficar presa a um web worker durante a geração e deixa de depender do limite de 30s do load balancer.
