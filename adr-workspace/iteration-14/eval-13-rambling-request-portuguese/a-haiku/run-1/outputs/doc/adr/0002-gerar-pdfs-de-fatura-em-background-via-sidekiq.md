# 2. Gerar PDFs de fatura em background via Sidekiq

Date: 2026-11-20

## Status

Accepted

## Context

Hoje o PDF da fatura é gerado dentro da própria request web, no momento em que o cliente clica em baixar. Em outubro houve três incidentes de timeout na página de faturamento: um cliente grande, com cerca de 4 mil itens de linha, pediu um ano de faturas, e a request excedeu o limite de 30 segundos do load balancer. O suporte registrou 41 tickets sobre o problema naquele mês.

Aumentar o timeout para 120 segundos foi considerado e rejeitado, porque apenas empurra o problema para frente e mantém um web worker ocupado durante toda a geração. Uma API de PDF de terceiros também foi considerada e rejeitada pelo jurídico, que não permite que dados de fatura saiam da infraestrutura da empresa.

O projeto já tem um Sidekiq em execução para o envio de e-mails, e essa fila é compartilhada.

## Decision

Vamos tirar a geração do PDF da request web e executá-la em background, pelo Sidekiq que já processa os e-mails. Quando o arquivo estiver pronto, ele será gravado no bucket de documentos, e o cliente receberá um e-mail com o link para o arquivo.

## Consequences

O download deixa de ser imediato, inclusive para faturas pequenas. O time optou por um único caminho de código em vez de manter dois fluxos, e aceitou essa perda.

A fila do Sidekiq é compartilhada com os e-mails. Se ela for sobrecarregada pela geração de PDFs, o envio de e-mails será afetado, e o time de e-mail sabe disso.
