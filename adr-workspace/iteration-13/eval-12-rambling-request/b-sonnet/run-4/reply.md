I wrote this up as an ADR. The decision, the October incidents (three timeouts, about 4k line items, 41 tickets), the two rejected alternatives (the 120s timeout and the third-party PDF API) and the accepted downsides are all as you described them.

Two things to know:

- There was no decision log in the repo, so I created `doc/adr/` with the standard seed ADR (0001, "Record architecture decisions"). Your decision is ADR 0002, status Accepted since you said it was agreed.
- I left the billing module rename out. It's a separate, undecided idea, and an ADR records one decision. If you do decide to rename it, tell me and I'll write it up as its own ADR.

Questions, if you want the record fuller. I did not guess at any of these:

1. Who agreed in the platform sync? Naming the people or team in the Context would help a future reader.
2. Is there a retention period for the generated PDFs in the documents bucket, or a link expiry? I didn't write either.
3. Do you want a different status than Accepted (for example Proposed, if the email team hasn't formally signed off)?

Files:
- doc/adr/0001-record-architecture-decisions.md
- doc/adr/0002-generate-invoice-pdfs-in-background-jobs.md
