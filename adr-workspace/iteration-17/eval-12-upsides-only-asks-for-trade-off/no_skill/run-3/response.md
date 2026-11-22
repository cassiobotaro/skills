FIRST REPLY (before any answer from the user):

I recorded the decision as ADR 3, in `doc/adr/0003-use-cloudfront-for-static-assets.md`. It follows the format of the two existing ADRs and has status Accepted, dated 2026-11-22. I haven't committed it.

- **Context:** Users in Asia waited three to four seconds for first paint, and the assets are already fingerprinted.
- **Decision:** CloudFront goes in front of the static assets, and the app servers stop serving them.
- **Consequences:** Pages load faster for users far from our region, and the app servers carry less load.

I added two consequences you didn't mention, so check that you agree with them:
- Assets cached forever need a new fingerprinted filename on every change, and anything not fingerprinted needs a shorter cache lifetime.
- CloudFront becomes a new dependency, with its own configuration and cost.

-----

(The first turn already wrote a file, so the user's answer was never sent. The first reply is also the final reply.)
