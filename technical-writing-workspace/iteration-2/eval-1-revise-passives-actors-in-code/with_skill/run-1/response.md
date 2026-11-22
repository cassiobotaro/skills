I edited `docs/pipeline.md` in place. Each step now names the component that does it, taken from `exporter/gateway.py`, `worker.py` and `notifier.py`. The gateway validates, rejects and enqueues. The worker generates, encrypts, uploads and retries. The notifier emails the link. The queue is named `exports` and the dead-letter queue `exports.dead`. The structure and facts are unchanged.

Questions for you:
- **Backups:** "Backups of the bucket are rotated weekly" has no actor, and nothing in the repository says who rotates them (a bucket lifecycle rule, a cron job, or another team). I left the sentence as it was. Who does it?
- **Link expiry:** The link is an S3 presigned URL with a 24-hour TTL. I wrote "The link expires after 24 hours" because the link expires by itself. Tell me if you want S3 named as the actor.

I assumed the reader is an engineer or on-call responder who is new to this service. I ran no commands.
