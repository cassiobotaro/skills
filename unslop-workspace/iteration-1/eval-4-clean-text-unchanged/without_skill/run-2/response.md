The text is already clear and specific, so I'd leave it as it is:

> The worker pulls export jobs from RabbitMQ and writes each file to S3. A job that fails three times goes to the dead-letter queue, and the on-call engineer gets a page. Exports above 100,000 rows are not supported yet.

It has no filler, hedging, or stock phrases. It also gives concrete details: the queue, the storage, the retry count, who gets paged, and the row limit. Rewriting it would only make it less precise.
