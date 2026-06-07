Li o código real em `evals/files/order-api` (`main.py`, `payments.py`, `db.py`, `events.py`) e montei o diagrama de sequência do `POST /orders` com os detalhes que estão de fato no código. Pode colar direto no README — GitHub e GitLab renderizam blocos ```mermaid``` nativamente.

```mermaid
sequenceDiagram
    autonumber
    participant C as Cliente
    participant API as Order API
    participant PG as PayGate
    participant DB as PostgreSQL
    participant MQ as RabbitMQ

    C->>+API: POST /orders
    Note over C,API: Content-Type: application/json<br/>{ "customer_id": "...", "card_token": "...",<br/>"items": [ { "sku", "quantity" (gt 0), "unit_price_cents" (gt 0) } ] }
    Note over API: total_cents = soma(unit_price_cents * quantity)

    API->>+PG: POST /v2/charges
    Note over API,PG: Authorization: Bearer (PAYGATE_API_KEY)<br/>Idempotency-Key: uuid v4 / timeout 10s<br/>{ "card_token", "amount": total_cents,<br/>"currency": "BRL", "capture": true }

    alt PayGate responde 2xx
        PG-->>-API: { "payment_id": "...", "status": "approved" | "declined" }
        alt status == "declined"
            API-->>C: 402 Payment Required
            Note over API,C: { "detail": "payment declined" }
        else status == "approved"
            API->>+DB: INSERT INTO orders (...) VALUES (...) RETURNING id
            Note over API,DB: status = 'confirmed'<br/>colunas: customer_id, payment_id, total_cents, status
            DB-->>-API: id (order_id)

            API-)MQ: publish order.created
            Note over API,MQ: exchange "orders" (topic) / routing_key "order.created"<br/>content_type: application/json / fire-and-forget<br/>{ "order_id", "customer_id", "total_cents" }

            API-->>C: 201 Created
            Note over API,C: { "order_id", "status": "confirmed", "total_cents" }
        end
    else PayGate responde 4xx/5xx (raise_for_status)
        PG--xAPI: erro HTTP
        API-->>C: 500 Internal Server Error
    end
    deactivate API
```

Passo a passo do fluxo:

1. O cliente chama `POST /orders` com `customer_id`, `card_token` e `items` (o Pydantic valida `quantity > 0`, `unit_price_cents > 0` e ao menos 1 item).
2. A API calcula `total_cents` somando `unit_price_cents * quantity` de cada item.
3-4. Chama o PayGate em `POST /v2/charges` (header `Authorization: Bearer` com `PAYGATE_API_KEY`, `Idempotency-Key` uuid v4, timeout de 10s) e recebe `payment_id` + `status`.
5-6. Se `status == "declined"`, a API responde `402` com `{"detail": "payment declined"}`.
7-9. Se aprovado, grava o pedido no Postgres (`INSERT ... RETURNING id`, com `status = 'confirmed'`) e recebe o `order_id`.
10. Publica `order.created` no RabbitMQ — exchange `orders` (topic), routing key `order.created` — em modo fire-and-forget (a resposta não espera os consumidores).
11. Responde `201 Created` com `{ order_id, status: "confirmed", total_cents }`.
12. Se o PayGate retornar 4xx/5xx, o `raise_for_status()` faz a exceção subir e o cliente recebe `500` (caminho que o próprio código documenta no docstring do `charge`).

Observação sobre validação: o servidor Mermaid MCP estava retornando erro de transporte ("Invalid Request" / JSON-RPC -32600) e o `mermaid-cli` local não consegue renderizar neste ambiente (falta o Chrome do puppeteer). Não instalei nada para contornar isso, então **o diagrama não foi validado aqui** — mas a sintaxe usa só o núcleo portável do Mermaid; cole no README e o GitHub/GitLab renderizam direto, ou jogue em <https://mermaid.live> para pré-visualizar e editar.
