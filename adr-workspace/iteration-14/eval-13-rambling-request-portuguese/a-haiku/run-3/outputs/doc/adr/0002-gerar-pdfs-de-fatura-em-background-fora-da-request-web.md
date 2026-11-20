# 2. Gerar PDFs de fatura em background, fora da request web

Date: 2026-11-20

## Status

Accepted

## Context

Hoje o PDF da fatura é gerado dentro da própria request web, no momento em que o cliente clica em baixar. Em outubro, a página de faturamento deu timeout três vezes: um cliente grande, com cerca de 4 mil itens de linha, pediu um ano de faturas e a request bateu no limite de 30 segundos do load balancer. Naquele mês, o suporte contou 41 tickets sobre o problema.

Duas alternativas foram consideradas e descartadas. Subir o timeout do load balancer para 120 segundos foi descartado porque apenas empurra o problema para frente e mantém um web worker preso durante toda a geração. Uma API de PDF de terceiros foi descartada porque o jurídico não aceita que dados de fatura saiam da infraestrutura própria.

O projeto já roda um Sidekiq para o envio de e-mails, e essa fila é compartilhada com o time de e-mail.

## Decision

Vamos tirar a geração do PDF da request web e executá-la em background, pelo Sidekiq que já existe. Quando o arquivo estiver pronto, ele será colocado no bucket de documentos, e o cliente receberá um e-mail com o link para baixá-lo.

Teremos um único caminho de código para gerar faturas, mesmo para faturas pequenas, em vez de manter dois caminhos.

## Consequences

O download imediato deixa de existir, inclusive para faturas pequenas. O cliente passa a esperar o e-mail com o link para obter a fatura. A equipe aceitou esse custo.

Em troca, há um único caminho de código para a geração de faturas, o que evita manter dois fluxos.

A fila do Sidekiq é compartilhada com os e-mails. Um volume grande de geração de PDFs pode atrasar o envio dos e-mails, e o time de e-mail sente esse impacto. O time de e-mail está ciente dessa dependência.
