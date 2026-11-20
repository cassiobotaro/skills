I wrote the decision up as ADR 0003, "Move invoice PDF generation to background jobs", at doc/adr/0003-move-invoice-pdf-generation-to-background-jobs.md in the repository. It is marked Accepted, since the platform sync agreed on it. The log is in English, so the ADR is too.

The ADR covers the October timeouts and the 41 tickets, the two rejected alternatives (raising the timeout to 120s, and a third-party PDF API that legal ruled out), the decision to use the existing Sidekiq setup with files in the documents bucket and an emailed link, and the accepted trade-offs: no instant download even for small invoices, and the shared Sidekiq queue with the email team.

I left out the billing module rename because it is unrelated to this decision. If you want it recorded, it needs its own decision first.

One thing to confirm: the ADR says the email team knows about the shared-queue risk. If you want a concrete mitigation there, such as a separate queue, that would be a new decision and would need its own ADR.
