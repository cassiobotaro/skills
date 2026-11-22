I wrote `README.md` at the repo root. It covers what `exporter` does, how to run it locally, how failed jobs are retried and requeued, and how to run the tests. I haven't run any of the commands in it, because they need RabbitMQ and AWS.

I assumed the reader is an engineer who runs or maintains this service. I took every command, variable name, port, and limit from the `Makefile`, the code, `scripts/requeue_dead.py`, and `deploy/alerts.yaml`.

Open questions:
- **License and support:** the repo has no license file and no contribution guide or support channel. I left those sections out instead of guessing. Tell me the license and where to ask for help, and I'll add them.
- **Bucket backups:** `docs/pipeline.md` says "Backups of the bucket are rotated weekly" but doesn't say who or what does it, and nothing in the repo shows it. I left that out of the README.
- **Pipeline doc passives:** `docs/pipeline.md` has other passives with no actor, such as "the payload is validated" and "the link is expired". The code answers them (the gateway validates, and the link is a presigned S3 URL), but I didn't edit that file. I can revise it if you want.
- **AWS setup:** the code reads AWS credentials from `boto3`'s default lookup, and the repo doesn't say which region or IAM permissions it needs. The README only says the credentials need access to S3 and SES.
