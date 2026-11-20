I haven't written an ADR, and `doc/adr` is untouched. Everything you listed is still open: which channels to support, whether to put a queue in front of the senders, how retries should work, and which team owns the service. An ADR records a decision the team has already made, along with its real reasons. Writing one now would mean inventing the decision and its rationale, and that would mislead whoever reads the log later.

What you have is a design that still needs working out. That is design-doc work. The `design-doc` skill is built for it, with questions about the problem, the alternatives and the trade-offs, and then a written doc for the team to align on.

Once you settle each question, I can write an ADR for it. Each one gets its own record, for example:
- the channels to support
- a queue in front of the senders
- the retry policy
- ownership of the service

If you already have a concrete proposal for one of these and it's waiting on the team's agreement, I can write it now as a `Proposed` ADR. To do that I need three things for that decision:
1. What you propose, stated concretely.
2. Why it's needed now.
3. What downside you're accepting.
