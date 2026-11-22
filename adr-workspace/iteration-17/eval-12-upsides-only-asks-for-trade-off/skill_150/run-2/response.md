FIRST REPLY (before any answer from the user):

Before I write this up, I need to know what the team accepted as the downside. You've given me the decision and the reasons, but everything so far is a benefit. An ADR's Consequences section should list the costs too, and I don't want to invent them.

1. **Trade-offs:** What gets harder or riskier with CloudFront in front of the static assets? Some possibilities are a new dependency and cost, cache invalidation or deploy steps, or extra configuration for the CDN domain. Which of these did the team actually weigh, and did it accept any others?
2. **Alternatives:** Did you consider anything else, such as a different CDN, a second region, or doing nothing? If so, I'll record why you passed on it. If not, I'll leave alternatives out.
3. **Status:** Is this agreed (`Accepted`), or still waiting on someone's sign-off (`Proposed`)?

Once you answer, I'll write it as `doc/adr/0003-…md`, following ADR 2 in your log.

-----

THE USER'S ANSWER:

That is everything we have on this one; nothing else was discussed. Please record it now with what I gave you.

-----

FINAL REPLY:

I recorded the decision as ADR 3, using only what you gave me. I didn't commit it.

The file is `doc/adr/0003-put-cloudfront-in-front-of-static-assets.md`, dated 2026-11-22 with status `Accepted`.

- **Context:** Asia users waited three to four seconds for first paint. The assets are fingerprinted, so they can be cached indefinitely. The app servers currently serve them.
- **Decision:** We will put CloudFront in front of the static assets and cache them with a long lifetime.
- **Consequences:** Pages should load faster for users far from the region, and the app servers stop serving static files. I also added a line saying no trade-offs or alternatives were discussed, so the record doesn't read as if there were none. If costs or problems turn up later, a new ADR can cover them. I left ADRs 1 and 2 untouched.
