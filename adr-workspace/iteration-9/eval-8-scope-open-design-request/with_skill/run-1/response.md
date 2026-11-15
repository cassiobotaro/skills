I haven't written an ADR yet, and I haven't touched `doc/adr`. An ADR records a decision the team has already made, along with its real reasons. Your message lists four open questions: which channels to support, whether to put a queue in front of the senders, how retries should work, and which team owns the service. If I wrote an ADR now, I would be inventing the decisions and the rationale behind them, and that would make the log misleading.

What you have is a design that is still being worked out, and that fits a design doc. If the `design-doc` skill is installed, it can walk you through the problem, the alternatives and the trade-offs for the notification service. Each question can become its own ADR once the team settles it. The log keeps one decision per ADR, so you would end up with separate records for channels, queueing, retry policy and ownership.

I can write ADRs as soon as any of these are decided, for example "we will put a queue in front of the senders, because ...". If you already have a concrete proposal that is waiting for sign-off, I can record it now with status `Proposed`. For either case I need:

1. What exactly was decided, or is being proposed (for example, queue technology, retry policy)?
2. Why now, and what alternatives were considered?
3. What downside is the team accepting?
4. Is it agreed (`Accepted`) or still awaiting agreement (`Proposed`)?
