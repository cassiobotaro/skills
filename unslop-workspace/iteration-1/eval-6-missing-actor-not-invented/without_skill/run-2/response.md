Here's a tightened version:

> Certificates are rotated every 90 days, and alerts fire when rotation fails. The keys were generated in the HSM.

What I changed:
- Cut "It is important to note that". It adds nothing.
- Merged the first two sentences, since the alert depends on the rotation.

I kept the passive voice because the paragraph doesn't say who or what does these things. I didn't want to guess. If you tell me, I can make it active. For example: who or what rotates the certificates (a cron job, cert-manager, an operator)? Who gets the alerts, and through which channel? Who generated the keys?
