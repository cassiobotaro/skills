# 2. Gerar PDFs de fatura em background via Sidekiq

Date: 2026-11-20

## Status

Accepted

## Context

Hoje o PDF de fatura é gerado dentro da própria request web, quando o cliente clica em baixar. Em outubro tivemos três incidentes em que a página de faturamento deu timeout: um cliente grande, com cerca de 4 mil itens de linha, pediu um ano de faturas e a request atingiu o limite de 30 segundos do load balancer. O suporte contou 41 tickets sobre o problema naquele mês.

Duas alternativas foram discutidas na sync de plataforma e descartadas. Subir o timeout para 120 segundos apenas empurra o problema e mantém um web worker preso durante toda a geração. Usar uma API de PDF de terceiros não é aceitável porque o jurídico não quer dados de fatura fora da nossa infraestrutura.

Já existe um Sidekiq em execução para o envio de e-mails, e a fila dele é compartilhada.

## Decision

Vamos tirar a geração de PDF da request web e executá-la em background, por meio do Sidekiq existente. O arquivo gerado será colocado no bucket de documentos, e o cliente receberá um e-mail com o link quando ele estiver pronto.

Isso vale para todas as faturas, inclusive as pequenas: não manteremos um segundo caminho de código para download imediato.

## Consequences

O download na hora deixa de existir para todos os clientes, mesmo para faturas pequenas. O time aceitou essa perda para não manter dois caminhos de código.

Como a fila do Sidekiq é compartilhada com os e-mails, se a geração de PDFs a entupir, o time de e-mail sentirá o efeito. O time de e-mail está ciente desse risco.
