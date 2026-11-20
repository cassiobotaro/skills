I haven't written an ADR, and I haven't created anything in `doc/adr`. The notification service is still in the design phase, and an ADR records a decision the team has already made. You listed four open questions: which channels to support, whether to put a queue in front of the senders, how retries should work, and which team owns it. If I wrote an ADR now, I would have to invent the decision and its reasons, and that would mislead whoever reads the log later.

A design doc fits this stage better. It can lay out the problem, compare the options for each question (channels, queue or no queue, retry strategy, ownership) and record the trade-offs. If the `design-doc` skill is installed, I can start there.

Once the team settles a question, each answer can become its own ADR. Two cases:
- **Decision made:** tell me the choice and the reasons, for example "we will put a queue in front of the senders because…". I'll write it as `Accepted`.
- **Concrete proposal awaiting agreement:** I can write it as `Proposed`.

Each decision gets a separate ADR, so these four questions would become up to four records. If you want to use the ADR log before then, tell me which decisions are already made.
