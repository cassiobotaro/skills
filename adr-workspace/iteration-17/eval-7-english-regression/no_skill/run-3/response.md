I wrote the ADR at `docs/adr/0001-iso-8601-utc-timestamps-in-public-api.md`. The repo was empty, so there was no existing ADR convention. I chose the common `docs/adr/NNNN-title.md` layout with Context, Decision and Consequences sections. I haven't committed it.

It records your decision, the two reasons (repeated client timezone bugs, and epoch integers being unreadable in logs), and the two trade-offs you accepted (clients parse strings, payloads get slightly bigger).

I added a few things you didn't give me, so please check them:
- **Status and date:** I set the status to Accepted and the date to today, 2026-11-22.
- **Format:** I specified the `Z` suffix (for example `2026-11-22T14:30:00Z`) and said it applies to both requests and responses.
- **Examples:** I gave "mixing up seconds and milliseconds" and "incorrect local-time conversions" as examples of the client bugs. Replace them with the real incidents if they differ.
- **Payload size:** I wrote roughly 20 bytes per timestamp against 10 for an epoch integer.
- **Open questions:** A short Notes section lists migration for existing epoch-based clients, and whether fractional seconds are allowed. I left both undecided.
