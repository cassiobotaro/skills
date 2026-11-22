I rewrote `docs/pipeline.md` in place so each step names the component that does it. I read the code to find each one and did not run any commands.

- **Request:** the gateway (`exporter/gateway.py`) validates the payload and rejects requests above 100,000 rows. It also publishes the job to the `exports` queue and returns the `202`.
- **Processing:** the worker (`exporter/worker.py`) generates the CSV, encrypts it, uploads it, retries failed jobs and moves them to the dead-letter queue.
- **Delivery:** the notifier (`exporter/notifier.py`) sends the email. The link now "expires after 24 hours", which the code does through an S3 presigned URL.

**Retry count changed.** The old text said "retried up to three times". `MAX_ATTEMPTS = 3` in the worker means three attempts in total: the first try plus two retries. I wrote "up to three attempts in total". If you meant three retries after the first try, the code is what's off.

**Backups still open.** "Backups of the bucket are rotated weekly" is unchanged. Nothing in the repository says what rotates the backups, and I didn't want to guess. Which job, lifecycle rule or team does it?

I assumed the reader is an engineer or on-call person who knows the system by name but not the order of its parts.
