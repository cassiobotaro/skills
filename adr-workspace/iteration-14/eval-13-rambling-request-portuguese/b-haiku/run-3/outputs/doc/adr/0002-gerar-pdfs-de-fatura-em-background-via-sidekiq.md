# 2. Gerar PDFs de fatura em background via Sidekiq

Date: 2026-11-20

## Status

Accepted

## Context

Hoje o PDF da fatura é gerado dentro da própria request web, no momento em que o cliente clica em baixar. Em outubro, a página de faturamento deu timeout em três incidentes. Em todos eles, um cliente grande, com cerca de 4 mil itens de linha, pediu um ano de faturas, e a request atingiu o limite de 30 segundos do load balancer. O time de suporte contabilizou 41 tickets sobre o problema naquele mês.

Subir o timeout para 120 segundos foi considerado e rejeitado: isso apenas empurra o problema para frente e mantém um web worker ocupado durante toda a geração. Uma API de PDF de terceiros também foi considerada e rejeitada, porque o jurídico não aceita que dados de fatura saiam da nossa infraestrutura.

Já existe um Sidekiq em execução, usado para o envio de e-mails, e a fila dele é compartilhada.

## Decision

Vamos tirar a geração do PDF da request web e executá-la em background, como um job no Sidekiq que já existe. Quando o arquivo estiver pronto, ele será colocado no bucket de documentos, e o cliente receberá um e-mail com o link para acessá-lo.

Não manteremos um caminho de download imediato. Todas as faturas, inclusive as pequenas, passam pelo mesmo fluxo, para não termos dois caminhos de código.

## Consequences

O download imediato deixa de existir. Até mesmo uma fatura pequena passa a ser entregue por link enviado por e-mail, depois que o job terminar. Essa troca foi aceita pelo time.

A geração deixa de ocupar um web worker e deixa de depender do limite de 30 segundos do load balancer para faturas grandes.

A fila do Sidekiq é compartilhada com o envio de e-mails. Se o volume de jobs de PDF crescer, o time de e-mails sentirá o impacto, e esse risco é conhecido por eles.

A geração continua dentro da nossa infraestrutura, o que atende à restrição do jurídico.
