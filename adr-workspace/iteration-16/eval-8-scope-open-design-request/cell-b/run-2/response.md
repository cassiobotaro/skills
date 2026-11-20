I haven't written the ADR yet, because nothing has been decided. An ADR records a decision and the real reasons behind it. What you described is four open questions: channels, a queue in front of the senders, retry behavior, and ownership. If I filled in answers, I'd be inventing the rationale, and that would mislead whoever reads the log later. I also haven't created `doc/adr/` or any files.

Some of these are also separate decisions, and each ADR should record one. Queue versus no queue, retry policy, and channel scope would each be their own record. Team ownership is usually organizational and may not need an ADR at all. A design doc is the better place to explore options, and the ADRs can come out of it once choices are made.

Here is what I need to write the ADR(s). Answer whichever apply:

1. **Which decision is settled first?** For example, "we will put a queue (Kafka/SQS/RabbitMQ/…) in front of the senders" or "we will support email, SMS and push at launch". If none are settled, I can write the ADR with status `Proposed` and the options listed as open. That needs the options on the table and the forces behind them.
2. **Why now, and what is wrong with the status quo?** What pushes you to build a notification service, and what do the services do today?
3. **What alternatives were considered, and what downside is the team willing to accept?** For example, a queue adds operational cost but gives you buffering and retry isolation. I need your actual trade-offs, not generic ones.
4. **Has everyone agreed?** If not, I'll use `Proposed`. If so, `Accepted`.

The repository is empty, so I will start a fresh log. I'll create `doc/adr/` and seed `0001-record-architecture-decisions.md`. Your decision will be `0002`, and any further decisions will be `0003` and so on. Tell me if you'd rather use a different directory.
