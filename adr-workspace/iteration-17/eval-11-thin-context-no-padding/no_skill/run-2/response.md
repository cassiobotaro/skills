I wrote the ADR at `doc/adr/0003-store-user-uploads-in-s3.md`. It follows the format of the two existing ADRs and has status Accepted, dated 2026-11-22. I haven't committed it.

- **Context:** uploads are on the app servers' local disk, and the autoscaling group replaces instances without keeping their disks. Local disk also isn't shared between instances.
- **Decision:** uploads are written to and read from S3.
- **Consequences:** files survive instance replacement and every instance sees the same files. The cost is that every file read becomes a network call, which adds latency and makes the app depend on S3 availability. That is the downside you said you'd accepted.

I added one consequence you didn't mention: existing files on the current servers must be migrated to S3 before the autoscaling move. Remove that line if migration is already handled somewhere else.

I kept the ADR to what you told me. It doesn't mention alternatives such as a shared network filesystem, or mitigations such as caching or a CDN. If you considered any of those, tell me and I'll add them.
