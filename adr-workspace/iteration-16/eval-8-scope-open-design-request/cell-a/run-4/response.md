I haven't written an ADR yet, and I haven't created any files in `doc/adr`.

An ADR records a decision that has already been made, along with the reasons for it. You listed four things that are still open: which channels to support, whether to put a queue in front of the senders, how retries should work, and which team owns the service. If I wrote the record now, I would be inventing the decision and its rationale. That would give future readers a made-up "why", which is worse than having no record.

An ADR also covers one decision. Four open questions would end up as several separate ADRs, one per decision, once each is settled.

Here are two ways to go from here:

1. **Work out the design first.** The questions you list are the contents of a design doc, where alternatives and trade-offs are weighed before anything is chosen. Once the team settles a question, each answer becomes its own ADR.
2. **Record the decisions you have already made.** If any of the four is decided, tell me and I'll write that one now. Please give me:
   - What was decided, concretely. For example: "We will put a queue between the API and the channel senders, using X."
   - Why, and why now. What pressure or problem led to the choice?
   - Which alternatives you considered, and what downside the team accepted.
   - Whether everyone has agreed (`Accepted`) or it is still waiting on sign-off (`Proposed`).

If you want a placeholder in the log while the architecture is undecided, tell me. I could write a `Proposed` ADR that only states the open question, with no outcome. I'd only do that if you ask for it.

Once I have the answers, I'll add the ADR to `doc/adr` and number it automatically.
