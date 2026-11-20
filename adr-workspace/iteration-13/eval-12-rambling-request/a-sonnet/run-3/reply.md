I wrote this up as ADR 3, Status Accepted, since the platform sync agreed on it:

`doc/adr/0003-generate-invoice-pdfs-in-background-jobs.md`

It records:
- the October incidents and the 41 tickets
- the two rejected options, a 120s timeout and a third-party PDF API
- the decision to use Sidekiq, the documents bucket and an email link
- the accepted downsides: no instant download, and a shared queue that affects the email team

I left out the idea of renaming the billing module. It is a separate topic and nobody has decided it. If you decide to do it, tell me and I'll write it as its own ADR.

Two things I did not fill in, because you didn't say:
- Is Accepted right, or did anyone still need to sign off? If so I'll change it to Proposed.
- Do you want the ADR to say who was in the sync, or who made the call? I left names out. I mentioned Rafael's and legal's positions only as the reasons the options were rejected.
