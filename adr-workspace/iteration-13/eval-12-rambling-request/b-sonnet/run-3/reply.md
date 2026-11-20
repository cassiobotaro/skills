I wrote the ADR as `doc/adr/0003-generate-invoice-pdfs-in-background-jobs.md`, status Accepted, dated 2026-11-20. The log already had 0001 and 0002, so this is 0003.

What it records:
- **Context:** the October incidents (three timeouts at the 30s load balancer limit, about 4k line items, 41 support tickets). It also covers the two rejected options: raising the timeout to 120s, and a third-party PDF API.
- **Decision:** Sidekiq background jobs, the file goes to the documents bucket, and the customer gets an email with a link. There is one code path for all invoices.
- **Consequences:** no instant download, even for small invoices. The shared Sidekiq queue means the email team will feel any flood of jobs. The ADR also says generation no longer holds a web worker and invoice data stays in-house.

I left out the billing module rename. It is a separate topic and no decision was made, so it has no ADR. If you decide to do it, tell me and I'll write one.

Questions:
1. I used today's date because you didn't give the date of the Thursday sync. Do you want the sync date instead?
2. Does the ADR need anything on how a failed or retried job is handled, or on how long the link stays valid? You didn't mention either, so I didn't write anything about them.
