# Export pipeline

This page describes what happens to an export request.

## Request

When a client requests an export, the gateway validates the payload. The gateway rejects
requests above 100,000 rows. If the payload is valid, the gateway publishes a job to the
`exports` queue and returns a `202`.

## Processing

The worker picks up the job and generates the CSV file. The worker encrypts the file before
it uploads the file to the bucket. If something goes wrong, the worker tries the job again,
up to three attempts in total. After the third failed attempt, the worker moves the job to
the dead-letter queue.

## Delivery

Once the worker has uploaded the file, the notifier sends a download link by email. The
link expires after 24 hours.

## Backups

Backups of the bucket are rotated weekly.
