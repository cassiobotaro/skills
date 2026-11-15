I haven't written the ADR yet. What you described is a list of open questions, not a decision, and an ADR records a decision the team has already made and why. If I filled in the channels, the queue, the retry policy and the owner myself, the record would contain made-up rationale, which is worse than having no record.

These are also four separate decisions (channels, queue, retries, ownership). The log keeps one decision per ADR, so each one will get its own record once it is settled.

Could you answer these so I can write the first record?

1. Which of the four has the team actually decided? For that one, what did you choose (for example, "we will put a queue in front of the senders, using X")?
2. Why now? What is wrong with the current state, or what pressure forces this decision (volume, reliability incidents, a new product requirement)?
3. What alternatives did you consider, and what downside did you accept by choosing this one?
4. Has everyone agreed? If not, I'll write it as `Proposed` instead of `Accepted`.

If the architecture is still being worked out, I can record the first decision that settles as `Proposed` and add the others as you decide them. A design doc may also be a better place to explore the open options before any ADR exists.

Once I have your answers, I'll create the ADR in `doc/adr/`. The directory doesn't exist yet, so I'll first create it with the standard `0001-record-architecture-decisions.md` seed record. Your decision will be `0002`.
