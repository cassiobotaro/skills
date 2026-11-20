# 3. Move invoice PDF generation to a background job

Date: 2026-11-20

## Status

Accepted

## Context

Invoice PDFs are currently generated inside the web request that runs when a customer clicks download. A large customer with about 4,000 line items asked for a year of invoices, and that request hit the 30-second timeout on the load balancer. In October this produced three incidents in which the billing page timed out, and support counted 41 tickets about it that month.

Raising the load balancer timeout to 120 seconds was considered and rejected: it moves the limit without removing it, and it keeps a web worker occupied for the whole generation. Sending invoice data to a third-party PDF API was also considered, but legal does not allow invoice data to leave our infrastructure.

## Decision

We will generate invoice PDFs outside the web request, in a background job run through the existing Sidekiq setup that already processes emails. When a PDF is ready, it is stored in the documents bucket and the customer receives an email with a link to it. Instant download is removed for all invoices, including small ones, so that there is a single code path for generating invoices.

## Consequences

Customers no longer get an invoice PDF immediately on download. Every invoice, regardless of size, is delivered later through an emailed link, and the team accepted this trade-off.

Having one code path for all invoice sizes avoids maintaining two separate download mechanisms.

The Sidekiq queue is shared with the email system. A large burst of PDF jobs can delay email delivery for other senders, and the email team is aware of this risk.

Because generation now depends on background processing and email delivery, the customer's access to an invoice depends on both succeeding.
</content>
