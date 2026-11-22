I read `docs/webhooks.md` and haven't edited it. It isn't ready to publish yet. The main problem is that a reader can't act on the verification and retry sections.

**Blocking issues**

1. **Signature verification is too vague to implement.**
   - It doesn't say how the signature is encoded (hex or base64), or whether there's a prefix such as `sha256=`.
   - It doesn't say which key signs the payload, though presumably it's the secret from setup.
   - It doesn't say how to compare signatures. Recommend a constant-time comparison.
   - There's no code example. A short snippet in one or two languages would help a lot.
   - There's no mention of replay protection. If deliveries carry a timestamp, say how to check it. If they don't, say so.
2. **Retries are undefined.**
   - "After some attempts" and "it is retried" give no numbers. State the number of attempts, the backoff schedule and the timeout per delivery.
   - State which HTTP status codes count as success. Say whether a 3xx redirect counts.
   - Say which email address gets the disable notice. Say how to re-enable a disabled endpoint.
3. **Delivery semantics are missing.**
   - Say whether delivery is at-least-once, and whether events can arrive out of order.
   - If events can arrive twice, say how to deduplicate them, for example with an event ID.
4. **The payload isn't documented.** No example JSON body and no list of headers other than `X-Signature`. Show one example payload per event type, or at least the common envelope.

**Should fix**

5. **The intro is history, not guidance.** The opening paragraph (2023, two designs, why push won) doesn't help someone setting up an endpoint. Cut it, or move it to a changelog or design note. Start with what webhooks do and who they're for.
6. **"In this guide you will learn everything about webhooks" overpromises.** The guide doesn't cover everything. Replace it with a concrete list of what's covered.
7. **The setup section is incomplete.**
   - "Simply paste the URL and the events will be delivered" skips details. Say whether the URL must be HTTPS, whether you can pick which events to subscribe to, and whether there's a test or ping button.
   - Add a note on what happens if the secret is lost. Presumably you can rotate it. Say so and say how.
8. **The events table is thin.**
   - "When" repeats the event name. Say what triggers each event precisely. For example, does `invoice.failed` fire on every failed charge attempt or only on the final one?
   - Add the key payload fields for each event.
   - Check that the list is complete. `customer.deleted` is the only customer event, which looks odd.
9. **Passive voice hides the actor** in several places: "the endpoint must be registered", "it is retried", "an email is sent". Name who does what ("You register…", "We retry…", "We email the account owner…").

**Minor**

- Add a short troubleshooting section covering common failures: signature mismatch because the body was parsed before verifying, timeouts, and disabled endpoints.
- State the expected response, for example return a 2xx quickly and process asynchronously.
- Link to the dashboard page and to any API reference for events.

I couldn't check any of these claims against the product, so please confirm the specifics (header name, algorithm, event list, retry behavior) with the code or the team before you fill in the gaps.

I can draft a revised version if you want. I'd need the retry policy, the signature format and the payload shapes from you first.
