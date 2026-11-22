# Export pipeline

This page describes what happens to an export request.

## Request

When a client requests an export, the gateway validates the payload. The gateway rejects
requests above 100,000 rows. If the payload is valid, the gateway enqueues a job in the
`exports` queue and returns `202`.

## Processing

The worker picks up the job and generates the CSV file. The worker encrypts the file
before it uploads the file to the bucket. If any step fails, the worker retries the job up
to three times, then moves it to the dead-letter queue (`exports.dead`).

## Delivery

Once the upload is done, the notifier emails a download link. The link expires after
24 hours.

## Backups

Backups of the bucket are rotated weekly.
