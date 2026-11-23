I haven't edited `docs/webhooks.md`. This review is in two groups, questions for you and proposed edits. There is no code in this repository, so I could only check the page against itself.

## Questions for you

These facts only you know, and I won't guess them.

1. **Who is the reader?** I assumed a developer at a customer's company, wiring up an endpoint. If so, the opening history is for someone else.
2. **Retries:** "After some attempts" needs the number of attempts and the schedule. Does the interval stay constant or back off?
3. **The disable email:** who receives it, and how does the reader re-enable the endpoint?
4. **Signature details:**
   - Is the `X-Signature` value hex or base64?
   - Does it carry a prefix?
   - Is there a timestamp header to guard against replays?
   - Which secret does the HMAC use? I assume the one generated at registration.
5. **Delivery success:** which response status counts as success, and how long does the platform wait for a response?
6. **Registration:** does the dashboard confirm or test the URL? "The events will be delivered" suggests that nothing more is needed.
7. **Payloads:** what does the body of each event look like? The page lists three events and no payload.
8. **The 2023 history:** is it worth keeping? I didn't verify it, and I'd move it out of this page.

## Proposed edits

**Mixed jobs.** The page mixes four jobs, so the reader can't act after one pass.
- The opening paragraph is Explanation (history and rationale).
- Setup is a How-to.
- The events table is Reference.
- Signature verification and retries are partly Reference and partly How-to.

I'd keep this page as the how-to ("How to receive webhooks"). I'd move the history to a separate "About webhooks" page and link it. The events table could become a reference page with payloads once you have them.

**Opening.**
- "In this guide you will learn everything about webhooks." says nothing and promises too much. Replace it with what the reader gets, for example: "This guide shows how to register an endpoint, verify the signature of each delivery, and handle retries."
- Also state what the page leaves out, such as payload formats, if they aren't covered.

**Actors.** Each of these sentences hides who acts.
- "First, the endpoint must be registered. It is done in the dashboard…" becomes "Register your endpoint in the dashboard under **Settings > Webhooks**."
- "the events will be delivered" becomes "the platform sends the events to that URL." I assumed "the platform", so confirm it.
- "a secret is generated" becomes "The dashboard generates a secret", assuming the dashboard does it.
- "It should be stored safely, because it is shown only once." becomes "Store the secret in your secrets manager. The dashboard shows it once."
- "Each delivery is signed." becomes "The platform signs each delivery…"
- "The signature is sent in the `X-Signature` header and must be verified before the payload is trusted." becomes "…Verify the signature before you trust the payload."
- "It is computed with HMAC-SHA256 over the raw body." becomes "The platform computes it as HMAC-SHA256 over the raw request body." Add the key and the encoding once you answer question 4.
- "it is retried" becomes "The platform retries the delivery", with the count and interval from question 2.
- "the endpoint is disabled and an email is sent" becomes "the platform disables the endpoint and emails <who>." This depends on question 3.
- In the events table, "An invoice is paid" is a state description and can stay. "A charge fails" could name its actor ("The payment provider declines a charge"), but only if that's true.

**Wording.**
- "Simply paste the URL" is flagged by the skill. Use "Paste the URL".
- Give each step an imperative verb. Setup could be a numbered list: open **Settings > Webhooks**, paste the URL, select events if you can, copy the secret.
- Add a warning before the secret step. The secret is shown once, so tell the reader to copy it first.
- Use one name per thing. The page says "endpoint", "URL", and "delivery", so pick consistent terms.

**Verification section.** Add a short, runnable sample in the reader's likely language, with the output it should print. Write it from the real implementation, not from convention. Show how to compare the signatures in constant time.

I assumed the reader and the platform actor. I ran no commands. I couldn't check any fact against code, since the repository holds only this file.
