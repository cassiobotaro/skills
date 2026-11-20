# 3. Generate invoice PDFs in the background

Date: 2026-11-20

## Status

Accepted

## Context

Invoice PDFs are currently generated inside the web request that runs when a customer clicks download. In October this caused three incidents on the billing page. A large customer with about 4,000 line items requested a year of invoices, and the request hit the 30-second limit on the load balancer. Support counted 41 tickets about the timeouts that month.

Two alternatives were considered and not adopted. Raising the load balancer timeout to 120 seconds only moves the limit, and it keeps a web worker occupied for the whole generation. Sending invoice data to a third-party PDF API was rejected because legal does not allow invoice data to leave our infrastructure.

## Decision

We will generate invoice PDFs in the background, outside the web request. Generation will run as a Sidekiq job on the existing Sidekiq setup, which already handles email. Each finished PDF will be stored in the documents bucket, and the customer will receive an email with a link to it when it is ready. Downloads will no longer be instant, including for small invoices, because we will not keep two code paths.

## Consequences

Customers no longer get an instant download, even for small invoices. They wait for an email with a link to the generated PDF.

There is a single code path for invoices of every size, instead of one path for small invoices and another for large ones.

The web worker is no longer occupied for the duration of PDF generation, so large requests no longer hit the load balancer timeout.

The Sidekiq queue is shared with the email team. A large burst of PDF jobs can delay email delivery for that team. The email team is aware of this risk.

Invoice data stays within our infrastructure, as legal requires.

PDF delivery now depends on the documents bucket and on the email path for customers to reach their files.
