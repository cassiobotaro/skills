# 2. Gerar o PDF da fatura em background, fora da request web

Date: 2026-11-20

## Status

Accepted

## Context

Hoje o PDF da fatura é gerado dentro da própria request web, no momento em que o cliente clica em baixar. Em outubro, um cliente grande, com cerca de 4 mil itens de linha, pediu um ano de faturas e a request bateu no limite de 30 segundos do load balancer. Foram três incidentes de timeout na página de faturamento naquele mês, e o suporte contou 41 tickets sobre o problema.

Foram consideradas duas alternativas. Subir o timeout do load balancer para 120 segundos só adia o problema e mantém um web worker preso durante toda a geração. Usar uma API de PDF de terceiros foi descartado, porque o jurídico não aceita que dados de fatura saiam da nossa infraestrutura.

## Decision

Vamos tirar a geração do PDF da request web e executá-la em background, pela fila do Sidekiq que já processa os e-mails. Quando o arquivo estiver pronto, ele é gravado no bucket de documentos e o cliente recebe um e-mail com o link para baixá-lo.

## Consequences

O download deixa de ser imediato, inclusive para faturas pequenas: o cliente passa a esperar o e-mail com o link. Aceitamos essa perda para manter um único caminho de código, em vez de dois caminhos separados para faturas pequenas e grandes.

A página de faturamento deixa de depender do limite de 30 segundos do load balancer para gerar os PDFs.

A fila do Sidekiq é compartilhada com os e-mails. Se gerarmos PDFs em volume alto, o envio de e-mails pode ser atrasado, e o time de e-mail sentirá esse impacto. Esse risco é conhecido e aceito por eles.
