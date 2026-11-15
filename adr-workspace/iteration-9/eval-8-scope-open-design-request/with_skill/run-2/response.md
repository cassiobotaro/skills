I didn't write an ADR, and I didn't change anything in `doc/adr`. An ADR records a decision the team has already made, along with its real reasons. What you describe is a design that is still open. The channels, the queue in front of the senders, the retry behavior and the owning team are all undecided. An ADR written now would invent decisions and rationale nobody has agreed on.

This is work for a design doc, where you compare the options and settle the open questions. The `design-doc` skill can help, if it is installed. It walks through the problem, the alternatives and the trade-offs. Once a question is settled, each answer can become its own ADR.

Here is how that could go:

- **Channels:** "We will support email and push first" would be one ADR.
- **Queue:** "We will put a message queue in front of the senders" would be another.
- **Retries:** the retry policy would be a third.
- **Ownership:** the owning team is usually a note in the design doc, not an ADR.

I'll write an ADR as soon as any of these is decided. Give me the decision, why you made it and what downside you accepted. If a concrete proposal is waiting for the team's agreement, I can write it as a `Proposed` ADR.

To start a design doc, a few questions would help:
1. What problem is the notification service solving, and why now?
2. Which channels are candidates, and which are firm requirements?
3. Which alternatives for the queue and for retries have you looked at?
4. Which teams are affected, and who has to agree?
