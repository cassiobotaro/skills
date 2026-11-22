# Export pipeline

An export passes through three components: the gateway (`exporter/gateway.py`), a RabbitMQ
queue, and the worker (`exporter/worker.py`). The worker calls the notifier
(`exporter/notifier.py`) at the end.

## Request

The gateway handles `POST /exports`:

1. `validate_payload` rejects the request with `422` if `account_id` is missing, and with
   `413` if `rows` is above 100,000 (`MAX_ROWS`).
2. The gateway publishes the payload to the `exports` queue.
3. The gateway returns `202` with `{"status": "queued"}`.

## Processing

The worker consumes the `exports` queue. For each job it:

1. Generates the CSV file (`build_csv`).
2. Encrypts the CSV with Fernet, using the key in `EXPORT_KEY`.
3. Uploads the encrypted file to the `EXPORT_BUCKET` S3 bucket as
   `<account_id>/<delivery_tag>.csv.enc`.
4. Calls the notifier (see Delivery).

If any step raises an exception, the worker publishes the job again with an `x-attempts`
header that counts the attempts. After the third failed attempt (`MAX_ATTEMPTS`), the worker
publishes the job to the `exports.dead` queue instead. In all cases the worker then
acknowledges the original message.

An alert (`deploy/alerts.yaml`) pages the on-call engineer when `exports.dead` holds more
than 10 messages for 5 minutes. An operator moves dead jobs back to `exports` with
`scripts/requeue_dead.py` (`--dry-run` counts them, `--limit` caps how many move).

## Delivery

The notifier asks S3 for a presigned download URL that is valid for 24 hours
(`LINK_TTL_SECONDS`). It then sends the URL through SES, from `MAIL_FROM` to
`<account_id>@accounts.example.com`. Because the notifier runs inside the worker's retry
block, an email failure causes the job to run again, and the worker uploads a new file.

## Backups

<!-- TODO: nothing in this repository rotates bucket backups. Name who does it (a bucket
lifecycle rule? an infrastructure job?) and where it is configured. -->

Backups of the bucket are rotated weekly.
