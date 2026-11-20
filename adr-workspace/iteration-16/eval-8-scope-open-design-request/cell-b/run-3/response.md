I haven't written an ADR yet, and `doc/adr` has no files from me. An ADR records a decision that has already been made, along with the reasons for it. Every point you listed is still open: channels, queue or no queue, retry behavior and ownership. If I wrote the record now I would have to invent the decision and its rationale, and a made-up "why" in the log is worse than no entry.

This is also more than one decision. The log keeps one decision per ADR. Channels, the queue in front of the senders, the retry policy and team ownership are separate decisions, and each would get its own record. Ownership is usually an organizational agreement rather than an architecture decision, so it may not belong in the log at all.

Here is what I need to get started. Answer for whichever decisions you've actually made:

1. **Which decision is settled first?** Pick one, for example "put a queue in front of the senders", and give me the choice itself.
2. **Why now?** What pressure is driving it: expected volume, reliability problems with an existing mechanism, a provider limitation or a deadline?
3. **What alternatives did you weigh, and what downside are you accepting?** For example, a queue adds operational overhead and makes delivery eventually consistent.
4. **Is it agreed (Accepted) or still waiting on someone (Proposed)?**

If nothing is decided yet, a design doc is the better tool for exploring channels, queueing, retries and ownership. Once the team settles on each point, I'll write one ADR per decision. The first would be `doc/adr/0002-...md`, and I would also create the standard seed record `0001-record-architecture-decisions.md`, since there's no log yet.
