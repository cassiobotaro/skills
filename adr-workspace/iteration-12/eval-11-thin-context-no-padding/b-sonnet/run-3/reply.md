I wrote ADR 3, "Store user-uploaded files in S3", as `outputs/doc/adr/0003-store-user-uploaded-files-in-s3.md`. Its status is Accepted and it is dated 2026-11-20. It follows ADRs 1 and 2 in your existing `doc/adr` log. Nothing else in the log was touched.

The Context and Consequences hold only what you told me: the move from local disk to S3, the autoscaling group next quarter, instances being replaced without their disks, and the accepted cost that every file read becomes a network call. I added no latency figures, alternatives or cost details, because I had none from you.

If you want the ADR to say more, these questions would fill it in. I left them out rather than guess:
1. Did you consider other options, such as a shared network filesystem, and why were they rejected?
2. Is there a plan for the existing files already on local disk, or for caching reads? If so, that probably belongs in a separate ADR.
3. Has everyone agreed? If not, I can change the status to Proposed.
