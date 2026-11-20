I wrote the ADR as 0003 in `doc/adr/` (next after your existing 0002), status Accepted since the thread says it was agreed: `doc/adr/0003-generate-invoice-pdfs-in-background-jobs.md`.

It covers the October incidents (3 timeouts, 4k line items, 30s limit, 41 tickets), the two rejected options (120s timeout, third-party PDF API blocked by legal), the Sidekiq + documents bucket + email-link decision, and the accepted downsides (no instant download, shared queue impact on the email team).

Notes:
- I left out the billing module rename. It is a separate, unmade idea. If you decide to do it, it would get its own ADR.
- I did not add details you did not give me (retry behaviour, a dedicated queue, link expiry, and so on). If any of those were agreed, tell me and I can add them to the Decision.

Questions:
1. Was the decision formally agreed in the Thursday sync (Accepted), or is it still awaiting sign-off (Proposed)?
2. What is the date of the sync, if you want it recorded in the Context? I dated the ADR today, 2026-11-20.
