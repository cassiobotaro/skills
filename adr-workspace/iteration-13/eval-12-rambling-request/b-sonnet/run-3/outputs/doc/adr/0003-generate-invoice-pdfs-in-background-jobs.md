# 3. Generate invoice PDFs in background jobs

Date: 2026-11-20

## Status

Accepted

## Context

Invoice PDFs are currently generated inside the web request when a customer clicks download. In October this caused three incidents in which the billing page timed out: a large customer with about 4,000 line items requested a year of invoices, and the request hit the 30-second limit on the load balancer. Support counted 41 tickets about the problem that month.

Two other options were discussed in the platform sync and rejected. Raising the timeout to 120 seconds would only move the cliff and would tie up a web worker for the whole request. A third-party PDF API is ruled out because legal does not want invoice data to leave our infrastructure.

A Sidekiq setup already runs for emails, and its queue is shared.

## Decision

We will move invoice PDF generation out of the web request and into background Sidekiq jobs on the existing setup. When a job finishes, it stores the file in the documents bucket, and the customer receives an email with a link to it.

We will use this single path for every invoice, including small ones, so that there are not two code paths.

## Consequences

Customers no longer get an instant download. This applies even to small invoices, because we chose not to keep two code paths. The team accepted this.

Because the Sidekiq queue is shared, a flood of PDF jobs will slow the email team's jobs. The email team knows about this.

Generation no longer holds a web worker or runs against the load balancer's 30-second limit.

Invoice data stays within our infrastructure.
