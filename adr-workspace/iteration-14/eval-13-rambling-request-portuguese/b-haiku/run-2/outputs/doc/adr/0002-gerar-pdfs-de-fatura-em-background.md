# 2. Gerar PDFs de fatura em background

Date: 2026-11-20

## Status

Accepted

## Context

Hoje o PDF da fatura é gerado dentro da própria requisição web, no momento em que o cliente clica em baixar. Em outubro, isso causou três incidentes de timeout na página de faturamento: um cliente grande, com cerca de 4 mil itens de linha, pediu um ano de faturas, e a requisição atingiu o limite de 30 segundos do load balancer. No mesmo mês, o suporte contou 41 tickets sobre o problema.

Elevar o timeout para 120 segundos foi considerado e descartado: isso só adia o problema e mantém um web worker ocupado durante toda a geração. Uma API de PDF de terceiros também foi considerada e descartada, porque o jurídico não permite que dados de fatura saiam da nossa infraestrutura.

## Decision

Vamos tirar a geração do PDF da requisição web e executá-la em background, usando o Sidekiq que já processa os e-mails. Quando o arquivo estiver pronto, ele será gravado no bucket de documentos e o cliente receberá um e-mail com o link para download. O download imediato deixa de existir para todas as faturas, inclusive as pequenas, porque não queremos manter dois caminhos de código.

## Consequences

O cliente deixa de baixar a fatura na hora, mesmo quando ela é pequena: ele passa a esperar o e-mail com o link para qualquer fatura. Essa desvantagem foi aceita.

A requisição web deixa de ficar presa à geração do PDF, e o web worker não fica mais ocupado por ela.

A fila do Sidekiq é compartilhada com o envio de e-mails. Uma geração grande de PDFs pode atrasar esses envios, e o time de e-mail sentirá o efeito se a fila for sobrecarregada. O time de e-mail está ciente disso.

Os PDFs gerados passam a ficar gravados no bucket de documentos.
