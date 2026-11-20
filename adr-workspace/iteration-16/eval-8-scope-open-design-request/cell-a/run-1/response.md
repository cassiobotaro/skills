I haven't written an ADR yet, because you haven't made the decision. An ADR records a choice that has already been made and the reasons for it. You listed four open questions (channels, a queue in front of the senders, retry behavior, and ownership), so I would have to invent the Decision and the trade-offs. That would put made-up rationale into the log, and future readers would take it as the team's actual reasoning. I created no files in `doc/adr`.

Which of these fits your situation?

1. **Some of the four are already settled.** Tell me which ones and why (for example, "we will put a queue in front of the senders because X"). I'll write one ADR per settled decision. An ADR covers a single decision, so the queue, the retry policy, the channel set and ownership would each be a separate record. For each one I need:
   - what you chose,
   - why now and what is wrong with the current situation,
   - the alternatives you weighed,
   - the downside the team accepted.
2. **None are settled yet.** Then this is a design discussion, and a design doc is the better tool for it. A design doc lays out options and trade-offs so the team can decide. Once the team has agreed on the architecture, each decision can be recorded here as its own ADR.
3. **One decision is agreed but not signed off.** I can record it with status `Proposed` instead of `Accepted`. Tell me who still needs to agree.

Two smaller questions for when you do record something:
- Is `doc/adr` an existing log? If it is, I'll continue its numbering and match its format. If it isn't, I'll create it with the standard `0001` "record architecture decisions" seed, and your first ADR will be `0002`.
- Is "which team owns it" an architectural decision, or an organizational one that belongs somewhere else? If you want it recorded, I need the owner and the reasoning behind that choice.
