I wrote this up as ADR 3, status Accepted, because the platform sync agreed on it:

- `doc/adr/0003-generate-invoice-pdfs-in-background-jobs.md`

It records the October incidents (three timeouts at the 30s load balancer limit, 41 tickets), the two rejected options (a 120s timeout, and a third-party PDF API that legal vetoed), and the decision to use the existing Sidekiq setup, the documents bucket and an email link. The consequences cover the loss of instant downloads, which you accepted to avoid two code paths. They also cover the shared queue and the email team's awareness of it. I added only what you told me.

Two things I left out on purpose:
- The billing module rename is a separate matter and no decision has been made, so it isn't in this ADR. If the team decides to do it, it can get its own ADR.
- You didn't say which Sidekiq queue the PDF jobs will use. I didn't invent one.

Questions, if you want to tighten the record:
1. Should the PDF jobs share the email queue or get their own queue? You said the queue is shared, so I recorded that as is.
2. Is there a target for how long a customer waits for the email link? I didn't write one.
