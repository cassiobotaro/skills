# 3. Generate invoice PDFs in the background

Date: 2026-11-20

## Status

Accepted

## Context

Invoice PDFs are currently generated inside the web request that runs when a customer clicks download. The load balancer times out requests after 30 seconds. In October the billing page timed out three times when a large customer with about 4,000 line items requested a year of invoices. Support counted 41 tickets about this problem that month.

Raising the timeout to 120 seconds was considered and rejected: it moves the limit rather than removing it, and it holds a web worker for the whole generation. Sending invoice data to a third-party PDF API was considered and rejected because legal does not allow invoice data to leave our infrastructure.

A Sidekiq setup already runs for email delivery. Its queue is shared with the email team.

## Decision

We will generate invoice PDFs as a background job in the existing Sidekiq setup, outside the web request. Each generated file is stored in the documents bucket, and the customer receives an email with a link when the file is ready.

Invoice PDFs will use this asynchronous path for every invoice, so there will be one code path and no instant download, including for small invoices.

## Consequences

Customers no longer download an invoice PDF instantly. This applies to all invoices, small ones included. We accept it in exchange for having a single code path.

PDF generation no longer runs inside the web request, so the 30-second load balancer limit no longer constrains it.

PDF jobs share the Sidekiq queue with email. A large volume of PDF jobs can delay email delivery for the email team. The email team is aware of this.

Customers receive the file through a link in an email instead of a download on the billing page.
