# 3. Generate invoice PDFs in background jobs

Date: 2026-11-20

## Status

Accepted

## Context

Invoice PDFs are currently generated inside the web request when a customer clicks download. In October this caused three incidents in which the billing page timed out: a large customer (about 4,000 line items) requested a year of invoices and the request hit the 30-second limit on the load balancer. Support counted 41 tickets about it that month.

Two alternatives were discussed in the platform sync and rejected. Raising the timeout to 120 seconds only moves the cliff and ties up a web worker for the whole request. A third-party PDF API was ruled out because legal does not want invoice data leaving our infrastructure.

A Sidekiq setup already runs for emails, and the documents bucket already exists.

## Decision

We will move PDF generation out of the web request and run it as a background job on the existing Sidekiq setup. The generated file will be stored in the documents bucket, and the customer will receive an email with a link when it is ready.

All invoices will use this path, including small ones, so that there is a single code path.

## Consequences

Downloads are no longer instant, even for small invoices. This was accepted so that we do not maintain two code paths.

Large requests no longer depend on the load balancer's 30-second limit or hold a web worker while the PDF is generated.

The Sidekiq queue is shared with the email team. If we flood it with PDF jobs, email delivery will be affected. The email team is aware of this.
