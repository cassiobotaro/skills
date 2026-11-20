I wrote the ADR as `doc/adr/0003-move-invoice-pdf-generation-to-a-background-job.md`, status Accepted, following the existing log in `doc/adr/` (ADRs 0001 and 0002, English, adr-tools format).

What it records: invoice PDFs move out of the web request into a Sidekiq background job, the file goes to the documents bucket, and the customer gets an email with a link. Instant download is dropped for all invoices. The rejected options (raising the timeout to 120s, a third-party PDF API) are in Context with the reasons you gave.

Two things I left out or need from you:
- The billing module rename is not in the ADR, since it was not decided in the sync. It can be its own ADR once the name is agreed.
- The ADR does not say how the email team's Sidekiq capacity is protected from a flood of PDF jobs (separate queue, rate limit, etc.). Nothing like that was mentioned, so it is recorded only as a known risk. If a mitigation was agreed, tell me and I will add it to Consequences.
