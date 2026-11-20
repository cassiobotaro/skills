I added ADR 3, "Store user-uploaded files in S3", to your existing log in `doc/adr/`. Its status is Accepted and it is dated 2026-11-20. The file is `doc/adr/0003-store-user-uploaded-files-in-s3.md`.

It records only what you told me. The Context says the files currently live on the app servers' local disk, and that the servers move into an autoscaling group next quarter where instances are replaced without keeping their disks. The Decision is to store the files in S3. The Consequences are that files no longer depend on a single server, and that every file read becomes a network call, which the team accepted.

I did not add latency figures, cost, or migration steps, because you didn't give any. If you want any of these in the record, tell me and I'll add them:

1. How will the existing files on local disk get to S3, and is that migration part of this decision?
2. Were other options considered, such as a shared network filesystem? If so, I can add why they lost.
3. Is this agreed across the team, or should it be Proposed instead of Accepted?
