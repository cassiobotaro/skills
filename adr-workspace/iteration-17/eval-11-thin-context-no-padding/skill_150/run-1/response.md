I wrote the ADR as `doc/adr/0003-store-user-uploaded-files-in-s3.md`, with status Accepted and today's date, 2026-11-22. It follows the existing log, which already had 0001 (record architecture decisions) and 0002 (PostgreSQL), so it is number 3. No other file was touched.

- **Context:** uploads currently sit on the app servers' local disks, and the autoscaling group next quarter replaces instances without keeping their disks.
- **Decision:** "We will store user-uploaded files in S3 instead of on the app servers' local disk."
- **Consequences:**
  - Files no longer depend on any one instance's lifetime.
  - Every file read becomes a network call, which is the downside you accepted.
  - Existing files on local disks have to be moved to S3 before those instances are replaced.

The third consequence is my inference from "moving", not something you said. Check it and edit or drop it if it's wrong. I added nothing about alternatives, latency numbers or caching, since you didn't give any. If you want those recorded, tell me and I'll add them.
