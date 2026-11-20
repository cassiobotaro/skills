# 2. Gerar PDF de fatura em background via Sidekiq

Date: 2026-11-20

## Status

Accepted

## Context

A geração do PDF de fatura acontece dentro da própria request web, quando o cliente clica em baixar. Em outubro tivemos três incidentes em que a página de faturamento deu timeout: um cliente grande, com cerca de 4 mil itens de linha, pediu um ano de faturas e a request atingiu o limite de 30 segundos do load balancer. Naquele mês, o suporte contou 41 tickets sobre o problema.

Duas alternativas foram descartadas. Subir o timeout para 120 segundos só empurra o problema e mantém um web worker preso durante toda a geração. Uma API de PDF de terceiros não foi aceita pelo jurídico, que não quer dados de fatura saindo da nossa infraestrutura.

## Decision

Vamos tirar a geração de PDF da request web e fazê-la em background, usando o Sidekiq que já processa os e-mails. Quando o arquivo estiver pronto, ele é gravado no bucket de documentos e o cliente recebe um e-mail com o link para download.

Não manteremos o download imediato nem para faturas pequenas, para não termos dois caminhos de código.

## Consequences

O download imediato deixa de existir, inclusive para faturas pequenas: o cliente passa a esperar o e-mail com o link para baixar qualquer fatura.

Como a request web deixa de gerar o PDF, faturas grandes deixam de depender do limite de 30 segundos do load balancer.

Há um único caminho de código para gerar todas as faturas, sem manter dois fluxos.

Cada fatura gerada passa a ser guardada como arquivo no bucket de documentos.

A fila do Sidekiq é compartilhada com os e-mails. Um volume alto de geração de PDF pode atrasar o envio de e-mails. O time de e-mails está ciente desse risco.
