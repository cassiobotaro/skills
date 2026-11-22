FIRST REPLY (before any answer from the user):

I haven't written the ADR yet. The decision and the reasons are clear, but you've only given me the upsides, and an ADR needs the costs too.

What downside did the team accept by putting CloudFront in front of the static assets? Some possible areas, which are only prompts and not facts I'll assume:

- Added cost or a new vendor dependency.
- How you'll invalidate or roll back assets.
- Anything about deployment, cache configuration or debugging that gets harder.

If you also considered alternatives, such as another CDN or serving from more regions, tell me and I'll add them. Otherwise I'll record only what you've said.

Once you answer, I'll add `doc/adr/0003-…`, following `0002-use-postgresql-for-persistence.md` and marked `Accepted`. Say so if the decision is still waiting on someone's agreement, and I'll mark it `Proposed`.

-----

THE USER'S ANSWER:

That is everything we have on this one; nothing else was discussed. Please record it now with what I gave you.

-----

FINAL REPLY:

I recorded the decision as ADR 3 in `doc/adr/0003-put-cloudfront-in-front-of-static-assets.md`.

It is dated 2026-11-22 and marked `Accepted`. It follows the format of the existing records, and I didn't edit the other two.

- **Context:** Users in Asia waited three to four seconds for first paint, and the assets are already fingerprinted so they can be cached indefinitely.
- **Decision:** We will put CloudFront in front of the web app's static assets and cache them with no expiry.
- **Consequences:** Pages load faster for users far from the region, and the app servers stop serving static files.

The Consequences section lists only the benefits you gave me, because you said nothing else was discussed. I didn't invent any downsides, so the record doesn't show a trade-off. If the team later identifies costs or risks, they can go into a new ADR that amends this one.
