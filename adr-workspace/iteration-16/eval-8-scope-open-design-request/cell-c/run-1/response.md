I haven't written an ADR, and `doc/adr` is untouched. Everything you listed is still undecided: which channels to support, whether to put a queue in front of the senders, how retries should work, and which team owns the service. An ADR records a decision the team has already made, with its real reasons. Writing one now would mean inventing the decision and its rationale.

What you have is a design that still needs working out. That is design doc territory, and the `design-doc` skill is installed. I'd start there, with those four open questions as the core of the doc, each with its alternatives and trade-offs.

Once the team settles a question, send it back to me and I'll write it as its own ADR, since each ADR holds one decision. For example, "we will put a queue in front of the senders" could be one, and "the platform team owns the service" another. If you already have a concrete proposal on one of them that's waiting for sign-off, I can write that one now with status `Proposed`.

Do you want to start the design doc?
