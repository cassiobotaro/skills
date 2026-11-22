# Export pipeline

This page describes what happens to an export request, and which component does each step:
the gateway (`exporter/gateway.py`), the worker (`exporter/worker.py`), and the notifier
(`exporter/notifier.py`).

## Request

When a client posts an export request to `/exports`, the gateway validates the payload. The
gateway rejects a request above 100,000 rows with a `413`. If the payload is valid, the
gateway publishes a job to the `exports` queue and returns a `202`.

## Processing

The worker takes the job from the `exports` queue and generates the CSV file. The worker
encrypts the file, then uploads it to the bucket. If any step fails, the worker publishes
the job back to the `exports` queue, up to three attempts in total. After the third failed
attempt, the worker publishes the job to the `exports.dead` queue instead.

## Delivery

Once the upload is done, the worker calls the notifier, which emails the download link to
the account. The link is a presigned S3 URL, and S3 refuses it after 24 hours.

## Backups

Backups of the bucket are rotated weekly. <!-- TODO: say who or what rotates them; nothing in the repository does. -->
