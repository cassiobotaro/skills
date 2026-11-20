# 3. Generate invoice PDFs in a background job

Date: 2026-11-20

## Status

Accepted

## Context

Invoice PDFs are generated inside the web request when a customer clicks download. In October, three incidents occurred in which the billing page timed out at the load balancer's 30-second limit. The trigger was a large customer with about 4,000 line items who requested a year of invoices. Support counted 41 tickets about the timeouts that month.

Two alternatives were considered. Raising the load balancer timeout to 120 seconds would move the limit, but it would still hold a web worker for the whole generation. A third-party PDF API was ruled out because legal does not want invoice data to leave our infrastructure.

## Decision

We will generate invoice PDFs outside the web request, as background jobs on the existing Sidekiq setup, the same queue that already handles emails. Each generated PDF is stored in the documents bucket, and the customer receives an email with a link when the file is ready. Downloads are no longer instant, for invoices of any size, so there is a single code path for invoice PDFs.

## Consequences

Customers no longer get an instant download, including for small invoices. The team accepted this in exchange for having one code path instead of two.

The billing page no longer holds a web worker or depends on the load balancer timeout while a PDF is generated, so large requests stop hitting the 30-second limit.

The Sidekiq queue is shared with email delivery. A flood of PDF jobs can delay emails. The email team knows about this risk and accepted it.
