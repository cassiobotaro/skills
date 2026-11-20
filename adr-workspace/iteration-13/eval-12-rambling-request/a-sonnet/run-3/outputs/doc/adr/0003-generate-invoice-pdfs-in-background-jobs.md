# 3. Generate invoice PDFs in background jobs

Date: 2026-11-20

## Status

Accepted

## Context

Invoice PDFs are generated inside the web request when a customer clicks download. In October this caused three incidents in which the billing page timed out: a large customer with about 4,000 line items requested a year of invoices and the request hit the 30-second limit on the load balancer. Support counted 41 tickets about it that month.

Two alternatives were discussed in the platform sync and rejected. Raising the timeout to 120 seconds only moves the cliff and ties up a web worker for the whole request. A third-party PDF API is not acceptable to legal, who do not want invoice data leaving our infrastructure.

A Sidekiq setup already runs for emails, and its queue is shared.

## Decision

We will move PDF generation out of the web request and run it as a background job on the existing Sidekiq setup. When the job finishes, we will store the file in the documents bucket and email the customer a link to it.

All invoice downloads will use this path, including small invoices, so that there is a single code path.

## Consequences

Customers lose the instant download: even a small invoice is now delivered by email once the job completes. The team accepted this to avoid maintaining two code paths.

Web workers are no longer held for the duration of PDF generation, and the request no longer depends on the 30-second load balancer limit.

Invoice data stays within our infrastructure.

The Sidekiq queue is shared with email, so a flood of PDF jobs will slow email delivery. The email team knows about this and accepts it.
