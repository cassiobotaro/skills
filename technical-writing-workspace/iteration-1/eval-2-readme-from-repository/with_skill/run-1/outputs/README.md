# exporter

`exporter` generates CSV exports of account data in the background. A FastAPI gateway accepts an export request and puts a job on a RabbitMQ queue. A worker builds the CSV, encrypts it, uploads it to an S3 bucket, and emails the account a download link that expires after 24 hours.

This page covers how to run the service locally, how to call it, and where the rest of the documentation lives.

## Prerequisites

- Python 3.12 or later
- [uv](https://docs.astral.sh/uv/)
- A RabbitMQ broker that the gateway and the worker can reach
- An S3 bucket and AWS credentials that boto3 finds, with permission to put and presign objects in the bucket and to send email through SES

## Run it

1. Install the dependencies:

   ```
   make setup
   ```

2. Set the environment variables. The gateway needs `QUEUE_URL`. The worker needs all four.

   | Variable | Value |
   |---|---|
   | `QUEUE_URL` | AMQP URL of the RabbitMQ broker |
   | `EXPORT_BUCKET` | Name of the S3 bucket that stores the exports |
   | `EXPORT_KEY` | Fernet key that encrypts each file |
   | `MAIL_FROM` | Sender address for the download email |

3. In one terminal, start the gateway on port 8080:

   ```
   make run-gateway
   ```

4. In a second terminal, start the worker:

   ```
   make run-worker
   ```

5. In a third terminal, request an export:

   ```
   curl -X POST localhost:8080/exports \
     -H 'Content-Type: application/json' \
     -d '{"account_id": "acme", "rows": 10}'
   ```

   The gateway answers `202` with `{"status": "queued"}`. When the worker finishes, it sends the download link to `acme@accounts.example.com`.

The gateway answers `422` when the payload has no `account_id`, and `413` when `rows` is above 100,000.

## Test

```
make test
```

## Operate

- If a job fails three times, the worker moves it to the `exports.dead` queue. The `ExportsDeadLetterHigh` alert in `deploy/alerts.yaml` pages when that queue holds more than 10 messages for 5 minutes.
- To move dead messages back to `exports`, run `scripts/requeue_dead.py`. Add `--dry-run` to count the messages without moving them, and `--limit <n>` to move at most `<n>` messages (default 100). The script reads `QUEUE_URL`.

  ```
  uv run python scripts/requeue_dead.py --dry-run
  ```

## More documentation

- [Export pipeline](docs/pipeline.md): what happens to a request from the gateway to the email.

## License and support

<!-- TODO: the repository has no LICENSE file; state the license here. -->
<!-- TODO: say where to ask for help (team channel, issue tracker, or on-call contact). -->
