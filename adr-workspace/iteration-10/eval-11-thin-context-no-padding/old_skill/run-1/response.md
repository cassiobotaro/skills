I wrote the ADR as `doc/adr/0003-store-user-uploaded-files-in-s3.md` (status Accepted, dated 2026-11-15). It follows the existing log, where 0002 is the latest record.

- **Context:** uploads live on the app servers' local disk. Next quarter the servers move into an autoscaling group, and instances there are replaced without keeping their disks.
- **Decision:** we will store user-uploaded files in S3.
- **Consequences:** files no longer depend on any single server's lifetime. The accepted downside is that every file read becomes a network call.

I added only what you told me. I didn't include alternatives, latency figures or migration steps, since you didn't give any. If you want those recorded, send them and I'll add them.
