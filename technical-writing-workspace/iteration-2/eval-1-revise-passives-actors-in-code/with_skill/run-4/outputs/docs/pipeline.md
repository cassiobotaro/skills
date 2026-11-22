# Export pipeline

This page describes what happens to an export request.

## Request

When a client requests an export, the gateway (`exporter/gateway.py`) validates the
payload. It rejects requests above 100,000 rows. If the payload is valid, the gateway
publishes a job to the `exports` queue and returns a `202`.

## Processing

The worker (`exporter/worker.py`) takes the job from the `exports` queue and generates the
CSV file. The worker encrypts the file before it uploads it to the bucket. If something
goes wrong, the worker republishes the job to `exports` for another attempt, up to three
attempts in total. After the third failure, the worker moves the job to the `exports.dead`
queue.

## Delivery

Once the upload is done, the notifier (`exporter/notifier.py`) sends a download link by
email through SES. The link expires after 24 hours.

## Backups

Backups of the bucket are rotated weekly.
