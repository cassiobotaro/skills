Here is the food delivery order lifecycle as a set of Mermaid sequence diagrams, ready to paste into the engineering wiki (GitHub renders these `mermaid` blocks natively). I split the flow into four diagrams because the whole lifecycle is well past what stays readable in one — participant ids and labels are identical across all four, so they read as one set. The first three cover the happy path plus the failure branches you described; the fourth is the cross-cutting Notification Service that consumes every `order.*` event.

## 1. Order placement and payment

The customer places the order; it flows through the gateway to the Order Service, which persists it as `PENDING` and authorizes the card via the Payment Service and Stripe. Approved orders become `PAID` and emit `order.paid` to Kafka; declined cards mark the order `FAILED` and the app shows the error (steps 16-22).

```mermaid
sequenceDiagram
    autonumber
    actor C as Customer
    participant App as Mobile App
    participant GW as API Gateway
    participant OS as Order Service
    participant PG as Order Postgres
    participant PS as Payment Service
    participant ST as Stripe
    participant K as Kafka

    C->>App: Place order
    App->>GW: POST /orders
    GW->>+OS: POST /orders
    OS->>PG: INSERT order (status=PENDING)
    PG-->>OS: order id
    OS->>+PS: POST /payments
    Note over OS,PS: authorize card for order total
    PS->>ST: Authorize card
    alt card approved
        ST-->>PS: approved
        PS-->>OS: approved
        OS->>PG: UPDATE order (status=PAID)
        OS-)K: publish order.paid
        OS-->>GW: 201 Created (PAID)
        GW-->>App: 201 Created
        App-->>C: Order confirmed
    else card declined
        ST-->>PS: declined
        PS-->>OS: declined
        OS->>PG: UPDATE order (status=FAILED)
        OS-->>GW: 402 Payment Required (FAILED)
        GW-->>App: 402 Payment Required
        App-->>C: Show payment error
    end
    deactivate PS
    deactivate OS
```

## 2. Restaurant acceptance

Continues from step 12 of diagram 1 (`order.paid` on Kafka). The Restaurant Service consumes it, pushes the order to the restaurant tablet, and waits for accept/reject. On reject it refunds via the Payment Service, marks the order `CANCELLED`, and notifies the customer; on accept it publishes `order.accepted`.

```mermaid
sequenceDiagram
    autonumber
    participant K as Kafka
    participant RS as Restaurant Service
    participant T as Restaurant Tablet
    participant OS as Order Service
    participant PG as Order Postgres
    participant PS as Payment Service
    participant ST as Stripe
    actor C as Customer

    K-)RS: consume order.paid
    RS->>+T: Push order to tablet
    Note over RS,T: restaurant reviews the order
    alt restaurant accepts
        T-->>RS: accepted
        RS-)K: publish order.accepted
    else restaurant rejects
        T-->>RS: rejected
        RS->>+PS: POST /payments/{id}/refund
        PS->>ST: Refund charge
        ST-->>PS: refunded
        PS-->>-RS: refunded
        RS->>OS: Mark order CANCELLED
        OS->>PG: UPDATE order (status=CANCELLED)
        RS-)K: publish order.cancelled
        Note over RS,C: customer notified via Notification Service (see diagram 4)
    end
    deactivate T
```

## 3. Courier assignment and delivery

Continues from the `order.accepted` event in diagram 2. The Courier Service consumes it, finds the nearest available courier, and offers the job — a courier may decline, so it loops to the next-nearest until one accepts. The assigned courier picks up and delivers, and the Courier Service publishes a status event at each transition.

```mermaid
sequenceDiagram
    autonumber
    participant K as Kafka
    participant CS as Courier Service
    actor CR as Courier

    K-)CS: consume order.accepted
    loop until a courier accepts
        CS->>CS: Find nearest available courier
        CS->>+CR: Offer job
        alt courier accepts
            CR-->>CS: accepted
            Note over CS,CR: exit loop with assigned courier
        else courier declines
            CR-->>CS: declined
            Note over CS,CR: retry with next-nearest courier
        end
        deactivate CR
    end
    CS->>CS: Assign order to courier
    CS-)K: publish order.courier_assigned

    CR->>CS: Mark PICKED_UP
    CS-)K: publish order.picked_up
    CR->>CS: Mark DELIVERED
    CS-)K: publish order.delivered
```

## 4. Customer notifications (cross-cutting)

The Notification Service subscribes to every `order.*` event published across diagrams 1-3 and sends the customer a push notification at each stage. This runs in parallel with the flows above rather than in sequence.

```mermaid
sequenceDiagram
    autonumber
    participant K as Kafka
    participant NS as Notification Service
    participant FCM as Push (FCM/APNs)
    actor C as Customer

    Note over K,NS: NS subscribes to order.* events
    K-)NS: order.paid
    NS->>FCM: Send push
    FCM-->>C: "Payment confirmed"
    K-)NS: order.accepted
    NS->>FCM: Send push
    FCM-->>C: "Restaurant accepted your order"
    K-)NS: order.courier_assigned
    NS->>FCM: Send push
    FCM-->>C: "A courier is assigned"
    K-)NS: order.picked_up
    NS->>FCM: Send push
    FCM-->>C: "Your order was picked up"
    K-)NS: order.delivered
    NS->>FCM: Send push
    FCM-->>C: "Your order was delivered"
```

---

**Validation:** I could not validate these here. The Mermaid MCP server returned a transport error on every call, and mermaid-cli is installed but cannot render in this environment (no Chrome for its headless browser). GitHub and GitLab render `mermaid` blocks natively, so they will display in the wiki as-is; to preview or tweak them yourself, paste any block into <https://mermaid.live>.

**Two mechanisms I chose where you stated the fact but not the plumbing**, flagged so you can correct them:
- The push-notification transport in diagram 4 is shown as a generic `Push (FCM/APNs)` participant — you said "push notification" but not the provider.
- The Kafka event names for the later stages (`order.cancelled`, `order.courier_assigned`, `order.picked_up`, `order.delivered`) follow the `order.*` convention you established for `order.paid` and `order.accepted`; rename them if your actual topics differ.

Everything else — endpoints, statuses (`PENDING`/`PAID`/`FAILED`/`CANCELLED`/`PICKED_UP`/`DELIVERED`), the decline/reject/refund branches, and the courier-decline retry loop — comes straight from your description.
