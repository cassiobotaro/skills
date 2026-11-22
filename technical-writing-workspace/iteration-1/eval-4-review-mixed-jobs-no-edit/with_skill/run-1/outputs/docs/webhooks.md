# Webhooks

Webhooks were introduced in 2023 after several customers asked for a way to avoid
polling. At the time, two designs were discussed, and the push model was chosen because
polling was considered wasteful.

In this guide you will learn everything about webhooks.

## Setup

First, the endpoint must be registered. It is done in the dashboard, under
**Settings > Webhooks**. Simply paste the URL and the events will be delivered.

The following events exist:

| Event | When |
|---|---|
| `invoice.paid` | An invoice is paid |
| `invoice.failed` | A charge fails |
| `customer.deleted` | A customer is deleted |

After registration a secret is generated. It should be stored safely, because it is
shown only once.

## Verifying signatures

Each delivery is signed. The signature is sent in the `X-Signature` header and must be
verified before the payload is trusted. It is computed with HMAC-SHA256 over the raw
body.

## Retries

If a delivery fails, it is retried. After some attempts, the endpoint is disabled and an
email is sent.
