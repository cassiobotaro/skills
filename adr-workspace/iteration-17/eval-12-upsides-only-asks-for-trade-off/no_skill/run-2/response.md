FIRST REPLY (before any answer from the user):

I recorded the decision as ADR 3 in `doc/adr/0003-serve-static-assets-through-cloudfront.md`, following the format of the existing ADRs. It's marked Accepted and dated 2026-11-22. I haven't committed it.

- **Context:** Users in Asia waited three to four seconds for first paint. The assets are already fingerprinted, so they can be cached forever.
- **Decision:** CloudFront goes in front of the static assets, with long-lived cache headers.
- **Consequences:** Pages load faster for users far from our region, and the app servers stop serving static files.

I added one consequence you didn't mention. Since assets are cached forever, they must always keep fingerprinted filenames, or users will get stale files. Remove that line if you'd rather not state it.

-----

(The first turn already wrote a file, so the user's answer was never sent. The first reply is also the final reply.)
