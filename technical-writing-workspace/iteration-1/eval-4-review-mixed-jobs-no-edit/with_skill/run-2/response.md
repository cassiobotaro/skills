I haven't edited `docs/webhooks.md`. The repository holds only that file, with no code, config or other docs, so I couldn't look up any actor or fact. Everything below is for you to decide.

## Questions for you

These are facts that only you or the code can answer. I haven't guessed any of them.

1. **Who is the reader?** The page never says. The intro and the "Setup" section suggest a developer integrating webhooks, so I assumed that reader.
2. **Who registers the endpoint, and what delivers the events?** In "the events will be delivered", which component delivers them, and to what? The text also doesn't say whether the endpoint has to respond with a particular status.
3. **Who generates the secret?** "After registration a secret is generated" doesn't say who generates it or where the reader sees it. The text also doesn't say what happens if the reader loses it, such as whether they can rotate it.
4. **Who signs each delivery?** "Each delivery is signed" doesn't name the signer. The signature section also leaves out the details a reader needs to verify:
   - the encoding of the `X-Signature` value (hex or base64, with or without a prefix)
   - the key used for the HMAC
   - a short code sample
5. **What does the retry section mean?** Each of these needs an answer from the code:
   - "it is retried": which component retries?
   - "some attempts": how many, and at what intervals?
   - "the endpoint is disabled": who disables it?
   - "an email is sent": who sends it, and to whom?
   - How does the reader re-enable the endpoint?
6. **Where does the history in the opening paragraph come from?** "Two designs were discussed" and "polling was considered wasteful" say nothing about who discussed or considered. If you want to keep the history, I'd need a source for the actors and the reasons.

## Proposed edits

**1. The page mixes jobs.** It holds history (an explanation), setup steps (a how-to), an event list (reference) and retry behavior (more explanation). The opening paragraph is the clearest case, because it delays the point.
- Cut the history, or move it to a separate "About webhooks" page.
- Make this page a how-to guide titled "How to receive webhooks". The event table can stay as a short list or link out to a reference page.

**2. The promise is too broad.** "In this guide you will learn everything about webhooks" promises more than the page delivers.
- Replace it with what the page covers and what the reader can do afterward. For example: "This guide shows you how to register a webhook endpoint, verify the signature on each delivery, and handle failed deliveries."

**3. Passives to rewrite.**
- "First, the endpoint must be registered. It is done in the dashboard…" becomes "Register your endpoint in the dashboard, under **Settings > Webhooks**." The actor is the reader, so use the imperative.
- "It should be stored safely, because it is shown only once." becomes "Store the secret right away: the dashboard shows it once." This assumes the dashboard shows it, which is question 3.
- "The signature… must be verified before the payload is trusted" becomes "Verify the signature before you trust the payload." The actor is the reader.
- "It is computed with HMAC-SHA256 over the raw body." Name who computes it, which is question 4. The sentence should also say where the reader gets the key.
- "If a delivery fails, it is retried… the endpoint is disabled and an email is sent." This needs the actors from question 5. It also needs a definition of "fails", such as which responses or timeouts count.
- "Webhooks were introduced… designs were discussed… was chosen… was considered" are all history passives. See question 6, or cut them.

**4. Passives that can stay.** "An invoice is paid" and "A customer is deleted" in the event table describe states, and no reader would ask "by whom?".

**5. Wording.** Cut "Simply" from "Simply paste the URL". It tells a reader who is stuck that the fault is theirs.

**6. Missing information.**
- The page doesn't show what a payload looks like. It doesn't list the headers other than `X-Signature`. It doesn't say what status code the endpoint should return.
- "When" in the event table is vague. Use "Sent when…" with the exact trigger, and match the event names to the code.
- Put the secret before the signature steps. A numbered sequence (register, store the secret, verify) would serve this reader better than the current mix of prose and table.

## Not done

I ran no commands, because nothing in the repository could be run. I haven't confirmed that the dashboard path, the event names or the header name match the product. Tell me which edits you want and send the answers to the questions above. I'll then apply the edits and mark any gaps that remain as `TODO`s.
