I wrote the ADR as `doc/adr/0003-store-user-uploaded-files-in-s3.md`. It's the next number after the existing `0001` and `0002`, status `Accepted`, dated 2026-11-22. It matches the format of the existing records. Nothing else in the log changed, because no earlier ADR covers file storage, so there's nothing to supersede.

- **Context:** Uploaded files sit on the app servers' local disks. Next quarter those servers move into an autoscaling group where instances are replaced without keeping their disks.
- **Decision:** We will store user-uploaded files in S3 instead of on the app servers' local disk.
- **Consequences:**
  - Files no longer depend on any one instance's lifetime.
  - Every file read becomes a network call to S3, which is the downside you accepted.
  - Existing files on local disks have to be moved to S3 before those instances are replaced. I took that from your word "moving", so check you're happy with it.

I recorded only the reasons you gave. I didn't add alternatives, latency figures, or a migration plan. If you considered other options, such as a shared network filesystem, or want specific mitigations recorded, tell me. A new ADR is better for those than editing this one afterwards.
