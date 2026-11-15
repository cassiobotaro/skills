I wrote ADR 3 in your existing log:

- `doc/adr/0003-store-user-uploaded-files-in-s3.md` (Status: Accepted, dated 2026-11-15)

It records the decision to store user-uploaded files in S3 instead of on the app servers' local disk. The context is your reason: the app servers move into an autoscaling group next quarter, and instances there are replaced without keeping their disks. The consequences list the benefit and the downside you accepted, that every file read becomes a network call.

I kept it to what you told me and added no alternatives, numbers or mitigations. If you want any of those in the record, such as the alternatives you rejected or a caching plan for reads, tell me and I'll add them in a follow-up.
