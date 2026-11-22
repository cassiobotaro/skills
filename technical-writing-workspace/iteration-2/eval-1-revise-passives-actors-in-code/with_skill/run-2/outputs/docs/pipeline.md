# Export pipeline

This page describes what happens to an export request.

## Request

When a client requests an export, the gateway (`exporter/gateway.py`) validates the payload.
The gateway rejects requests above 100,000 rows. If the payload is valid, the gateway
publishes a job to the `exports` queue and returns a `202`.

## Processing

The worker (`exporter/worker.py`) picks up the job and generates the CSV file. The worker
encrypts the file before it uploads the file to the bucket. If something goes wrong, the
worker republishes the job to the `exports` queue, up to three attempts in total. After the
third failed attempt, the worker publishes the job to the dead-letter queue, `exports.dead`.

## Delivery

Once the upload is done, the worker calls the notifier (`exporter/notifier.py`), which emails
a download link to the account. The link expires after 24 hours.

## Backups

Backups of the bucket are rotated weekly.
