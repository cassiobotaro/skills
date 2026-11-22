I wrote the ADR at `docs/adr/0001-iso-8601-utc-timestamps-in-public-api.md`. I haven't committed it.

The repo was empty, so there was no existing ADR convention. I picked `docs/adr/` with a numbered filename and a short MADR-style layout (Context, Decision, Consequences). If you already use a different location or template, tell me and I'll move or reformat it.

- **Context:** the repeated client timezone bugs and the unreadable epoch values in logs.
- **Decision:** all public API timestamps are ISO 8601 strings in UTC with a `Z` suffix, for both requests and responses.
- **Consequences:** the benefits are the removed timezone ambiguity and readable logs. The accepted costs are that clients must parse strings and payloads get slightly bigger.

I added two details you didn't give me:
- **`Z` suffix and request scope:** I wrote the `Z` suffix and said the rule covers both requests and responses. Check that both match what you decided.
- **Open points:** a short Notes section lists migration and versioning for existing clients, and whether fractional seconds are allowed. I marked these as not decided. Delete the section if you've already settled them.

The status is "Accepted" and the date is today, 2026-11-22. Adjust the date if the decision was made earlier.
