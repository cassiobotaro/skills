# 2. Gerar PDFs de fatura em background

Date: 2026-11-20

## Status

Accepted

## Context

Hoje o PDF da fatura é gerado dentro da própria requisição web, no momento em que o cliente clica em baixar. Em outubro tivemos três incidentes em que a página de faturamento deu timeout: um cliente grande, com cerca de 4 mil itens de linha, pediu um ano de faturas e a requisição atingiu o limite de 30 segundos do load balancer. Naquele mês, o suporte registrou 41 tickets sobre o problema.

Duas alternativas foram consideradas e descartadas. Aumentar o timeout para 120 segundos empurra o problema para frente e mantém um web worker preso durante toda a geração. Usar uma API de PDF de terceiros foi descartado porque o jurídico não aceita que dados de fatura saiam da nossa infraestrutura.

## Decision

Vamos tirar a geração de PDF da requisição web e executá-la como job em background no Sidekiq que já existe para os e-mails. O arquivo gerado será gravado no bucket de documentos, e o cliente receberá um e-mail com o link quando o arquivo estiver pronto.

## Consequences

O download deixa de ser imediato, inclusive para faturas pequenas: o cliente passa a esperar o e-mail com o link.

Teremos um único caminho de código para gerar o PDF, em vez de um caminho síncrono para faturas pequenas e outro assíncrono para faturas grandes.

A geração sai da requisição web, então a rota de faturamento deixa de depender do limite de 30 segundos e deixa de prender web workers durante a geração.

A fila do Sidekiq é compartilhada com o envio de e-mails. Um volume alto de geração de PDFs pode atrasar esses e-mails, e o time de e-mail está ciente desse risco.

Os dados de fatura continuam dentro da nossa infraestrutura, como exige o jurídico.
