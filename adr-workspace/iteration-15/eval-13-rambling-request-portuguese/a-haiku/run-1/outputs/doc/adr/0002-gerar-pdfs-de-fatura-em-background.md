# 2. Gerar PDFs de fatura em background

Date: 2026-11-20

## Status

Accepted

## Context

Hoje o PDF da fatura é gerado dentro da própria request web, no momento em que o cliente clica em baixar. Em outubro tivemos três incidentes em que a página de faturamento deu timeout: um cliente grande, com cerca de 4 mil itens de linha, pediu um ano de faturas e a request atingiu o limite de 30 segundos do load balancer. O suporte registrou 41 tickets sobre o problema naquele mês.

Subir o timeout para 120 segundos foi considerado e descartado, porque só adia o problema e mantém um web worker preso durante toda a geração. Uma API de PDF de terceiros também foi considerada e descartada, porque o jurídico não permite que dados de fatura saiam da nossa infraestrutura.

A fila do Sidekiq já é usada para os e-mails e é compartilhada entre os dois usos.

## Decision

Vamos tirar a geração do PDF da request e executá-la em background, pelo Sidekiq que já processa os e-mails. Quando o arquivo estiver pronto, ele será gravado no bucket de documentos, e o cliente receberá um e-mail com o link para baixá-lo.

## Consequences

O download passa a não ser mais imediato, inclusive para faturas pequenas. Aceitamos essa perda para não manter dois caminhos de código.

A fila do Sidekiq é compartilhada com os e-mails, e um volume alto de geração de PDFs pode atrasar o envio de e-mails. O time de e-mail sabe disso.

A geração deixa de depender do limite de timeout do load balancer, e o web worker não fica preso durante a geração do arquivo.
