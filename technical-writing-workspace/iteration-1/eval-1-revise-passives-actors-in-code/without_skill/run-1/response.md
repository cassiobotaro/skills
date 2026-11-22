I rewrote `docs/pipeline.md` so each step names what performs it, using what I found in `exporter/`, `scripts/` and `deploy/`. I didn't run or test anything.

- **Intro:** it now lists the gateway, RabbitMQ, the worker, the notifier, S3 and SES, with the file each lives in.
- **Request:** the gateway's `validate_payload` returns `422` when `account_id` is missing and `413` above 100,000 rows. The old text only said "rejected". The gateway publishes valid requests to the `exports` queue and returns `202`.
- **Processing:** the worker's steps are numbered (build the CSV, encrypt it with Fernet, upload to S3, call the notifier). On failure, the worker republishes the job with an `x-attempts` header. After the third failure it publishes to `exports.dead`.
- **Dead-letter handling:** I added `scripts/requeue_dead.py` and the `ExportsDeadLetterHigh` alert, since the page didn't mention them.
- **Delivery:** the notifier asks S3 for a presigned URL and sends it through SES. S3 stops honoring the link after 24 hours. The old "the link is expired" had no actor.

**Needs your input — Backups:** nothing in the repo rotates backups, so I couldn't say who does it. I replaced the sentence with a TODO. Tell me what does the rotation (an S3 lifecycle rule or an AWS Backup plan, for example) and where it's configured, and I'll fill it in. Or delete the section if the claim is stale.
