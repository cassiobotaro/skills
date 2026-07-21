Li os quatro arquivos (`main.py`, `payments.py`, `events.py`, `db.py`) e montei o diagrama só com o que está no código. Salvei a seção pronta para colar no README em `post-orders-sequence.md`; segue o conteúdo:

## Fluxo de criação de pedido (`POST /orders`)

```mermaid
sequenceDiagram
    autonumber
    participant C as Cliente HTTP
    participant API as Order API
    participant PG as PayGate
    participant DB as Postgres (orders)
    participant MQ as RabbitMQ (exchange orders)

    C->>+API: POST /orders
    Note over C,API: { "customer_id": "...", "card_token": "...",<br/>"items": [ { "sku": "...", "quantity": 1,<br/>"unit_price_cents": 1000 } ] }<br/>quantity e unit_price_cents (gt) 0, items com no mínimo 1 item
    Note over API: total_cents = soma(unit_price_cents * quantity)

    API->>+PG: POST /v2/charges
    Note over API,PG: Authorization: Bearer PAYGATE_API_KEY<br/>Idempotency-Key: uuid4()<br/>{ "card_token": "...", "amount": total_cents,<br/>"currency": "BRL", "capture": true }<br/>timeout 10s

    alt PayGate responde 2xx
        PG-->>API: { "payment_id": "...", "status": "approved" | "declined" }
    else PayGate responde 4xx/5xx
        PG-->>API: erro HTTP (raise_for_status)
        API-->>C: 500 Internal Server Error
    end
    deactivate PG

    alt status == "approved"
        API->>+DB: INSERT INTO orders (customer_id, payment_id, total_cents, status) VALUES (..., 'confirmed') RETURNING id
        DB-->>-API: id do pedido
        API-)MQ: publish order.created
        Note over API,MQ: exchange "orders" (topic), routing_key "order.created"<br/>content_type: application/json<br/>{ "order_id": 1, "customer_id": "...", "total_cents": 1000 }<br/>a resposta da API não espera os consumidores
        API-->>C: 201 Created
        Note over C,API: { "order_id": 1, "status": "confirmed", "total_cents": 1000 }
    else status == "declined"
        API-->>C: 402 Payment Required
        Note over C,API: { "detail": "payment declined" }
    end
    deactivate API
```

**Como ler:** o cliente envia o pedido (1); a API soma o total dos itens e cobra o cartão
no PayGate (3) com uma `Idempotency-Key` por requisição e timeout de 10s. Se o PayGate
devolver 4xx/5xx, o erro sobe e a API responde 500 (6). Com a cobrança aprovada, o
pedido é gravado no Postgres já com `status = 'confirmed'` (8), o evento `order.created`
é publicado no RabbitMQ sem que a resposta espere os consumidores (10) e o cliente
recebe 201 (11). Se o PayGate devolver `status: "declined"`, nada é gravado nem
publicado e a API responde 402 (13).

**Sobre validação:** o diagrama tem detalhe interno (endpoint do PayGate, header de
autorização, `Idempotency-Key`, campos do payload, colunas da tabela `orders`, exchange
e routing key do RabbitMQ), então evitei o servidor Mermaid MCP hospedado, que renderiza
remotamente. O `mermaid-cli` local não está instalado (e não instalei nada só para
validar), portanto **o código não foi validado aqui**. GitHub e GitLab renderizam blocos
` ```mermaid ` nativamente, e você pode colar o bloco em <https://mermaid.live> para
pré-visualizar e editar.

**Duas observações sobre o que ficou de fora / foi interpretado:**

- Erros de rede/timeout do lado do Postgres e do RabbitMQ não estão desenhados — o
  código não trata nenhum dos dois, e a exceção simplesmente sobe. Se quiser, dá para
  acrescentar um ramo mostrando que uma falha na publicação do evento derruba a resposta
  (hoje o `await publish_order_created(...)` acontece antes do `return`, ou seja: apesar
  de ser fire-and-forget para os consumidores, uma exceção ali ainda quebraria a
  requisição).
- A validação do Pydantic (422 quando `quantity`/`unit_price_cents` não são maiores que
  zero ou `items` vem vazio) também não está no diagrama, para não competir com o fluxo
  principal — falo se quiser que eu inclua.
