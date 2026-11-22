FIRST REPLY (before any answer from the user):

I haven't written the ADR yet. The log is `doc/adr/`, it's at 0002, and this one would be 0003. Before I write it I need one thing from you.

**What did the team give up or accept in exchange for putting CloudFront in front of the static assets?** For example, an alternative you passed over (another CDN, or serving from the app servers or a regional replica), a new cost or dependency, or something that gets harder, like cache invalidation, deploy steps, or debugging. If there was no trade-off, say so and I'll record it that way.

I have the decision, the forces (Asia users waiting 3–4 seconds for first paint, and fingerprinted assets that can be cached forever) and the benefits (faster loads far from your region, and app servers no longer serving static files). I won't invent a cost or an alternative for the record.

Is this decision final (`Accepted`), or does it still need sign-off (`Proposed`)? I'll assume `Accepted` unless you tell me otherwise.

-----

THE USER'S ANSWER:

That is everything we have on this one; nothing else was discussed. Please record it now with what I gave you.

-----

FINAL REPLY:

I recorded the decision as ADR 3 at `doc/adr/0003-serve-static-assets-through-cloudfront.md`, with status `Accepted` and today's date, 2026-11-22. It follows the format of the existing records in `doc/adr/`. I didn't touch any other file.

- **Context:** Asia users waited three to four seconds for first paint, and the assets are already fingerprinted, so they can be cached indefinitely.
- **Decision:** We will put CloudFront in front of the web app's static assets.
- **Consequences:** Pages load faster for users far from your region, and the app servers no longer serve static files.

The record has no trade-off, because you said nothing else was discussed. I didn't add a cost or an alternative. If one comes up later, such as cache invalidation or the cost of the service, it belongs in a new ADR that supersedes this one, because accepted records aren't edited.
