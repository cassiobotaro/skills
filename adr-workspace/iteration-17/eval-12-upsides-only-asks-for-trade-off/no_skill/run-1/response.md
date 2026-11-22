FIRST REPLY (before any answer from the user):

I recorded the decision as a new ADR, `doc/adr/0003-serve-static-assets-through-cloudfront.md`. It follows the format of the existing ADRs, is dated 2026-11-22, and has status Accepted. I haven't committed it.

- **Context:** Asia users waited three to four seconds for first paint, and the assets are already fingerprinted.
- **Decision:** CloudFront goes in front of the static assets, with long-lived cache headers.
- **Consequences:**
  - Pages load faster for users far from our region.
  - The app servers stop serving static files.

I added two consequences you didn't mention. Caching forever only works while filenames stay fingerprinted, and CloudFront is new infrastructure to operate. The cache-header detail in the decision is also my inference from "cached forever". Edit those if they don't match what you intend.

-----

(The first turn already wrote a file, so the user's answer was never sent. The first reply is also the final reply.)
