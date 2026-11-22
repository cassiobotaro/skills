# Export pipeline

An export passes through two services and two AWS services: the gateway (`exporter/gateway.py`)
accepts the request, RabbitMQ holds the job, the worker (`exporter/worker.py`) builds and uploads
the file, and the notifier (`exporter/notifier.py`, called by the worker) emails the link.

## Request

`POST /exports` in the gateway:

1. `validate_payload` rejects the request with `422` if `account_id` is missing, and with `413`
   if `rows` is above 100,000 (`MAX_ROWS`).
2. If the payload is valid, the gateway publishes it to the `exports` queue in RabbitMQ and
   returns `202` with `{"status": "queued"}`.

## Processing

The worker consumes the `exports` queue. For each job it:

1. Builds the CSV in memory (`build_csv`).
2. Encrypts the CSV with Fernet, using the key in `EXPORT_KEY`.
3. Uploads the encrypted file to the S3 bucket in `EXPORT_BUCKET`, under
   `<account_id>/<delivery_tag>.csv.enc`.
4. Calls the notifier (see Delivery).

If any step raises, the worker publishes the job back to `exports` with an incremented
`x-attempts` header. On the third failure (`MAX_ATTEMPTS`) it publishes the job to the
`exports.dead` queue instead. The worker acknowledges the original message in both cases.

To move dead-lettered jobs back to `exports`, run `scripts/requeue_dead.py` (`--dry-run` counts
without moving, `--limit` caps the number moved, default 100). Prometheus fires the
`ExportsDeadLetterHigh` alert (`deploy/alerts.yaml`) and pages when `exports.dead` holds more
than 10 messages for 5 minutes.

## Delivery

After the upload, the notifier asks S3 for a presigned download URL and sends it with SES to
`<account_id>@accounts.example.com`. S3 stops honoring the URL after 24 hours
(`LINK_TTL_SECONDS`).

## Backups

TODO: unverified. Nothing in this repository rotates bucket backups, so the previous claim
("backups are rotated weekly") has no actor. Name who does it (for example an S3 lifecycle rule
or an AWS Backup plan) and where it is configured.
