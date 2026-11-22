I wrote the ADR as `doc/adr/0003-store-user-uploads-in-s3.md`, following the format of the two existing ADRs. Its status is Accepted and it's dated 2026-11-22. I haven't committed it.

- **Context:** uploads sit on app-server local disk, and the autoscaling group replaces instances without keeping their disks.
- **Decision:** uploads are written to and read from S3.
- **Consequences:**
  - Files no longer depend on any single instance.
  - Every file read becomes a network call, which means more latency and a new dependency on S3 availability. The ADR says the team accepts this.

The migration line is my own addition, since you didn't mention it. The ADR says existing local files must be moved to S3 before the servers join the autoscaling group. Delete that line if migration is already handled elsewhere.

I left out details I couldn't confirm from the repo, such as bucket setup, a CDN or caching layer, and access control. If you plan to mitigate the read cost, for example with CloudFront or local caching, I can add that.
