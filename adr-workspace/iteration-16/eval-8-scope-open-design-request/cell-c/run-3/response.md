I haven't written an ADR, and I haven't touched `doc/adr`. Nothing is decided yet, so there is nothing to record.

The four open questions are which channels to support, whether to put a queue in front of the senders, how retries work, and which team owns the service. An ADR records one decision the team has already made, along with its real reasons. If I wrote one now, I would be inventing the decision and its rationale.

This is a design that still needs working out. The `design-doc` skill fits that: it walks through the problem, the trade-offs and the alternatives with you, and ends in a written design document. I can start that now if you like.

Once you settle each question, each one becomes its own ADR (one decision per record). The queue question and the retry policy would each get one, for example. The ownership question would get one too if you want it in the log. Come back with the outcome and I'll write them as `Accepted` records. If you already have a concrete proposal that is waiting on agreement, I can also write it as a `Proposed` ADR. For that I'd need the proposal itself, the reasons behind it, and the downsides the team is accepting.
