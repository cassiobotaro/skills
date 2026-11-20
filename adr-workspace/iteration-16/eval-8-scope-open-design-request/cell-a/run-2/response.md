I haven't written an ADR yet, and I haven't created or changed any files. An ADR records a decision that has already been made, along with the reasons for it. You've listed four open questions: which channels to support, whether to put a queue in front of the senders, how retries should work, and which team owns it. Right now there is nothing to record, and writing the ADR would mean inventing the choices and the rationale. That would make the log misleading for whoever reads it later.

Here is how I'd split the work:

- **While the architecture is open**, a design doc is the better tool. It is the place to compare channels, queue versus no queue, and retry strategies, and to settle ownership. I can help draft one if you want.
- **Once a question is settled**, each one becomes its own ADR in `doc/adr` (one ADR per decision). For example: "Put a queue in front of the notification senders", "Retry failed deliveries with exponential backoff", "Support email and push as the initial channels". If the team hasn't fully agreed yet, I can write the ADR with the status `Proposed`.

If some of these are already decided, tell me which ones and I'll write those ADRs now. These are the questions I'd need answered for each decision:

1. **What did you decide?** For example, the channel list, queue or no queue (and which technology), or the retry policy.
2. **Why, and why now?** What pressures led to this choice, and what is wrong with the current situation?
3. **What else did you consider, and what downside are you accepting?**
4. **Has everyone agreed?** That decides whether the status is `Accepted` or `Proposed`.

Team ownership is usually an organizational fact rather than an architecture decision. You can mention it in the Context of the relevant ADR, or I can record it as a separate ADR if it was a deliberate choice with trade-offs.

If you want everything recorded as `Proposed` for now, send me your current leaning on each question and the reasons behind it. I'll write them up faithfully and won't add anything you didn't say.
