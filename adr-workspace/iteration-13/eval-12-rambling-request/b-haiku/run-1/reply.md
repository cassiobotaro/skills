I wrote the ADR as `doc/adr/0003-generate-invoice-pdfs-in-the-background.md`, status Accepted, with Context, Decision and Consequences taken from what you described. The Consequences include the trade-offs you accepted: no instant download even for small invoices, and the shared Sidekiq queue that can slow the email team.

I left out the billing module rename because it is a separate decision and would need its own ADR when you make it.

A few things are not in the ADR because you did not say them. Please tell me if you want any added:
1. What happens when a PDF job fails: retries, and how the customer is told.
2. Whether the emailed link expires or needs login, and who can access the documents bucket.
3. Whether the Sidekiq queue gets its own worker pool or a priority setting to protect email delivery, or whether that is still open.
