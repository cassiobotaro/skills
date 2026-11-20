# 3. Generate invoice PDFs in a background job

Date: 2026-11-20

## Status

Accepted

## Context

Invoice PDFs are generated inside the web request that runs when a customer clicks download. In October the billing page timed out three times when a large customer with about 4,000 line items requested a year of invoices and the request hit the 30-second load balancer limit. Support counted 41 tickets about this in that month.

Two alternatives were considered. Raising the timeout to 120 seconds was rejected because it only moves the limit and keeps a web worker busy for the whole generation. A third-party PDF API was rejected because legal does not want invoice data to leave our infrastructure.

## Decision

We will move invoice PDF generation out of the web request and into a background job on the existing Sidekiq setup, which already runs email jobs. Each generated PDF will be stored in the documents bucket, and the customer will receive an email with a link when the file is ready. Downloads will go through this path for all invoices, including small ones, so there is a single code path.

## Consequences

Customers no longer get an instant download, including for small invoices. This was accepted in exchange for having a single code path for all invoices.

Customers must wait for the email with the link before they can download a PDF, so the download now depends on the background job completing and on email delivery.

Large requests no longer hold a web worker or run into the load balancer timeout.

The Sidekiq queue is shared with the email team. A large batch of PDF jobs, such as a year of invoices for a large customer, could delay email delivery for everyone on that queue. The email team is aware of this risk.
