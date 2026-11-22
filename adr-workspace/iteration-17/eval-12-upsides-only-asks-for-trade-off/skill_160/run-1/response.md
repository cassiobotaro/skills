FIRST REPLY (before any answer from the user):

Before I write this, I need one thing from you. I have the decision (CloudFront in front of the static assets) and the forces (Asia first paint of 3–4 seconds, fingerprinted assets that can be cached forever). I also have what gets better: faster loads far from your region, and app servers that no longer serve static files. I don't have the trade-off.

- **What did you give up or pass over?** For example, another CDN or serving from the app servers in more regions, or a cost or constraint you're taking on, such as a new AWS dependency, cache invalidation, or deploy changes.
- **Is this settled, or still waiting on someone's agreement?** I'll record it as `Accepted` unless you say it's still a proposal.

If there was no alternative or cost, say so. I'll write the record with what you've given me and note that it has no trade-off.

The log is in `doc/adr/`. This will be ADR 3, `0003-…md`.

-----

THE USER'S ANSWER:

That is everything we have on this one; nothing else was discussed. Please record it now with what I gave you.

-----

FINAL REPLY:

I recorded the decision as ADR 3, with status `Accepted` and today's date, 2026-11-22. The file is `doc/adr/0003-serve-static-assets-through-cloudfront.md`. I didn't edit any other file.

- **Context:** Asia users wait three to four seconds for first paint, and the assets are already fingerprinted, so they can be cached forever.
- **Decision:** "We will put CloudFront in front of the web app's static assets."
- **Consequences:** Pages load faster for users far from your region, and the app servers stop serving static files.

This record has no trade-off. You said no alternatives or costs were discussed, so I didn't add any. If you later think of a cost, such as cache invalidation or the new AWS dependency, that would be a new ADR rather than an edit to this one.
