# 3. Generate invoice PDFs in a background job

Date: 2026-11-20

## Status

Accepted

## Context

Invoice PDFs are currently generated inside the web request that runs when a customer clicks download. In October, three incidents caused the billing page to time out. A large customer with about 4,000 line items requested a year of invoices, and the request hit the 30-second limit on the load balancer. Support counted 41 tickets about the problem that month.

Two alternatives were considered. Raising the timeout to 120 seconds was rejected, because it only moves the limit and keeps a web worker busy for the whole generation. Using a third-party PDF API was rejected, because legal does not allow invoice data to leave our infrastructure.

## Decision

We will generate invoice PDFs outside the web request, in a background job run by the existing Sidekiq setup that already handles email. Each generated file will be stored in the documents bucket, and the customer will receive an email with a link when the file is ready. Invoice downloads will no longer be instant, including for small invoices, so that the system keeps a single code path.

## Consequences

Downloading an invoice no longer returns the PDF immediately, even for small invoices. Customers wait for an email with a link. The team accepted this trade-off to avoid maintaining two code paths.

Generating a large request no longer holds a web request or a web worker for the duration of the generation, which removes the load balancer timeout as the limit on this path.

The PDF jobs share the Sidekiq queue with email delivery. A large burst of PDF jobs can delay emails, and the email team is aware of this risk.

Invoice data stays within our infrastructure, as legal requires, because no third-party PDF service is used.
