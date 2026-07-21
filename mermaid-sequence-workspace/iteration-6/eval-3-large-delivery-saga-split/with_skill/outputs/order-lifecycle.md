# Food delivery — order lifecycle

How an order moves from "Place order" in the mobile app to "Delivered", including the
payment-declined, restaurant-rejected and courier-declined branches.

The flow is split into one overview plus four phase diagrams — a single diagram would run
past 25 messages and 12 participants and stop being readable. Participant ids and labels
are identical across the whole set, and each phase says where it continues from.

---

## 1. Overview

Coarse view of the whole lifecycle. Each branch is drawn in detail in the diagrams below.

```mermaid
sequenceDiagram
    autonumber
    actor C as Customer
    participant M as Mobile App
    participant O as Order Service
    participant P as Payment Service
    participant R as Restaurant Service
    participant CO as Courier Service
    participant N as Notification Service

    C->>M: Place order
    M->>O: Create order (PENDING)
    O->>P: Authorize card
    alt card approved
        P-->>O: approved
        O-)R: order.paid
        alt restaurant accepts
            R-)CO: order.accepted
            CO->>CO: Assign courier, then PICKED_UP and DELIVERED
        else restaurant rejects
            R->>O: Order rejected
            O->>P: Refund
            O->>O: Mark order CANCELLED
        end
    else card declined
        P-->>O: declined
        O->>O: Mark order FAILED
        M-->>C: Show payment error
    end
    Note over O,CO: Every state change is published to Kafka as an order.* event
    N-)C: Push notification at each stage
```

---

## 2. Phase 1 — placing the order and paying

From the tap in the app to `order.paid` on Kafka, with the declined branch.

```mermaid
sequenceDiagram
    autonumber
    actor C as Customer
    participant M as Mobile App
    participant G as API Gateway
    participant O as Order Service
    participant DB as Order DB (Postgres)
    participant P as Payment Service
    participant S as Stripe
    participant K as Kafka

    C->>M: Place order
    M->>+G: Submit order
    G->>+O: POST /orders
    O->>DB: INSERT order
    Note over O,DB: The order is persisted as PENDING before payment is attempted
    DB-->>O: order id
    O->>+P: POST /payments
    P->>+S: Authorize card
    S-->>-P: approved or declined
    alt card approved
        P-->>O: approved
        O-)K: publish order.paid
        O-->>G: order accepted
        G-->>M: order accepted
        M-->>C: Show order placed
    else card declined
        P-->>O: declined
        O->>DB: UPDATE order status = FAILED
        O-->>G: payment declined
        G-->>M: payment declined
        M-->>C: Show payment error
    end
    deactivate P
    deactivate O
    deactivate G
```

---

## 3. Phase 2 — the restaurant accepts or rejects

Continues from step 10 of phase 1 (`order.paid` published).

```mermaid
sequenceDiagram
    autonumber
    participant K as Kafka
    participant R as Restaurant Service
    actor T as Restaurant<br/>(tablet)
    participant O as Order Service
    participant P as Payment Service

    K-)R: order.paid
    R->>T: Push order to the tablet
    alt restaurant accepts
        T-->>R: Accept
        R-)K: publish order.accepted
    else restaurant rejects
        T-->>R: Reject
        R->>O: Order rejected by the restaurant
        O->>P: Refund the payment
        P-->>O: refunded
        O->>O: Mark order CANCELLED
        O-)K: publish order.cancelled
        Note over O,P: Assumption: the Order Service owns the refund and the CANCELLED<br/>transition, mirroring how it marks FAILED in phase 1. Confirm the owner.
    end
```

---

## 4. Phase 3 — courier assignment and delivery

Continues from step 5 of phase 2 (`order.accepted` published). The offer loop is the
retry the courier decline triggers.

```mermaid
sequenceDiagram
    autonumber
    participant K as Kafka
    participant CO as Courier Service
    actor V as Courier
    actor T as Restaurant<br/>(tablet)
    actor C as Customer

    K-)CO: order.accepted
    loop until a courier accepts
        CO->>CO: Find nearest available courier
        CO->>V: Offer the job
        alt courier accepts
            V-->>CO: Accept
            CO->>CO: Assign the order to the courier
            CO-)K: publish order.courier_assigned
        else courier declines
            V-->>CO: Decline
            Note over CO,V: Retry the offer with the next nearest courier
        end
    end
    V->>T: Collect the order
    V->>CO: Mark PICKED_UP
    CO-)K: publish order.picked_up
    V->>C: Deliver the order
    V->>CO: Mark DELIVERED
    CO-)K: publish order.delivered
```

---

## 5. Notifications (cross-cutting)

The Notification Service subscribes to every `order.*` event and pushes to the customer at
each stage. It runs alongside phases 1–3 rather than after them.

```mermaid
sequenceDiagram
    autonumber
    participant K as Kafka
    participant N as Notification Service
    participant M as Mobile App
    actor C as Customer

    Note over K,N: The Notification Service consumes all order.* events
    K-)N: order.paid
    N->>M: Push: payment confirmed
    K-)N: order.accepted
    N->>M: Push: restaurant accepted the order
    K-)N: order.courier_assigned
    N->>M: Push: courier assigned
    K-)N: order.picked_up
    N->>M: Push: order picked up
    K-)N: order.delivered
    N->>M: Push: order delivered
    M-->>C: Notification shown on the phone
    opt the restaurant rejected the order
        K-)N: order.cancelled
        N->>M: Push: order cancelled and refunded
    end
```

---

## Open points

These were drawn because you established the fact, but the mechanism was not stated —
worth confirming before this goes on the wiki:

- **Refund ownership (phase 2).** You said a rejection means "refund via the Payment
  Service, order CANCELLED, customer notified", not which service drives it. Drawn as the
  Order Service, consistent with it marking FAILED in phase 1.
- **Event names for the courier stages.** `order.paid` and `order.accepted` are yours;
  `order.courier_assigned`, `order.picked_up`, `order.delivered` and `order.cancelled` are
  placeholders that match the stages you listed. Replace with the real topic/event names.
- **Push delivery path.** "Push notification to the customer" is drawn as the Notification
  Service pushing to the mobile app; the actual transport (FCM/APNs or otherwise) is not
  shown because it was not stated.
- **Endpoints beyond `POST /orders` and `POST /payments`** are unnamed on purpose — no
  headers, payload fields or status codes were invented for the notes.
