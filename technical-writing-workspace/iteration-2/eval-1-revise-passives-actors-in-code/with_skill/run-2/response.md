I edited `docs/pipeline.md` in place. Every action now names who does it, checked against `exporter/gateway.py`, `worker.py` and `notifier.py`:
- **Request:** the gateway validates and rejects the payload, then publishes the job to the `exports` queue.
- **Processing and delivery:** the worker builds, encrypts and uploads the CSV, retries the job, and moves it to `exports.dead` after the third failed attempt. The notifier emails the link.

Question for you: "Backups of the bucket are rotated weekly" is unchanged. Nothing in the repository says what rotates the backups, so I didn't guess. Which job or service does it, and where is it configured?

I assumed the reader is an engineer or on-call person who needs to know which component to look at. I ran no commands.
