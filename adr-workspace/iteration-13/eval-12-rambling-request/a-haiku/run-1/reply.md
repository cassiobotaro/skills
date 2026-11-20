I wrote the ADR as `doc/adr/0003-generate-invoice-pdfs-in-a-background-job.md`. It is Accepted, because the platform sync agreed on it. It records only the decision, the October incidents, the two rejected alternatives (raising the timeout to 120s, and the third-party PDF API), and the accepted trade-offs (no instant download, and the shared Sidekiq queue with email).

Three things I left out on purpose:

- The billing module rename is a separate decision. It belongs in its own ADR once someone decides on it.
- The ADR does not say whether the emailed link expires or how access to the documents bucket is controlled. You did not mention either, so I did not guess.
- It does not say whether PDF jobs will get their own queue to protect email. That would be a new decision, so I recorded the shared queue as a known risk.

Questions for you:

1. Is the email link time-limited, or does it need login? If the team has decided, I can add that to Consequences.
2. Was a separate queue for PDF jobs discussed? If so, and it was rejected, I can record that as an alternative.
3. Should the billing module rename get its own ADR when it is decided?
