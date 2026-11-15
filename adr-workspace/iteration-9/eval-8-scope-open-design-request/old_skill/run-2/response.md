I haven't written an ADR yet, and I haven't created or changed anything in `doc/adr`. An ADR records a decision that has already been made, and the four things you listed (channels, a queue, retries, ownership) are still open. If I wrote one now, I would be inventing the decision and the reasons for it. That would leave a false record for whoever reads the log later.

The four items are also separate decisions. Each one gets its own ADR, so this will end up as several records, not one. Tell me which of them you have settled, and I'll write those.

For each one you have decided, I need:

1. **What did you decide?** For example: which channels (email, SMS, push, ...), whether a queue sits in front of the senders and which technology, what the retry policy is (attempts, backoff, dead-letter handling), and which team owns the service.
2. **Why now, and what was wrong with the status quo?** What pushed this decision, and which alternatives did you consider and reject?
3. **What downside did you accept?** Every choice has a cost, such as operational complexity from a queue or delayed delivery from retries. I need the real trade-off so Consequences isn't one-sided.
4. **Is it agreed (Accepted) or still waiting on sign-off (Proposed)?**

If you want to record that the architecture is still open, I can write a single ADR with status Proposed that names the open questions. That ADR would state what is undecided and why, and I wouldn't pick answers for you. Say so if you want it.

Once you answer, I'll write the ADRs in `doc/adr`. The folder doesn't exist yet, so I'll start the log with the standard "Record architecture decisions" ADR as 0001, and your decisions will follow from 0002.
