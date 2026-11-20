# 3. Move invoice PDF generation to background jobs

Date: 2026-11-20

## Status

Accepted

## Context

Invoice PDFs are currently generated inside the web request that serves a customer's download. A large request can exceed the 30-second limit enforced by the load balancer. A customer with about 4,000 line items who asked for a year of invoices hit that limit. In October this caused three incidents in which the billing page timed out, and the support team counted 41 tickets about it that month.

Two alternatives were considered. Raising the request timeout to 120 seconds was rejected because it only moves the limit and keeps a web worker occupied for the whole generation. Using a third-party PDF API was rejected because the legal team does not allow invoice data to leave our infrastructure.

## Decision

We will generate invoice PDFs in a background job, using the Sidekiq setup that already runs email jobs. When a PDF is ready, it is stored in the documents bucket and the customer receives an email with a link to it.

## Consequences

Customers no longer get an instant download, including for small invoices. This was accepted so that the system keeps a single code path for all invoices instead of separate paths for small and large ones.

PDF generation no longer runs inside a web request, so large invoices are no longer bounded by the load balancer's 30-second limit.

The Sidekiq queue is shared with the email jobs. A large volume of PDF jobs can slow email delivery for the email team, who are aware of this risk.

Finished invoice files are kept in the documents bucket and reached through the link in the email.
