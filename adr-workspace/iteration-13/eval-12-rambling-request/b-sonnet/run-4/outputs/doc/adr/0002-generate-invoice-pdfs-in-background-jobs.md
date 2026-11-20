# 2. Generate invoice PDFs in background jobs

Date: 2026-11-20

## Status

Accepted

## Context

Invoice PDFs are generated inside the web request when a customer clicks download. In October this caused three incidents in which the billing page timed out: a large customer with about 4,000 line items requested a year of invoices, and the request hit the 30-second limit on the load balancer. Support counted 41 tickets about the problem that month.

Two alternatives were discussed in the platform sync. Raising the timeout to 120 seconds was rejected because it only moves the cliff and ties up a web worker for the whole request. A third-party PDF API was rejected because legal does not want invoice data to leave our infrastructure.

A Sidekiq setup already runs for emails.

## Decision

We will move PDF generation out of the web request and run it as a background job on the existing Sidekiq setup. The generated file will be stored in the documents bucket, and the customer will receive an email with a link when it is ready.

We will use this flow for every invoice, including small ones, so that there is a single code path.

## Consequences

Large invoice requests no longer depend on the load balancer's 30-second limit, and they no longer hold a web worker while the PDF is built.

Customers lose the instant download, even for small invoices. The team accepted this in order to avoid maintaining two code paths.

The Sidekiq queue is shared with emails, so a flood of PDF jobs will be felt by the email team. They are aware of this.
