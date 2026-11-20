# 2. Gerar PDFs de fatura em background via Sidekiq

Date: 2026-11-20

## Status

Accepted

## Context

Hoje os PDFs de fatura são gerados dentro da própria request web quando o cliente clica em baixar. Em outubro tivemos três incidentes em que a página de faturamento deu timeout: um cliente grande, com cerca de 4 mil itens de linha, pediu um ano de faturas e a request atingiu o limite de 30 segundos do load balancer. O suporte contou 41 tickets sobre o problema naquele mês.

Duas alternativas foram discutidas e descartadas. Subir o timeout para 120 segundos apenas empurra o problema e mantém um web worker preso durante toda a geração. Usar uma API de PDF de terceiros foi vetado pelo jurídico, que não quer dados de fatura saindo da nossa infraestrutura.

Já existe um Sidekiq em operação para o envio de e-mails.

## Decision

Vamos tirar a geração de PDF de fatura da request web e executá-la em background, em jobs do Sidekiq já existente. O arquivo gerado será colocado no bucket de documentos e o cliente receberá um e-mail com o link quando ele estiver pronto.

Isso vale para todas as faturas, inclusive as pequenas: não vamos manter um segundo caminho de código para download imediato.

## Consequences

Os timeouts da página de faturamento por geração de PDF deixam de depender do limite de 30 segundos do load balancer, e nenhum web worker fica preso durante a geração. Os dados de fatura continuam dentro da nossa infraestrutura.

Acaba o download na hora, mesmo para faturas pequenas. O cliente passa a esperar o e-mail com o link. O time aceitou essa perda para não manter dois caminhos de código.

A fila do Sidekiq é compartilhada com o envio de e-mails. Se a geração de PDFs entupir a fila, o time de e-mail sentirá o efeito; esse risco é conhecido e foi aceito pelos envolvidos.
