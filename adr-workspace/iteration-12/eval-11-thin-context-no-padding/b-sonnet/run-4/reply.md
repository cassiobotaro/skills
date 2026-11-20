I wrote ADR 3, "Store user-uploaded files in S3", as Accepted. It is in `doc/adr/0003-store-user-uploaded-files-in-s3.md`, after the existing ADRs 1 and 2. I used today's date, 2026-11-20.

It records only what you told me. The reason is that the app servers move into an autoscaling group next quarter and replaced instances lose their disks. The accepted downside is that every file read becomes a network call. I left out anything beyond that, such as alternatives, latency figures, migration plan, or caching, because you didn't give me any.

Optional questions, if you want the record fuller:
- Were other options considered, such as a shared network filesystem? If so, I can add why they lost.
- How will the existing files on local disk be migrated? That may deserve its own ADR.
- Is this agreed, or still awaiting sign-off? If it is still pending, I'll change the status to Proposed.
