I wrote the whole lifecycle to `docs/order-lifecycle.md` as **five diagrams** instead of one — the full saga is ~40 messages and 13 participants, which renders as an unreadable wall. The split is by phase, with the same participant ids/labels everywhere and explicit "continues in diagram N" notes at the seams. All five are validated (rendered by the Mermaid MCP server) and use only safe-core syntax, so GitHub renders them as-is.

## 0. Overview — <https://l.mermaid.ai/Snxf1b>

Coarse view of the whole saga; each hop is expanded below.

```mermaid
sequenceDiagram
    autonumber
    actor cust as Customer
    participant app as Mobile App
    participant ord as Order Service
    participant rest as Restaurant Service
    participant crs as Courier Service
    participant notif as Notification Service

    cust->>app: Place order
    app->>ord: Create + pay order (diagram 1)
    ord-)rest: order.paid (diagram 2)
    rest-)crs: order.accepted (diagram 3)
    crs-)notif: order.picked_up / order.delivered (diagram 4)
    notif-)cust: Push notification at each stage
```

## 1. Placement and payment — <https://l.mermaid.ai/PofgdN>

Steps 1-7 go from the tap in the app to the Stripe authorization. Step 8-9 approved continues into diagram 2; steps 10-15 are the declined branch (`FAILED` + error in the app).

```mermaid
sequenceDiagram
    autonumber
    actor cust as Customer
    participant app as Mobile App
    participant gw as API Gateway
    participant ord as Order Service
    participant db as Order Postgres
    participant pay as Payment Service
    participant stripe as Stripe

    cust->>app: Place order
    app->>gw: POST /orders
    gw->>+ord: POST /orders
    ord->>db: INSERT order (status = PENDING)
    db-->>ord: order id
    ord->>+pay: POST /payments
    pay->>+stripe: Authorize card
    alt Card approved
        stripe-->>pay: Approved
        pay-->>ord: Approved
        Note over ord,pay: Continues in diagram 2 —<br/>the Order Service publishes order.paid
    else Card declined
        stripe-->>pay: Declined
        pay-->>ord: Declined
        ord->>db: UPDATE order status = FAILED
        ord-->>gw: Payment declined
        gw-->>app: Payment declined
        app-->>cust: Show payment error
    end
    deactivate stripe
    deactivate pay
    deactivate ord
```

## 2. Restaurant acceptance — <https://l.mermaid.ai/pavq4I>

Steps 1-3 deliver `order.paid` to the tablet. Accept (4-5) emits `order.accepted` and continues into diagram 3; reject (6-11) refunds through the Payment Service, sets `CANCELLED` and emits `order.cancelled`.

```mermaid
sequenceDiagram
    autonumber
    participant ord as Order Service
    participant db as Order Postgres
    participant pay as Payment Service
    participant kafka as Kafka
    participant rest as Restaurant Service
    actor rst as Restaurant (tablet)

    ord-)kafka: order.paid
    kafka-)rest: order.paid
    rest->>rst: Push order to the tablet
    alt Restaurant accepts
        rst-->>rest: Accept
        rest-)kafka: order.accepted
        Note over rest,kafka: Continues in diagram 3 —<br/>the Courier Service consumes order.accepted
    else Restaurant rejects
        rst-->>rest: Reject
        rest->>+pay: Refund the payment
        pay-->>-rest: Refunded
        rest->>ord: Order rejected
        ord->>db: UPDATE order status = CANCELLED
        ord-)kafka: order.cancelled
        Note over ord,kafka: The customer is notified of the cancellation<br/>through the Notification Service (diagram 4)
    end
```

## 3. Courier assignment and delivery — <https://l.mermaid.ai/IrGSak>

Steps 3-8 are the offer loop: nearest courier, offer, decline retries with the next one, accept assigns and emits `order.courier_assigned`. Steps 9-12 are pickup and delivery with their status events.

```mermaid
sequenceDiagram
    autonumber
    participant kafka as Kafka
    participant rest as Restaurant Service
    participant crs as Courier Service
    actor cour as Courier

    rest-)kafka: order.accepted
    kafka-)crs: order.accepted
    loop Until a courier accepts
        crs->>crs: Find the nearest available courier
        crs->>cour: Offer the job
        alt Courier declines
            cour-->>crs: Decline
            Note over crs,cour: Retry with the next nearest courier
        else Courier accepts
            cour-->>crs: Accept
            crs->>crs: Assign the courier to the order
            crs-)kafka: order.courier_assigned
        end
    end
    cour->>crs: Picked up the order
    crs-)kafka: order.picked_up
    cour->>crs: Delivered the order
    crs-)kafka: order.delivered
```

## 4. Notification fan-out — <https://l.mermaid.ai/DSjTYE>

Drawn once as a loop because the shape is identical for all five stages.

```mermaid
sequenceDiagram
    autonumber
    participant kafka as Kafka
    participant notif as Notification Service
    participant app as Mobile App
    actor cust as Customer

    loop For each order.* event
        kafka-)notif: order.paid / order.accepted /<br/>order.courier_assigned /<br/>order.picked_up / order.delivered
        notif-)app: Push notification
        app-)cust: Show the notification
    end
```

## Two things I filled in — check them

- **Push delivery mechanism.** You said the customer gets a push notification at each stage but not how it reaches the device, so diagram 4 shows Notification Service → Mobile App → Customer. If there is an APNs/FCM (or similar) hop in between, tell me and I will add it.
- **Cancellation notice.** You said "order CANCELLED, customer notified" without naming the event, so I drew the Order Service publishing `order.cancelled`, consumed by the Notification Service like the other `order.*` events. If the cancellation notice goes out some other way, that arrow should change.

## Deliberately not drawn (you did not describe them)

Payment/Stripe timeouts, Kafka consumer retries or DLQs, an offer timeout when a courier neither accepts nor declines, and the exhaustion case where every courier declines. Say what should happen in any of those and I will add the branch — I did not want to invent failure handling.

Notes are conceptual: you gave endpoints (`POST /orders`, `POST /payments`) and status names, but no headers or payload fields, so I did not put any in.
