# 3. Generate invoice PDFs in background jobs

Date: 2026-11-20

## Status

Accepted

## Context

Invoice PDFs are currently generated inside the web request when a customer clicks download. In October this caused three incidents in which the billing page timed out: a large customer, with about 4,000 line items, requested a year of invoices and the request hit the 30-second limit on the load balancer. Support counted 41 tickets about the problem that month.

Other options were discussed in the platform sync. Raising the timeout to 120 seconds only moves the cliff and keeps a web worker busy for the whole request. A third-party PDF API was ruled out because legal does not want invoice data to leave our infrastructure.

A Sidekiq setup already runs for emails.

## Decision

We will move invoice PDF generation out of the web request and into background jobs on the existing Sidekiq setup. The generated file will be stored in the documents bucket, and the customer will receive an email with a link when it is ready.

All downloads will use this path, including those for small invoices.

## Consequences

Customers no longer get an instant download, even for small invoices. We accepted this to avoid maintaining two code paths.

The Sidekiq queue is shared with email, so a flood of PDF jobs will be felt by the email team. They are aware of this.

Web workers are no longer tied up while a PDF is generated, and the request no longer runs into the load balancer's 30-second limit.

Invoice data stays inside our infrastructure.
