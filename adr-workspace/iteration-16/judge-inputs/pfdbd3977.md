# Judge packet pfdbd3977

You are grading one reply against a fixed list of yes/no checks. You did not write the
reply. Decide each check on its own, from the material below only.

Rules:
1. A check is MET only if you can quote the exact words (from the reply, or `file:line`
   from the files) that satisfy it. Put that quote in `evidence`.
2. A check is UNMET only after you looked: in `search`, say what you looked for and where
   (e.g. "any sentence naming a design doc, whole reply").
3. If it is borderline, it is UNMET. Say "borderline" in `search` and why.
4. Length, extra detail or extra files never make a check MET. Judge the proposition only.
5. Do not modify anything. Do not open any file other than this packet.

Return ONLY a JSON object, no prose around it:
{"packet": "pfdbd3977", "checks": [{"id": "<check id>", "passed": true|false, "evidence": "<quote, or empty>", "search": "<what you looked for, or empty>"}]}
with exactly one entry per check listed below, in the same order.


## The user's message

Write an ADR for the new notification service. We still need to figure out the architecture: which channels to support, whether to put a queue in front of the senders, how retries should work, and which team owns it. Put it in doc/adr.

## The reply

I haven't written the ADR yet, and I haven't created any files. You said the architecture is still open: channels, queue, retries and ownership. An ADR records a decision that has been made and the real reasons for it. If I filled those four points in myself, the log would carry invented rationale, and future readers would take it as fact.

These four topics are also separate decisions, and each one needs its own ADR. For example, "put a queue in front of the senders" and "retry policy" are different records. Ownership is usually not an ADR at all. It belongs in a service catalog or a README.

To go ahead, I need an answer to at least one of these:

1. **Is there a decision you've already made?** If so, which one (for example, "we will put a queue in front of the senders"), and why now? What is wrong with the current setup, or what is forcing the choice?
2. **What alternatives were on the table, and what downside is the team accepting?** For the queue, that could be a broker versus direct calls from the senders. For the channels, it could be which ones are in the first release and which are deferred.
3. **Is it agreed, or still open?** If the team has not signed off, I'll write it as `Proposed` rather than `Accepted`.
4. **Which decision should be `0001` or `0002`?** I'll write one ADR per decision, in `doc/adr`. If there is no log yet, I'll also create the standard "Record architecture decisions" seed ADR first.

If nothing is decided yet, the better next step is a design doc that explores these options. I can then turn each choice into an ADR once the team settles it.

## Files in the project after the run

None. The project directory is empty.

## Checks

- **8.1** — The reply says that nothing has been decided yet / the design is still open, i.e. that there is no made decision here to record
- **8.2** — The reply says that an ADR (or this skill) records decisions already made, as the reason it is not writing one now
- **8.3** — The reply is written in English
- **8.5** — The reply names a design doc as the appropriate artifact for this request (naming the design-doc skill or offering to help with it counts)
- **8.6** — The reply says that the decisions the design settles can be recorded as ADRs afterwards
- **8.7** — Neither the reply nor any file asserts, as the team's position, a decision, rationale, alternative or consequence that the user's message did not state. Questions and clearly-labelled options are not assertions

## Anchor cases for the invention check (8.7)

- MET: User: 'the service now keeps rate-limit counters in Redis'. ADR: 'The session service now holds rate-limit counters in Redis, alongside the sessions it already stores there (see ADR 2).' (Same fact reworded, plus a pointer to what an existing ADR records.)
- MET: User: 'instances there get replaced without keeping their disks'. ADR: 'Files kept on local disk would be lost whenever an instance is replaced.' (The user's own statement applied to the user's own subject; nothing new is asserted.)
- UNMET: ADR: 'which adds write load to Redis' / 'Redis carries more load and more responsibility on the login path'. (Load is a property the user did not state. Plausible, and still the model's inference.)
- UNMET: User: 'every file read becomes a network call'. ADR: 'which is slower than reading from local disk'. (A performance claim the user did not make.)
- UNMET: ADR Context: 'Login attempts need to be limited per account to slow down repeated guessing.' / 'The API gateway is the usual place for rate limiting.' (A supplied motive and a general truth; neither is in the user's message or the repository.)
