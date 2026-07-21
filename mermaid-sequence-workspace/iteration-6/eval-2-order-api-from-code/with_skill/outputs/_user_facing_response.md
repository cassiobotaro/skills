Li os quatro arquivos (`main.py`, `payments.py`, `db.py`, `events.py`) e montei o diagrama só com o que está no código. Cole o bloco abaixo direto no README — GitHub e GitLab renderizam ` ```mermaid ` nativamente.

```mermaid
sequenceDiagram
    autonumber
    participant C as Cliente HTTP
    participant API as Order API (FastAPI)
    participant PG as PayGate
    participant DB as PostgreSQL
    participant MQ as RabbitMQ

    C->>+API: POST /orders
    Note over C,API: Body: { "customer_id": "...", "card_token": "...",<br/>"items": [ { "sku": "...", "quantity": (gt 0), "unit_price_cents": (gt 0) } ] }<br/>items exige no mínimo 1 item
    API->>API: total_cents = soma(unit_price_cents * quantity)
    API->>+PG: POST /v2/charges
    Note over API,PG: api.paygate.example.com<br/>Authorization: Bearer PAYGATE_API_KEY<br/>Idempotency-Key: uuid4 novo a cada chamada<br/>Body: { "card_token": "...", "amount": total_cents,<br/>"currency": "BRL", "capture": true }<br/>timeout de 10s
    alt pagamento aprovado (status = approved)
        PG-->>API: { "payment_id": "...", "status": "approved" }
        API->>+DB: INSERT INTO orders ... RETURNING id
        Note over API,DB: (customer_id, payment_id, total_cents, status)<br/>status gravado como 'confirmed'
        DB-->>-API: id
        API-)MQ: publish order.created
        Note over API,MQ: exchange "orders", routing_key "order.created"<br/>content_type: application/json<br/>Body: { "order_id": ..., "customer_id": "...", "total_cents": ... }<br/>a resposta da API não espera os consumidores
        API-->>C: 201 Created
        Note over C,API: { "order_id": ..., "status": "confirmed", "total_cents": ... }
    else pagamento recusado (status = declined)
        PG-->>API: { "payment_id": "...", "status": "declined" }
        API-->>C: 402 Payment Required
        Note over C,API: { "detail": "payment declined" }
    else PayGate responde 4xx/5xx ou estoura o timeout
        PG-->>API: erro HTTP
        Note over API,PG: raise_for_status() propaga e vira 500 na nossa API
        API-->>C: 500 Internal Server Error
    end
    deactivate PG
    deactivate API
```

Como ler: o cliente manda o `POST /orders` (1), a API calcula o total a partir dos itens (2) e cobra o cartão no PayGate (3). Aprovado, ela grava o pedido no Postgres com status `confirmed` (5), publica `order.created` no exchange `orders` do RabbitMQ sem esperar consumidor (7) e devolve `201` (9). Recusado, para no `402` (12). Se o PayGate falhar com 4xx/5xx ou estourar os 10s de timeout, o `raise_for_status()` sobe e o cliente recebe `500` (15).

Sobre a validação: o diagrama carrega detalhe interno de vocês (URL e chave do parceiro de pagamento, nomes de campos, tabela, exchange), então **não** mandei o código para o servidor Mermaid hospedado que está conectado aqui — ele renderiza remotamente. O `mmdc` local não está instalado e eu não instalei nada, então **o código não foi validado nesta máquina**. Pelo mesmo motivo não sugiro colar no mermaid.live: é o mesmo tipo de renderizador remoto. A checagem sem exposição é abrir o próprio README no preview do GitHub/GitLab do repositório — que já hospeda esse código. Se para vocês essa exposição for aceitável, é só falar que eu valido pelo servidor hospedado e devolvo o link de preview.

Duas coisas que deixei de fora de propósito, porque o código não as estabelece explicitamente: o `422` de validação do Pydantic (corpo inválido, `quantity`/`unit_price_cents` menores ou iguais a zero, lista de itens vazia) e qualquer falha na gravação no Postgres ou na publicação no RabbitMQ — hoje elas simplesmente sobem como erro. Se quiser, incluo esses caminhos, mas aí preciso que vocês me digam o que de fato acontece.
