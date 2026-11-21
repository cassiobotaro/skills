Here's a tightened version:

> Certificates rotate every 90 days, and an alert fires if rotation fails. The keys were generated in the HSM.

What I changed:
- Removed "It is important to note that". It adds no information.
- Merged the first two sentences, since the alert depends on the rotation.
- Switched "are rotated" to "rotate" and "Alerts are sent" to "an alert fires". This drops the passive voice without needing to name an actor.

I didn't name who or what rotates the certificates, sends the alerts, or generated the keys. The original doesn't say, so I left it out rather than guess. If you add those details, the runbook gets more useful. For example, "cert-manager rotates certificates every 90 days and pages the on-call team if rotation fails." Who generated the keys, and who gets the alert, are the gaps worth filling.
