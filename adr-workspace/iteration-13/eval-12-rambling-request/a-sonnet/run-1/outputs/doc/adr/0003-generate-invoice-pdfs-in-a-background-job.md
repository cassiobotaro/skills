# 3. Generate invoice PDFs in a background job

Date: 2026-11-20

## Status

Accepted

## Context

Invoice PDFs are generated inside the web request when a customer clicks download. In October this caused three incidents in which the billing page timed out: a large customer with about 4,000 line items requested a year of invoices, and the request hit the 30 second limit on the load balancer. Support counted 41 tickets about it that month.

Raising the timeout to 120 seconds was considered and rejected, because it only moves the cliff and ties up a web worker for the whole request. A third-party PDF API was also considered, but legal does not want invoice data to leave our infrastructure.

A Sidekiq setup already runs for emails, and its queue is shared.

## Decision

We will move invoice PDF generation out of the web request and into a background job on the existing Sidekiq setup. The job will store the generated file in the documents bucket, and the customer will receive an email with a link when it is ready.

## Consequences

Large invoice requests no longer depend on the load balancer's 30 second limit or hold a web worker while the PDF is built.

Customers lose the instant download, even for small invoices. We accepted this to avoid maintaining two code paths.

The Sidekiq queue is shared with the email team, so a flood of PDF jobs would delay their emails. The email team is aware of this.
