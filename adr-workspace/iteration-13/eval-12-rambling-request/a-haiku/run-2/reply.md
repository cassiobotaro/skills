I wrote the ADR as `doc/adr/0003-generate-invoice-pdfs-in-a-background-job.md`, Accepted, dated 2026-11-20. It follows the existing log (`0001` and `0002` in `doc/adr/`, English). The Context covers the October timeouts, the 41 tickets, and the two rejected options (raising the timeout, and the third-party PDF API that legal ruled out). The Consequences list the accepted costs: no instant download even for small invoices, and the shared Sidekiq queue that can slow email delivery if flooded.

Things to know:

- The billing module rename is not in this ADR. It is a separate, unrelated decision, so it gets its own record if and when it is made.
- The shared-queue risk has no agreed mitigation in what you told me, so the ADR records it as a known risk without a fix. If you decided on a separate queue or throttling, tell me and I will add it as a decision or a follow-up ADR.
- The ADR does not name anyone or record the platform sync date, since you did not give an exact date for it. If you want the meeting cited in Context, send me the date.
