I wrote the ADR as `doc/adr/0003-generate-invoice-pdfs-in-a-background-job.md` (Accepted, dated 2026-11-20), in the existing English log next to 0001 and 0002.

Questions for you before this is final:

1. Retention and access: does the documents bucket link in the email expire, and does it require the customer to be logged in? You did not say, so the ADR does not mention either.
2. Queue isolation: is a separate Sidekiq queue for PDF jobs planned, or is sharing the email queue the accepted setup? The ADR records the shared queue as it was described.
3. Failure handling: what happens when a PDF job fails, and does the customer get a notice? Not stated, so not recorded.

Not recorded: the billing module rename. It is unrelated to this decision and belongs in its own record if it is ever decided.
