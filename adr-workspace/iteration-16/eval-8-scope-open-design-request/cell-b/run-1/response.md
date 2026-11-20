I haven't written the ADR yet, and I haven't created any files. You said the architecture is still open: channels, queue, retries and ownership. An ADR records a decision that has been made and the real reasons for it. If I filled those four points in myself, the log would carry invented rationale, and future readers would take it as fact.

These four topics are also separate decisions, and each one needs its own ADR. For example, "put a queue in front of the senders" and "retry policy" are different records. Ownership is usually not an ADR at all. It belongs in a service catalog or a README.

To go ahead, I need an answer to at least one of these:

1. **Is there a decision you've already made?** If so, which one (for example, "we will put a queue in front of the senders"), and why now? What is wrong with the current setup, or what is forcing the choice?
2. **What alternatives were on the table, and what downside is the team accepting?** For the queue, that could be a broker versus direct calls from the senders. For the channels, it could be which ones are in the first release and which are deferred.
3. **Is it agreed, or still open?** If the team has not signed off, I'll write it as `Proposed` rather than `Accepted`.
4. **Which decision should be `0001` or `0002`?** I'll write one ADR per decision, in `doc/adr`. If there is no log yet, I'll also create the standard "Record architecture decisions" seed ADR first.

If nothing is decided yet, the better next step is a design doc that explores these options. I can then turn each choice into an ADR once the team settles it.
