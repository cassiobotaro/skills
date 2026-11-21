The text has no hits, so I'm returning it unchanged.

The worker pulls export jobs from RabbitMQ and writes each file to S3. A job that fails three times goes to the dead-letter queue, and the on-call engineer gets a page. Exports above 100,000 rows are not supported yet.
