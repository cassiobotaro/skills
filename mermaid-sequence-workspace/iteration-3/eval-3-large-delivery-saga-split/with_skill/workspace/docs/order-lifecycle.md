# Food delivery — order lifecycle

The full lifecycle is split into five diagrams: an overview plus one per phase, and a
last one for the notification fan-out. Participant ids and labels are the same across
all of them, so the same box means the same service everywhere.

## 0. Overview

<!-- preview/edit: https://l.mermaid.ai/Snxf1b -->

Coarse view of the whole saga — each numbered hop is expanded in the diagrams below.

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

## 1. Placement and payment

<!-- preview/edit: https://l.mermaid.ai/PofgdN -->

From the tap in the app to an authorized (or declined) card. Ends either in `FAILED`
(declined) or in the `order.paid` event that starts diagram 2.

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

## 2. Restaurant acceptance

<!-- preview/edit: https://l.mermaid.ai/pavq4I -->

Continues from the approved branch of diagram 1. The restaurant either accepts (which
starts diagram 3) or rejects, which refunds and cancels the order.

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

## 3. Courier assignment and delivery

<!-- preview/edit: https://l.mermaid.ai/IrGSak -->

Continues from `order.accepted` in diagram 2. The offer loop repeats with the next
nearest courier on every decline.

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

## 4. Notification fan-out

<!-- preview/edit: https://l.mermaid.ai/DSjTYE -->

The Notification Service consumes every `order.*` event and pushes one notification per
stage. Same shape for each event, so it is drawn once as a loop.

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
