I wrote ADR 3, "Store user-uploaded files in S3", as `doc/adr/0003-store-user-uploaded-files-in-s3.md`. Its status is Accepted and it is dated 2026-11-20. It follows ADR 2 in your existing log.

- **Context:** the files sit on local disk today, the app servers join an autoscaling group next quarter, and instances there are replaced without keeping their disks.
- **Decision:** we will store user-uploaded files in S3.
- **Consequences:** files no longer depend on a single server's life, and every file read becomes a network call, which the team accepted.

I included only what you told me. I left out migration of existing files, caching, cost, and alternatives you considered, because you didn't mention them.

If any of those shaped the decision, tell me and I can add them. The ADR is Accepted now. If it still needs sign-off, I can change it to Proposed.
