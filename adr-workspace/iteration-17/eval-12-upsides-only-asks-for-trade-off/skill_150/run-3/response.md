FIRST REPLY (before any answer from the user):

I haven't written the ADR yet. The log is at `doc/adr/`, and this would be `0003-put-cloudfront-in-front-of-static-assets.md`. I need one thing from you first.

You gave me the decision and the reasons: Asia users wait three to four seconds for first paint, the assets are fingerprinted so they can be cached forever, and the app servers stop serving static files. The Consequences section also has to list what gets harder or riskier, and so far you've only named benefits. I don't want to make up the downsides for you.

- **What did the team accept as a trade-off?** Examples would be new cost, another piece of infrastructure to run, or how cache invalidation and deploys work. Tell me which ones actually apply.
- **Were other options considered?** For example, a different CDN, or serving from more regions. This is optional. I'll leave it out if you say there weren't any.
- **Is this settled, or still waiting on someone's sign-off?** I'll record it as `Accepted` unless you say it's pending, in which case it's `Proposed`.

Once you answer, I'll write the file.

-----

THE USER'S ANSWER:

That is everything we have on this one; nothing else was discussed. Please record it now with what I gave you.

-----

FINAL REPLY:

I recorded the decision as ADR 3, status `Accepted`, dated 2026-11-22:

`doc/adr/0003-put-cloudfront-in-front-of-static-assets.md`

- **Context:** Asia users waited three to four seconds for first paint, and the assets are already fingerprinted so they can be cached indefinitely.
- **Decision:** "We will put CloudFront in front of the web app's static assets."
- **Consequences:** Pages should load faster for users far from our region, and the app servers no longer serve static files.

You said no trade-offs were discussed, so the Consequences section lists only benefits. A decision with no downsides is unusual, so you may want to add the costs later. Because accepted ADRs aren't edited, the way to do that is a new ADR that amends this one.

I didn't touch any other files.
