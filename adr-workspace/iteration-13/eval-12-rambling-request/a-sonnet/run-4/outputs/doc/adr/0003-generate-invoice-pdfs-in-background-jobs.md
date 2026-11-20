# 3. Generate invoice PDFs in background jobs

Date: 2026-11-20

## Status

Accepted

## Context

Invoice PDFs are generated inside the web request when a customer clicks download. In October this caused three incidents in which the billing page timed out: a large customer with about 4,000 line items requested a year of invoices, and the request hit the 30 second limit on the load balancer. Support counted 41 tickets about it that month.

Three options were discussed in the platform sync. Raising the timeout to 120 seconds only moves the cliff and keeps a web worker tied up for the whole request. A third-party PDF API is ruled out because legal does not want invoice data to leave our infrastructure.

## Decision

We will move PDF generation out of the web request and run it as a background job on the existing Sidekiq setup, which already runs emails. The generated file will be stored in the documents bucket, and the customer will receive an email with a link when it is ready.

All invoice downloads will use this path, including those for small invoices, so that there is a single code path.

## Consequences

Web workers are no longer held while a PDF is generated, and the request no longer depends on the load balancer's 30 second limit.

Customers lose the instant download, even for small invoices. The team accepted this to avoid maintaining two code paths.

The Sidekiq queue is shared with emails, so a flood of PDF jobs will be felt by the email team. They are aware of this.
