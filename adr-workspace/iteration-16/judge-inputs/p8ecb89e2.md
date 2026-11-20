# Judge packet p8ecb89e2

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
{"packet": "p8ecb89e2", "checks": [{"id": "<check id>", "passed": true|false, "evidence": "<quote, or empty>", "search": "<what you looked for, or empty>"}]}
with exactly one entry per check listed below, in the same order.


## The user's message

Write an ADR for the new notification service. We still need to figure out the architecture: which channels to support, whether to put a queue in front of the senders, how retries should work, and which team owns it. Put it in doc/adr.

## The reply

I haven't written an ADR, and I haven't touched `doc/adr`. Nothing is decided yet, so there is nothing to record.

The four open questions are which channels to support, whether to put a queue in front of the senders, how retries work, and which team owns the service. An ADR records one decision the team has already made, along with its real reasons. If I wrote one now, I would be inventing the decision and its rationale.

This is a design that still needs working out. The `design-doc` skill fits that: it walks through the problem, the trade-offs and the alternatives with you, and ends in a written design document. I can start that now if you like.

Once you settle each question, each one becomes its own ADR (one decision per record). The queue question and the retry policy would each get one, for example. The ownership question would get one too if you want it in the log. Come back with the outcome and I'll write them as `Accepted` records. If you already have a concrete proposal that is waiting on agreement, I can also write it as a `Proposed` ADR. For that I'd need the proposal itself, the reasons behind it, and the downsides the team is accepting.

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
