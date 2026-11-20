I wrote the ADR as `doc/adr/0003-generate-invoice-pdfs-in-a-background-job.md` (Accepted, dated 2026-11-20). It follows the existing log, where 0001 is the seed and 0002 is PostgreSQL.

It records the decision as you described it. The context is the October timeouts (three incidents, 4k line items, the 30s load balancer limit, 41 tickets). The rejected options are the 120s timeout and the third-party PDF API, which legal ruled out. The consequences are the loss of instant download, the shared Sidekiq queue, and the email team knowing about it.

I left the billing module rename out. It is a separate topic, and it has no decision yet. If you decide to do it, it would get its own ADR.

A few details I did not know, so the ADR does not mention them:
1. Was the Thursday platform sync the place where this was agreed, and who owns the follow-up? I left meeting and people names out.
2. Is there any plan to protect the shared queue, such as a separate queue or rate limiting? The ADR only says the email team is aware. Tell me if there is one and I will add it.
3. Does the emailed link expire, or have any access control? That is not recorded, so I did not write it.
