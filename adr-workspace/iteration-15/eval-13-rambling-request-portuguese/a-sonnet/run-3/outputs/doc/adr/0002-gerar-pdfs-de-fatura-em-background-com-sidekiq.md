# 2. Gerar PDFs de fatura em background com Sidekiq

Date: 2026-11-20

## Status

Accepted

## Context

Hoje o PDF da fatura é gerado dentro da própria request web, quando o cliente clica em baixar. Em outubro, isso causou três incidentes em que a página de faturamento deu timeout: um cliente grande, com cerca de 4 mil itens de linha, pediu um ano de faturas e a request atingiu o limite de 30 segundos do load balancer. Naquele mês o suporte contou 41 tickets sobre o problema.

Duas alternativas foram discutidas e descartadas. Aumentar o timeout para 120 segundos apenas empurraria o problema e manteria um web worker ocupado durante todo o tempo da geração. Usar uma API de PDF de terceiros foi descartado porque o jurídico não quer dados de fatura saindo da nossa infraestrutura.

Já existe um Sidekiq em execução para o envio de e-mails.

## Decision

Vamos tirar a geração de PDF da request web e executá-la em background, por meio do Sidekiq. O arquivo gerado será gravado no bucket de documentos, e o cliente receberá um e-mail com o link quando o PDF estiver pronto.

## Consequences

O download imediato deixa de existir, inclusive para faturas pequenas. Aceitamos isso porque não queremos manter dois caminhos de código. Todos os envolvidos concordaram com essa desvantagem.

A request web deixa de depender do limite de 30 segundos do load balancer para gerar o PDF, e a geração não prende mais um web worker.

A fila do Sidekiq é compartilhada com o envio de e-mails. Se a geração de PDFs entupir a fila, o time de e-mail sentirá o efeito, e eles estão cientes disso.
