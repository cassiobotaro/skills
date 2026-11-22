I edited `docs/pipeline.md` in place. Every step now names what does it: the gateway validates and publishes, the worker generates, encrypts, uploads and retries, and the notifier sends the email. I took each actor from `exporter/` and added the file path beside it. The structure and facts are unchanged.

I assumed the reader is an engineer or on-call person who needs to know which component to open.

One question is still open. The Backups line, "Backups of the bucket are rotated weekly", is untouched. Nothing in the repo shows what rotates the backups. Is it a bucket lifecycle rule, an external job, or a team? Once you tell me, I'll name it.

I didn't run any commands.
