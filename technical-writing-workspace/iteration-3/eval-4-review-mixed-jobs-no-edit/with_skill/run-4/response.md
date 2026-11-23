I read `docs/webhooks.md` and haven't edited it. The page needs changes before you publish it. The main problems are that it mixes jobs and leaves out facts a reader needs.

**Reader I assumed:** a developer integrating webhooks who wants to register an endpoint and trust what arrives.

**Structural problem**

The page does three jobs at once. The history paragraph is explanation. Setup and signature verification are how-to. The events table and the retry details are reference. The opener, "you will learn everything about webhooks", promises more than the page gives and doesn't say what the page is for. I suggest this:
- Make the page a how-to guide: register an endpoint, verify signatures, handle retries.
- Move the 2023 history and the push-vs-polling reasoning to a separate concept page, or cut them.
- Link to a reference page for the events and the retry policy.
- Rewrite the first paragraph to say what the reader gets, for example "Register a webhook endpoint, receive events, and verify their signatures."

**Questions for you** (the page needs these facts, and I can't find them in the repository):
1. **Who does the passive-voice actions?** I can't tell who performs these:
   - "After registration a secret is generated." Does the dashboard generate it?
   - "It is retried." Does the platform retry?
   - "An email is sent." Who receives it: the account owner, or the address on the endpoint?
   - "Each delivery is signed." Does the platform sign it?
2. **What are the retry numbers?** "After some attempts" needs a count, the interval between attempts, and what counts as a failure (a non-2xx status? a timeout, and how long?).
3. **What does "disabled" mean for the endpoint, and how does the reader re-enable it?**
4. **How do you verify a signature?**
   - What is the header format?
   - Is the HMAC keyed with the secret from setup?
   - Is the signature hex or base64?
   - Is there a timestamp or a replay window?
   - A short code sample would help.
5. **What does the payload look like, and what must the endpoint return?** The page doesn't say, and a reader needs both to build a handler.
6. **Is the 2023 date, and the claim that polling "was considered wasteful", recorded anywhere?** I can't confirm either, and I don't want to polish a reason nobody wrote down.

**Proposed edits** (each applies once you decide on the structure)
- "First, the endpoint must be registered. It is done in the dashboard…" → "Register your endpoint in the dashboard, under **Settings > Webhooks**." The instruction was written as a description, and the reader is the actor.
- "Simply paste the URL and the events will be delivered." → "Paste the URL." Drop "simply". It tells a stuck reader the fault is theirs. Also say which events are delivered by default. Are they all three?
- "It should be stored safely, because it is shown only once." → "Copy the secret now and store it in your secrets manager. The dashboard shows it once." This is a warning, so it should come before the step it guards. Verify that the dashboard is the one showing it.
- "The signature is sent in the `X-Signature` header and must be verified…" → "Verify the `X-Signature` header before you trust the payload." Name who sends it once you answer question 1.
- "The following events exist:" → "Webhooks deliver these events:". The table's "When" column also uses passives ("An invoice is paid"). They describe states and are fine, but "A charge fails" for `invoice.failed` and "A customer is deleted" could be more precise. Say what triggers each event.
- "Verifying signatures" and "Retries" are noun headings. Task sections should start with a verb: "Verify signatures". The retry section is reference, so "Retry policy" is fine if you move it.
- Name the thing consistently: you use "endpoint", "URL", and "delivery". Choose one name for each, and match the name in the dashboard and the code.

**Not done:** I didn't check the product or dashboard. I also didn't run the `unslop` step, because I made no edits.

Tell me which structure you want and what you know about the questions above, and I'll apply the edits. I won't guess the answers.
