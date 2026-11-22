# Export pipeline

This page describes what happens to an export request.

## Request

When a client requests an export, the gateway validates the payload. The gateway rejects
requests above 100,000 rows. If the payload is valid, the gateway enqueues a job on the
`exports` queue and returns `202`.

## Processing

The worker picks up the job from the `exports` queue and generates the CSV file. The
worker encrypts the file before it uploads the file to the bucket. If something goes
wrong, the worker puts the job back on the queue. After three failed attempts, the worker
moves the job to the dead-letter queue (`exports.dead`).

## Delivery

Once the upload is done, the worker calls the notifier, which emails a download link. The
link expires after 24 hours.

## Backups

Backups of the bucket are rotated weekly.
