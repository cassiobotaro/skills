I wrote this up as ADR 3 and saved it to `doc/adr/0003-generate-invoice-pdfs-in-background-jobs.md`. It is Accepted, because you said the platform sync agreed on it. It records the October incidents and the 41 tickets, the two rejected options (a 120s timeout and a third-party PDF API), the move to Sidekiq with the documents bucket and an email link, and the accepted trade-offs.

- I left the billing module rename out. It is a separate topic, and no decision was made on it. If the team decides to do it, it gets its own ADR.
- I did not add anything about queue isolation or rate limiting. You only said the email team knows about the shared queue. If the team agreed on a mitigation, such as a dedicated queue or a concurrency cap, tell me and I can add it.

Question: was the platform sync fully agreed, or should this stay Proposed until someone signs off? Change the Status line if it is not final.
