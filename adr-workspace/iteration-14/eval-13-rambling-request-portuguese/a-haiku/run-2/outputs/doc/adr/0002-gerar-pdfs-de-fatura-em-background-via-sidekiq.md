# 2. Gerar PDFs de fatura em background via Sidekiq

Date: 2026-11-20

## Status

Accepted

## Context

Hoje o PDF da fatura é gerado dentro da própria request web, no momento em que o cliente clica em baixar. Em outubro, houve três incidentes em que a página de faturamento sofreu timeout: um cliente grande, com cerca de 4 mil itens de linha, pediu as faturas de um ano inteiro, e a request atingiu o limite de 30 segundos do load balancer. O suporte registrou 41 tickets sobre o problema naquele mês.

Duas alternativas foram consideradas e descartadas. Aumentar o timeout para 120 segundos só adia o problema e mantém um web worker ocupado durante toda a geração. Uma API de PDF de terceiros foi descartada porque o jurídico não permite que dados de fatura saiam da nossa infraestrutura.

A fila do Sidekiq já é usada para os e-mails e é compartilhada entre os dois usos.

## Decision

Vamos tirar a geração de PDF da request web e executá-la em background, como um job no Sidekiq que já existe. Quando o arquivo ficar pronto, ele é gravado no bucket de documentos e o cliente recebe um e-mail com o link para download.

Não manteremos o download síncrono em paralelo. Faturas pequenas também passarão pelo mesmo caminho assíncrono, para que exista um único caminho de código.

## Consequences

O download imediato deixa de existir, inclusive para faturas pequenas. O cliente passa a esperar um e-mail com o link para baixar o arquivo.

A geração de faturas grandes deixa de ficar sujeita ao limite de 30 segundos do load balancer, e o web worker deixa de ficar preso durante a geração.

Os dados de fatura continuam na nossa infraestrutura, como exige o jurídico.

A fila do Sidekiq é compartilhada com os e-mails. Um volume alto de geração de PDF pode atrasar o envio de e-mails, e o time de e-mail está ciente desse risco.

O fluxo passa a depender de três partes funcionando: o job de geração, o bucket de documentos e o envio do e-mail com o link.
