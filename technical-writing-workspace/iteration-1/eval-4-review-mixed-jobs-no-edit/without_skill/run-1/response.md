**Review of `docs/webhooks.md`: not ready to publish yet.** The main problem is that the guide leaves out the details a reader needs to build an integration. I haven't changed the file.

**Content gaps (these matter most)**
1. **Retries** is too vague to act on. "Some attempts" and "it is retried" don't tell a reader how many attempts, how long the gaps are, or what counts as a failure. Please state:
   - the number of attempts and the backoff schedule;
   - the timeout, and whether any non-2xx status or only some statuses count as a failure;
   - which email goes to whom when an endpoint is disabled, and how to re-enable it.
2. **Signature verification** has no usable detail:
   - There's no code example.
   - It doesn't say how the hex or base64 digest is encoded, whether the secret is used directly as the key, or whether the header has a prefix.
   - It doesn't mention comparing signatures in constant time.
   - There's no replay protection. If deliveries carry a timestamp, document the tolerance window. If they don't, say so.
3. **Payloads:** the guide has no example payload, no envelope schema, and no description of the event object. The reader can't write a handler without these.
4. **Delivery semantics:**
   - It doesn't say whether delivery is at-least-once or whether events can arrive out of order.
   - It doesn't say whether to dedupe on an event ID, or what that ID field is.
   - It doesn't say how fast the endpoint must respond (the usual advice is to return 2xx quickly and process asynchronously).
5. **Setup details:**
   - HTTPS requirements are missing.
   - It doesn't say whether you can register several endpoints or pick which events each one gets. "Simply paste the URL and the events will be delivered" suggests all events go to one endpoint.
   - There's no way to test, such as a "send test event" button, and no way to see delivery logs.
   - The secret is shown only once, but the guide doesn't say how to rotate it if it's lost.
6. **Event table:** the "When" descriptions just repeat the event names. `invoice.failed` ("A charge fails") is ambiguous about whether it fires on every failed attempt or only the final one. Please also confirm the list is complete. Three events seems small, and there's no `customer.created`.

**Structure and tone**
- **The history paragraph comes first.** "Introduced in 2023… two designs were discussed" is internal background, and readers don't need it before setup. Cut it, or move it to a changelog or an "About" note.
- **"In this guide you will learn everything about webhooks"** overpromises, given the gaps above. Replace it with a concrete one-liner, such as "This guide shows how to register an endpoint, verify signatures, and handle retries."
- **Passive voice hides who does what.** For example, "the endpoint must be registered" and "It is done in the dashboard" don't say who acts. "Register your endpoint in **Settings > Webhooks**" is shorter and clearer.
- **"Simply"** in "Simply paste the URL" is filler, and it's condescending if the reader hits a problem.
- **Order:** the secret is generated after registration, but signature verification comes later. Consider a "Quickstart" that goes register, store secret, verify, respond 2xx, so that new readers get a working path first.

**Smaller points**
- The `X-Signature` header name and the algorithm are shown in code formatting, which is good. Do the same for the dashboard path if you like.
- The email on disable should say who receives it, such as the account owner or an alert address.
- Check that "Settings > Webhooks" matches the current dashboard labels.

**What works well**
- The guide is short and the sections are in a sensible order.
- Telling readers the secret is shown only once is important and clear.
- Verifying against the raw body is the right detail to include.

I can draft the missing sections, such as retries, a verification example and a sample payload, if you give me the real values. I don't want to invent numbers like retry counts or timeouts.
