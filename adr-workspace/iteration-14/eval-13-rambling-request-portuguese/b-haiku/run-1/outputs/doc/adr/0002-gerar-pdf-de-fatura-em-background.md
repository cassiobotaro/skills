# 2. Gerar PDF de fatura em background

Date: 2026-11-20

## Status

Accepted

## Context

Hoje o PDF de cada fatura é gerado dentro da própria request web, no momento em que o cliente clica em baixar. Em outubro houve três incidentes de timeout na página de faturamento: um cliente grande, com cerca de 4 mil itens de linha, pediu um ano de faturas, e a request atingiu o limite de 30 segundos do load balancer. O suporte registrou 41 tickets sobre o problema naquele mês.

Aumentar o timeout para 120 segundos foi considerado e descartado: isso apenas empurra o problema para mais tarde e mantém um web worker preso durante toda a geração.

Uma API de PDF de terceiros também foi considerada e descartada, porque o jurídico não permite que dados de fatura saiam da infraestrutura própria.

A fila do Sidekiq já é usada para o envio de e-mails e é compartilhada entre os times.

## Decision

Vamos tirar a geração do PDF da request web e executá-la em background, pela fila do Sidekiq que já processa os e-mails. Quando o arquivo estiver pronto, ele é gravado no bucket de documentos, e o cliente recebe um e-mail com o link para baixá-lo.

## Consequences

O download imediato deixa de existir, inclusive para faturas pequenas. Aceitamos isso para manter um único caminho de código, em vez de dois.

O cliente passa a depender do e-mail para obter a fatura: o arquivo só fica disponível depois que a geração termina e o e-mail é enviado.

A fila do Sidekiq é compartilhada com o envio de e-mails. Uma carga grande de geração de PDFs pode atrasar esses e-mails. O time de e-mails está ciente desse risco.

Os PDFs passam a ser armazenados no bucket de documentos.

Os dados de fatura continuam dentro da infraestrutura própria, como o jurídico exige.
