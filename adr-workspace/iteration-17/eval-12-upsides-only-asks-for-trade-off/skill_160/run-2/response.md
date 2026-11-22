FIRST REPLY (before any answer from the user):

I haven't written the ADR yet. You gave me the decision and the reasons, but not what it costs or what you passed over. That trade-off is what makes the record useful to someone reading it later, and I don't want to make one up.

I have four quick questions:

1. **Alternatives:** Did you consider anything else, such as a different CDN, a second region, or leaving things as they are? If so, why did you pass on it?
2. **Cost:** What are you taking on in exchange? This could be CDN spend, invalidation or deploy changes, or something else. If there's no real downside, say so and I'll record it that way.
3. **Status:** Is this agreed (`Accepted`), or still waiting on sign-off (`Proposed`)?
4. **Numbers:** Is "three to four seconds for first paint" the figure you want recorded as is?

Once you answer, I'll write it as `doc/adr/0003-…md`. The next number is 3, after the existing 0001 and 0002.

-----

THE USER'S ANSWER:

That is everything we have on this one; nothing else was discussed. Please record it now with what I gave you.

-----

FINAL REPLY:

I recorded the decision as ADR 3 with status `Accepted`, dated 2026-11-22. I didn't edit any existing ADR.

The file is `doc/adr/0003-put-cloudfront-in-front-of-static-assets.md`.

- **Context:** Asia users waited three to four seconds for first paint, and the assets are already fingerprinted, so they can be cached indefinitely.
- **Decision:** We will put CloudFront in front of the web app's static assets.
- **Consequences:** Pages should load faster for users far from the region, and the app servers stop serving static files.

The record has no trade-off. You said nothing else was discussed, so there are no alternatives or costs in it. I added a closing line to Consequences saying that, so a future reader knows it wasn't left out by accident. If you later find a cost, or an alternative you passed over, a new ADR that amends this one can add it. I can write that when you're ready.
