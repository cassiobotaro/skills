I wrote ADR 3, "Store user-uploaded files in S3", at doc/adr/0003-store-user-uploaded-files-in-s3.md. Its status is Accepted. The log already had ADRs 1 and 2, so this one takes the next number.

The Context and Consequences hold only what you told me: files are on local disk, the app servers move to an autoscaling group next quarter, and instances there are replaced without keeping their disks. The accepted downside is that every file read becomes a network call. I did not add anything else, such as alternatives, costs or migration steps.

Two optional questions. Answer them only if you want them in the record:
1. Were other options considered, such as EFS or a shared volume? If so, I can add why S3 won.
2. Is there a plan for migrating the existing files, or for mitigating the read latency, for example a CDN or caching? I can add it to Consequences.
