# 3. Generate invoice PDFs in background jobs

Date: 2026-11-20

## Status

Accepted

## Context

Invoice PDFs are generated inside the web request when a customer clicks download. In October this caused three incidents in which the billing page timed out: a large customer with about 4k line items asked for a year of invoices, and the request hit the 30s load balancer limit. Support counted 41 tickets about it that month.

Two alternatives were discussed in the platform sync and rejected. Raising the timeout to 120s only moves the cliff and ties up a web worker for the whole request. A third-party PDF API is ruled out because legal does not want invoice data leaving our infrastructure.

A Sidekiq setup already runs for emails.

## Decision

We will move invoice PDF generation out of the web request and run it as background jobs on the existing Sidekiq setup. The generated file will be stored in the documents bucket, and the customer will receive an email with a link when it is ready.

## Consequences

Large invoice requests no longer depend on the 30s load balancer limit or hold a web worker while the PDF is built.

Downloads are no longer instant, even for small invoices. We accepted this to avoid maintaining two code paths.

The Sidekiq queue is shared with emails, so a flood of PDF jobs will slow email delivery. The email team knows and has accepted this.
