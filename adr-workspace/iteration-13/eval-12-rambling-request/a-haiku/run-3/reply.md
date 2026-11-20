I wrote the ADR as `doc/adr/0003-generate-invoice-pdfs-in-a-background-job.md`, following the existing log in `doc/adr/` (0001 and 0002, English, adr-tools format). It is marked Accepted, since you said the team agreed on it. It does not supersede anything, because no existing ADR covers invoice generation.

What the ADR records:
- Context: the October timeouts (three incidents, the 4,000-line-item customer, 41 tickets), plus the two rejected options: the 120-second timeout and the third-party PDF API (legal).
- Decision: background generation through the existing Sidekiq setup, storage in the documents bucket, and an emailed link.
- Consequences: no instant download even for small invoices, a shared Sidekiq queue that can delay email, and invoice data staying in our infrastructure.

I left out the billing module rename, since it is not part of this decision. It can be its own ADR if the team decides on it.

Questions for you, which the ADR does not answer:
1. Does the email team have a mitigation for the shared queue, such as a separate queue or a concurrency cap for PDF jobs? The ADR records the risk only.
2. How long do the download links stay valid, and what happens if a PDF job fails or is retried? Neither is in the ADR.
