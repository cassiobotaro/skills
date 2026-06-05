# Food Delivery — Order Lifecycle

This page documents the end-to-end lifecycle of a food delivery order, from the moment a customer places it in the mobile app through to delivery (or one of the failure branches along the way).

The flow is an event-driven **saga**: each service owns one step, persists its own state, and either calls the next service synchronously (for payment) or emits a Kafka event (`order.*`) that downstream services consume. The Notification Service listens to every `order.*` event and pushes the customer an update at each stage.

> All diagrams below are Mermaid `sequenceDiagram` blocks and render natively on GitHub.

## 1. End-to-end overview (with failure branches)

```mermaid
sequenceDiagram
    autonumber
    actor Cust as Customer (Mobile App)
    participant GW as API Gateway
    participant Ord as Order Service
    participant DB as Postgres (Orders)
    participant Pay as Payment Service
    participant Stripe as Stripe
    participant K as Kafka
    participant Rest as Restaurant Service
    participant Tab as Restaurant Tablet
    participant Cour as Courier Service
    actor Crr as Courier
    participant Notif as Notification Service

    Cust->>GW: Place order
    GW->>Ord: POST /orders
    Ord->>DB: INSERT order (status = PENDING)
    DB-->>Ord: ok

    Ord->>Pay: POST /payments (authorize)
    Pay->>Stripe: Authorize card
    Stripe-->>Pay: approved / declined
    Pay-->>Ord: result

    alt Payment declined
        Ord->>DB: UPDATE status = FAILED
        Ord-->>GW: 402 Payment Failed
        GW-->>Cust: Show payment error
        Note over Cust,Stripe: End — order FAILED
    else Payment approved
        Ord->>DB: UPDATE status = PAID
        Ord->>K: publish order.paid
        K-->>Notif: order.paid
        Notif-->>Cust: Push "Payment confirmed"
        Ord-->>GW: 201 Created (order PAID)
        GW-->>Cust: Order placed

        K-->>Rest: consume order.paid
        Rest->>Tab: Push new order
        Tab-->>Rest: Accept / Reject

        alt Restaurant rejects
            Rest->>Pay: POST /refunds
            Pay->>Stripe: Refund charge
            Stripe-->>Pay: refunded
            Pay-->>Rest: ok
            Rest->>K: publish order.cancelled
            K-->>Ord: consume order.cancelled
            Ord->>DB: UPDATE status = CANCELLED
            K-->>Notif: order.cancelled
            Notif-->>Cust: Push "Order cancelled & refunded"
            Note over Cust,Stripe: End — order CANCELLED (refunded)
        else Restaurant accepts
            Rest->>K: publish order.accepted
            K-->>Ord: consume order.accepted
            Ord->>DB: UPDATE status = ACCEPTED
            K-->>Notif: order.accepted
            Notif-->>Cust: Push "Restaurant accepted your order"

            K-->>Cour: consume order.accepted
            loop Until a courier accepts
                Cour->>Cour: Find nearest available courier
                Cour->>Crr: Offer job
                Crr-->>Cour: Decline (try next)
            end
            Crr-->>Cour: Accept
            Cour->>K: publish order.courier_assigned
            K-->>Ord: consume order.courier_assigned
            Ord->>DB: UPDATE status = COURIER_ASSIGNED
            K-->>Notif: order.courier_assigned
            Notif-->>Cust: Push "Courier assigned"

            Crr->>Cour: Mark PICKED_UP
            Cour->>K: publish order.picked_up
            K-->>Ord: consume order.picked_up
            Ord->>DB: UPDATE status = PICKED_UP
            K-->>Notif: order.picked_up
            Notif-->>Cust: Push "Order picked up"

            Crr->>Cour: Mark DELIVERED
            Cour->>K: publish order.delivered
            K-->>Ord: consume order.delivered
            Ord->>DB: UPDATE status = DELIVERED
            K-->>Notif: order.delivered
            Notif-->>Cust: Push "Delivered — enjoy!"
            Note over Cust,Notif: End — order DELIVERED
        end
    end
```

## 2. Focused view: Place order & payment

```mermaid
sequenceDiagram
    autonumber
    actor Cust as Customer (Mobile App)
    participant GW as API Gateway
    participant Ord as Order Service
    participant DB as Postgres (Orders)
    participant Pay as Payment Service
    participant Stripe as Stripe
    participant K as Kafka
    participant Notif as Notification Service

    Cust->>GW: Place order
    GW->>Ord: POST /orders
    Ord->>DB: INSERT order (status = PENDING)
    DB-->>Ord: ok

    Ord->>Pay: POST /payments (authorize)
    Pay->>Stripe: Authorize card
    Stripe-->>Pay: approved / declined
    Pay-->>Ord: result

    alt Payment declined
        Ord->>DB: UPDATE status = FAILED
        Ord-->>GW: 402 Payment Failed
        GW-->>Cust: Show payment error
    else Payment approved
        Ord->>DB: UPDATE status = PAID
        Ord->>K: publish order.paid
        Ord-->>GW: 201 Created
        GW-->>Cust: Order placed
        K-->>Notif: order.paid
        Notif-->>Cust: Push "Payment confirmed"
    end
```

## 3. Focused view: Restaurant accept/reject

```mermaid
sequenceDiagram
    autonumber
    participant K as Kafka
    participant Rest as Restaurant Service
    participant Tab as Restaurant Tablet
    participant Pay as Payment Service
    participant Stripe as Stripe
    participant Ord as Order Service
    participant DB as Postgres (Orders)
    participant Notif as Notification Service
    actor Cust as Customer (Mobile App)

    K-->>Rest: consume order.paid
    Rest->>Tab: Push new order
    Tab-->>Rest: Accept / Reject

    alt Restaurant rejects
        Rest->>Pay: POST /refunds
        Pay->>Stripe: Refund charge
        Stripe-->>Pay: refunded
        Pay-->>Rest: ok
        Rest->>K: publish order.cancelled
        K-->>Ord: consume order.cancelled
        Ord->>DB: UPDATE status = CANCELLED
        K-->>Notif: order.cancelled
        Notif-->>Cust: Push "Order cancelled & refunded"
    else Restaurant accepts
        Rest->>K: publish order.accepted
        K-->>Ord: consume order.accepted
        Ord->>DB: UPDATE status = ACCEPTED
        K-->>Notif: order.accepted
        Notif-->>Cust: Push "Restaurant accepted your order"
    end
```

## 4. Focused view: Courier assignment, pickup & delivery

```mermaid
sequenceDiagram
    autonumber
    participant K as Kafka
    participant Cour as Courier Service
    actor Crr as Courier
    participant Ord as Order Service
    participant DB as Postgres (Orders)
    participant Notif as Notification Service
    actor Cust as Customer (Mobile App)

    K-->>Cour: consume order.accepted

    loop Until a courier accepts
        Cour->>Cour: Find nearest available courier
        Cour->>Crr: Offer job
        Crr-->>Cour: Decline (try next)
    end
    Crr-->>Cour: Accept

    Cour->>K: publish order.courier_assigned
    K-->>Ord: consume order.courier_assigned
    Ord->>DB: UPDATE status = COURIER_ASSIGNED
    K-->>Notif: order.courier_assigned
    Notif-->>Cust: Push "Courier assigned"

    Crr->>Cour: Mark PICKED_UP
    Cour->>K: publish order.picked_up
    K-->>Ord: consume order.picked_up
    Ord->>DB: UPDATE status = PICKED_UP
    K-->>Notif: order.picked_up
    Notif-->>Cust: Push "Order picked up"

    Crr->>Cour: Mark DELIVERED
    Cour->>K: publish order.delivered
    K-->>Ord: consume order.delivered
    Ord->>DB: UPDATE status = DELIVERED
    K-->>Notif: order.delivered
    Notif-->>Cust: Push "Delivered — enjoy!"
```

## Notes & assumptions

A few details weren't fully specified, so the diagrams make these reasonable, clearly-labelled choices. Adjust if your implementation differs:

- **Order status enum.** Uses `PENDING → PAID → ACCEPTED → COURIER_ASSIGNED → PICKED_UP → DELIVERED`, plus terminal `FAILED` and `CANCELLED`. Only `PENDING`, `FAILED`, `CANCELLED`, `PICKED_UP`, and `DELIVERED` were named explicitly; the intermediate states are inferred from the notification stages you listed.
- **Canonical order state.** I assumed the Order Service is the system of record and updates Postgres in response to downstream Kafka events. If each service keeps its own state with no central order projection, drop those Order Service/Postgres update arrows.
- **Event names.** `order.paid` and `order.accepted` were specified. I named the others (`order.cancelled`, `order.courier_assigned`, `order.picked_up`, `order.delivered`) to match the `order.*` pattern the Notification Service subscribes to. Rename to fit your conventions.
- **Refund vs. void.** On rejection I show a refund per your description; if payment was only *authorized* (not captured), this is typically a void of the authorization instead — worth confirming against the Payment Service API.
- **API Gateway in async parts.** The gateway only appears on the synchronous request/response path. Once the saga goes async over Kafka, the app receives updates via push notifications, not the gateway.
