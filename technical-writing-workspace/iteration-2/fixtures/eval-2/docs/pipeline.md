# Export pipeline

This page describes what happens to an export request.

## Request

When an export is requested, the payload is validated. Requests above 100,000 rows are
rejected. If the payload is valid, a job is enqueued and a `202` is returned.

## Processing

The job is picked up and the CSV file is generated. The file is encrypted before it is
uploaded to the bucket. If something goes wrong, the job is retried up to three times,
after which it is moved to the dead-letter queue.

## Delivery

Once the upload is done, a download link is sent by email. The link is expired after
24 hours.

## Backups

Backups of the bucket are rotated weekly.
