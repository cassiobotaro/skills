I wrote the ADR as `doc/adr/0003-store-user-uploaded-files-in-s3.md`, status Accepted, dated 2026-11-15. It follows ADR 2 in the existing log.

- **Context:** uploads sit on the app servers' local disk. Next quarter the servers move into an autoscaling group, where replaced instances lose their disks.
- **Decision:** we will store user-uploaded files in S3.
- **Consequences:** files no longer depend on any one server's lifetime. Every file read becomes a network call, which is the downside you accepted.

I kept it to what you told me. I did not add alternatives, latency figures or a migration plan, since you didn't give any. If you want those recorded, send them and I'll add them before the ADR is committed.
