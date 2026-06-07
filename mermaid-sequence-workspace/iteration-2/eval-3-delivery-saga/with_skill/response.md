Here is the food delivery order lifecycle documented as Mermaid sequence diagrams. The flow is large (8 services plus the customer, ~30+ interactions, multiple failure branches), so I split it into one overview plus four phase diagrams rather than one wall of arrows. Participant ids and labels are identical across every diagram, so they read as one set. All blocks paste directly into a GitHub wiki — GitHub renders ```mermaid``` natively.

> Validation note: the connected Mermaid MCP server returned transport-level errors on every attempt, and mermaid-cli is installed here (v11.15.0) but cannot render (no Chrome — "Could not find Chrome", an environment problem, not a syntax one). So these blocks were **not rendered/validated in this environment**. They use only safe-core Mermaid syntax that GitHub and GitLab support; to preview or edit, paste any block into <https://mermaid.live>.

## 1. Overview — end-to-end happy path

A zoomed-out view of the whole lifecycle. Each phase below drills into one segment of this diagram and adds its failure branch. Kafka topics are shown as async (open-arrow) messages; the consuming service is named on the publish.

```mermaid
sequenceDiagram
    autonumber
    actor C as Customer
    participant App as Mobile App
    participant GW as API Gateway
    participant OS as Order Service
    participant PS as Payment Service
    participant RS as Restaurant Service
    participant CS as Courier Service
    participant NS as Notification Service

    C->>App: Place order
    App->>GW: POST /orders
    GW->>OS: POST /orders
    Note over OS: Persist order as PENDING (Postgres)
    OS->>PS: POST /payments
    Note over OS,PS: Payment Service authorizes the card with Stripe
    PS-->>OS: approved
    Note over OS: Order PAID
    OS-)RS: publish order.paid (Kafka)
    OS-)NS: order.paid
    NS-)C: push "Order paid"

    Note over RS: Restaurant accepts on tablet -> ACCEPTED
    RS-)CS: publish order.accepted (Kafka)
    RS-)NS: order.accepted
    NS-)C: push "Restaurant accepted"

    Note over CS: Offer & assign nearest courier -> ASSIGNED
    CS-)NS: order.courier_assigned
    NS-)C: push "Courier assigned"

    Note over CS: Courier picks up -> PICKED_UP
    CS-)NS: order.picked_up
    NS-)C: push "Picked up"

    Note over CS: Courier delivers -> DELIVERED
    CS-)NS: order.delivered
    NS-)C: push "Delivered"
```

## 2. Phase 1 — order placement & payment (with the declined branch)

From the tap in the app through card authorization. The `alt` covers both Stripe outcomes: approved continues the saga; declined ends it as FAILED.

```mermaid
sequenceDiagram
    autonumber
    actor C as Customer
    participant App as Mobile App
    participant GW as API Gateway
    participant OS as Order Service
    participant DB as Order Postgres
    participant PS as Payment Service
    participant Stripe as Stripe
    participant K as Kafka

    C->>App: Place order
    App->>GW: POST /orders
    GW->>+OS: POST /orders
    OS->>DB: INSERT order (status = PENDING)
    DB-->>OS: ok
    OS->>+PS: POST /payments
    Note over OS,PS: { "order_id": "...", "amount": "...", "card": "..." }
    PS->>Stripe: authorize card
    Stripe-->>PS: auth result
    alt card approved
        PS-->>OS: approved
        OS->>DB: UPDATE order (status = PAID)
        OS-)K: publish order.paid
        OS-->>GW: 201 Created
        GW-->>App: 201 Created
        App-->>C: Order confirmed
    else card declined
        PS-->>OS: declined
        OS->>DB: UPDATE order (status = FAILED)
        OS-->>GW: 402 Payment Required
        GW-->>App: 402 Payment Required
        App-->>C: Show payment error
    end
    deactivate PS
    deactivate OS
```

## 3. Phase 2 — restaurant accept / reject (with the refund + cancel branch)

Continues from step "publish order.paid" above. The Restaurant Service consumes `order.paid`, pushes the order to the tablet, and the restaurant either accepts (saga continues to the courier phase) or rejects (refund via the Payment Service, order CANCELLED, customer notified).

```mermaid
sequenceDiagram
    autonumber
    actor C as Customer
    actor R as Restaurant
    participant K as Kafka
    participant RS as Restaurant Service
    participant Tab as Restaurant Tablet
    participant OS as Order Service
    participant PS as Payment Service
    participant NS as Notification Service

    K-)RS: consume order.paid
    RS->>Tab: push new order
    Tab->>R: show order
    alt restaurant accepts
        R->>Tab: Accept
        Tab->>RS: accept
        Note over RS: Order ACCEPTED
        RS-)K: publish order.accepted
    else restaurant rejects
        R->>Tab: Reject
        Tab->>RS: reject
        RS->>PS: POST /refunds
        Note over RS,PS: refund the Stripe authorization
        PS-->>RS: refunded
        RS->>OS: mark order CANCELLED
        OS-->>RS: ok
        RS-)K: publish order.cancelled
        K-)NS: consume order.cancelled
        NS-)C: push "Order cancelled & refunded"
    end
```

## 4. Phase 3 — courier assignment & delivery (with the courier-declines retry loop)

Continues from `order.accepted`. The Courier Service finds the nearest available courier and offers the job; a courier can decline, so it loops to the next-nearest until one accepts. After assignment the courier picks up and delivers, and the service publishes a status event at each transition.

```mermaid
sequenceDiagram
    autonumber
    actor Co as Courier
    participant K as Kafka
    participant CS as Courier Service
    participant OS as Order Service

    K-)CS: consume order.accepted
    loop until a courier accepts
        CS->>CS: find nearest available courier
        CS->>Co: offer job
        alt courier accepts
            Co-->>CS: accept
        else courier declines
            Co-->>CS: decline
            Note over CS: retry with next-nearest courier
        end
    end
    CS->>OS: assign courier
    OS-->>CS: ok
    Note over CS: Courier ASSIGNED
    CS-)K: publish order.courier_assigned

    Co->>CS: mark PICKED_UP
    Note over CS: Order PICKED_UP
    CS-)K: publish order.picked_up

    Co->>CS: mark DELIVERED
    Note over CS: Order DELIVERED
    CS-)K: publish order.delivered
```

## 5. Phase 4 — notifications (cross-cutting)

The Notification Service consumes every `order.*` event and sends one push to the customer per stage. This is the fan-in that the other diagrams reference; shown once here instead of repeating the push on every phase.

```mermaid
sequenceDiagram
    autonumber
    actor C as Customer
    participant K as Kafka
    participant NS as Notification Service
    participant Push as Push Provider

    Note over K,NS: NS subscribes to order.* (paid, accepted, courier_assigned, picked_up, delivered, cancelled)

    K-)NS: order.paid
    NS->>Push: send push
    Push-)C: "Order paid"

    K-)NS: order.accepted
    NS->>Push: send push
    Push-)C: "Restaurant accepted"

    K-)NS: order.courier_assigned
    NS->>Push: send push
    Push-)C: "Courier assigned"

    K-)NS: order.picked_up
    NS->>Push: send push
    Push-)C: "Picked up"

    K-)NS: order.delivered
    NS->>Push: send push
    Push-)C: "Delivered"

    opt order was cancelled
        K-)NS: order.cancelled
        NS->>Push: send push
        Push-)C: "Order cancelled & refunded"
    end
```

### Reading guide

- **Diagram 1** is the map; diagrams 2-5 are the territory. Order status moves PENDING -> PAID -> ACCEPTED -> ASSIGNED -> PICKED_UP -> DELIVERED on the happy path, with FAILED (declined payment) and CANCELLED (restaurant reject) as the two terminal failure branches you called out.
- **Failure branches**, all drawn: payment declined -> FAILED + error to the app (diagram 2); restaurant rejects -> refund + CANCELLED + notify (diagram 3); courier declines -> retry the next-nearest courier in a loop (diagram 4).
- **Plumbing I had to choose** (flagged so you can correct it): the customer-facing pushes go through a generic "Push Provider" because you didn't name one (APNs/FCM/etc.); the gateway returns `201`/`402` to the app on the synchronous order call; and topic names like `order.courier_assigned` / `order.cancelled` follow your `order.*` convention but were not given verbatim. Everything else — services, the POST /orders and POST /payments calls, Stripe authorization, the Kafka hand-offs, and the status transitions — comes straight from your description.
