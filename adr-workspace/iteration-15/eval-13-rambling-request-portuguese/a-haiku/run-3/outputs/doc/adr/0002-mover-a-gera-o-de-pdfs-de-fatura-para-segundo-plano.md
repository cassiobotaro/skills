# 2. Mover a geração de PDFs de fatura para segundo plano

Date: 2026-11-20

## Status

Accepted

## Context

Hoje o PDF da fatura é gerado dentro da própria requisição web, no momento em que o cliente clica em baixar. Em outubro, tivemos três incidentes de timeout na página de faturamento: um cliente grande, com cerca de 4 mil itens de linha, pediu um ano de faturas, e a requisição atingiu o limite de 30 segundos do load balancer. Naquele mês, o suporte registrou 41 tickets sobre o problema.

Duas alternativas foram consideradas e descartadas. Aumentar o timeout para 120 segundos só adia o problema e mantém um web worker preso durante toda a geração. Uma API de PDF de terceiros foi descartada porque o jurídico não permite que dados de fatura saiam da nossa infraestrutura.

O projeto já executa um Sidekiq para o envio de e-mails, e essa fila é compartilhada com o time de e-mail.

## Decision

Vamos tirar a geração do PDF da requisição web e executá-la em background, pelo Sidekiq que já existe. O arquivo gerado será gravado no bucket de documentos, e o cliente receberá um e-mail com o link quando o arquivo estiver pronto.

## Consequences

O download imediato deixa de existir, inclusive para faturas pequenas. Aceitamos isso para não manter dois caminhos de código: todas as faturas passam pelo mesmo fluxo, e o cliente passa a obter o arquivo pelo link enviado por e-mail.

A requisição web deixa de gerar o PDF, então deixa de segurar um web worker durante a geração e deixa de depender do limite de 30 segundos do load balancer.

A fila do Sidekiq é compartilhada com os e-mails. Um volume alto de geração de PDFs pode atrasar o envio de e-mails. O time de e-mail conhece esse risco e o aceitou.
