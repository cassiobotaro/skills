Criei o ADR em `docs/adr/0001-usar-postgresql-no-servico-de-pedidos.md`. Não fiz commit.

O repositório estava vazio, então escolhi eu o local `docs/adr/`, a numeração 0001 e um formato enxuto em português (Contexto, Decisão, Alternativas, Consequências). Se o time preferir outro padrão, é fácil ajustar.

O texto cobre só o que você me contou:
- **Motivos:** a transação ACID entre estoque, pagamento e pedido, a experiência do time com Postgres e o RDS que a empresa já paga.
- **Desvantagens:** o schema mais rígido e as migrações como passo de deploy.
- **Alternativa:** o MongoDB aparece como a opção descartada.

Coloquei o status como "Aceita" e a data como 2026-11-22 (hoje). Mude se a decisão foi tomada em outro dia ou ainda não foi formalizada.
