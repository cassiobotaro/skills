I wrote this up as ADR 3 in your existing log: `doc/adr/0003-generate-invoice-pdfs-in-background-jobs.md`. Its status is Accepted and it is dated today. The log already had ADRs 1 and 2, so this is the next number.

It records the problem (October's three timeout incidents, 41 tickets), the two rejected options (raising the timeout to 120s, and a third-party PDF API that legal vetoed), and the decision itself: Sidekiq jobs, the file stored in the documents bucket, and an email with a link. The consequences list the downsides you named: no instant download, and the shared queue affecting the email team. I added nothing beyond what you told me.

I left out the idea of renaming the billing module because it is a separate matter. If you want it recorded, tell me and I will write it as its own ADR once there is an actual decision.

I have three questions, which would only add detail to the ADR:
1. Should the ADR mention anything about the link, such as how long it stays valid or whether it needs authentication? You didn't say, so I left it out.
2. Is there a cap or separate queue to keep PDF jobs from flooding the shared one? I only wrote that the email team knows about the risk.
3. Do you want Rafael, Marta or others named in the record? I kept it to the decisions and reasons without names.
