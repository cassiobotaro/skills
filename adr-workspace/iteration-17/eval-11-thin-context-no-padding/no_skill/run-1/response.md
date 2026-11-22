I wrote the ADR at `doc/adr/0003-store-user-uploads-in-s3.md`. It follows the format of the two existing ADRs and has status Accepted, dated 2026-11-22.

- **Context:** Uploads sit on app-server local disk. Next quarter the servers move into an autoscaling group, where instances are replaced without keeping their disks.
- **Decision:** Store user-uploaded files in S3.
- **Consequences:**
  - Uploads survive instance replacement.
  - Every file read becomes a network call, which adds latency and makes us depend on S3 availability. You said you'd accepted this downside.

The last consequence is my addition, not something you told me: files already on local disks need to be migrated to S3 before the move to the autoscaling group. Remove it if a migration isn't planned or is handled elsewhere.

I didn't commit it.
