Criei o ADR em `docs/adr/0001-usar-postgresql-no-servico-de-pedidos.md`. Ainda não fiz commit.

Ele tem status "Aceito" e a data de hoje (2026-11-22). Segue o formato Contexto, Decisão, Justificativa, Consequências e Alternativa descartada. Os motivos são os que você deu: transação ACID no fluxo de pedido, experiência do time e o RDS já pago. As desvantagens também são as que você citou: schema mais rígido e migrações como passo de deploy.

Na seção da alternativa descartada, escrevi que o time tem menos experiência com MongoDB e que não há infraestrutura contratada para ele. Isso é inferência minha a partir do que você disse sobre Postgres e RDS, então confirme se está certo. Se houver outro dado, como o prazo ou alguma consideração de custo, posso incluir.
