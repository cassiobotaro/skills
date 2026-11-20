# 3. Generate invoice PDFs in a background job

Date: 2026-11-20

## Status

Accepted

## Context

Invoice PDFs are generated inside the web request that runs when a customer clicks download. In October, three incidents occurred in which the billing page timed out at the load balancer's 30-second limit. The cause was a large customer with about 4,000 line items who requested a year of invoices. Support counted 41 tickets about the problem that month.

Raising the load balancer timeout to 120 seconds was considered. It would move the point at which requests fail rather than remove it, and the web worker would stay occupied for the whole generation. A third-party PDF generation API was also considered, but legal does not allow invoice data to leave our infrastructure.

The service already runs Sidekiq for sending emails.

## Decision

We will generate invoice PDFs in a background job, run through the existing Sidekiq setup. When a PDF is ready, it is stored in the documents bucket and the customer receives an email with a link to it.

Every invoice goes through this path, including small ones, so that there is a single code path for invoice PDFs.

## Consequences

Customers no longer get an instant download. Every invoice, including small ones, is delivered by email with a link, which the team accepted in exchange for having one code path.

Large exports no longer hold a web worker for the duration of generation, and they are no longer subject to the load balancer's 30-second request limit.

The Sidekiq queue is shared with the email team's jobs. A large volume of invoice jobs can delay email delivery. The email team is aware of this. This decision does not add a separate queue or throttling for invoice jobs.
