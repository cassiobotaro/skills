I read `docs/webhooks.md` and made no edits. The repo holds only this file, with no code, config or other docs, so I couldn't check any fact against a source. That's why the actor questions go to you.

**Main problem: the page does three jobs**

I assumed the reader is a developer integrating webhooks, who needs to register an endpoint and verify deliveries.

- The intro (lines 3-5) is Explanation: why the push model won over polling.
- Setup is a How-to.
- The events table is Reference.
- The signature and retry sections are partly Reference and partly How-to.

The page opens with history, and line 7 ("you will learn everything about webhooks") promises a tutorial it doesn't deliver. I'd move the history to a separate "About webhooks" page, or cut it. I'd rewrite the opener as: "Register an endpoint, verify each delivery's signature, and handle retries." Splitting the page is your call, since it changes the structure.

**Questions for you (only you or the code know these)**

1. Line 11, "the endpoint must be registered": is that the reader's job? If so, the sentence becomes "Register your endpoint in the dashboard…".
2. Line 22, "a secret is generated": does the dashboard generate it, or something else? It matters because the reader has to copy it.
3. Line 22, "it is shown only once": shown where? Is it in the dashboard right after registration, or in an email? If the reader loses it, can they regenerate it? That is the one recovery path the page leaves out.
4. Line 27, "each delivery is signed": which component signs it? "The signature is sent" has the same gap.
5. Line 28, "must be verified": the reader should verify it, so this should be an imperative. What is verified against what? The page should say that the reader computes HMAC-SHA256 over the raw body with the secret and compares the result to `X-Signature`. Also confirm the header's exact encoding (hex or base64) and whether it has a prefix.
6. Lines 33-34, retries: who retries, and how many times ("some attempts")? What are the intervals? Who disables the endpoint, and who gets the email? How does the reader re-enable it? An integrator can't plan around "some". Please give the real numbers.
7. Lines 18-20, events table: is this the full list? The reference has to be complete. "When" is also vague for `invoice.failed` ("A charge fails"). And there is no payload shape for any event.
8. Is anything else missing that you know of? I can't tell what you haven't written, such as the expected HTTP response from the endpoint, timeouts, and an example payload.

**Proposed edits (I'll apply them once you answer the questions above)**

- Line 3, "were introduced… were discussed… was chosen… was considered wasteful": four passives with no actor, and they carry history instead of the task. Move them to an explanation page, and say who chose and why if you keep them.
- Line 7, "learn everything about webhooks": replace it with the one-line statement of what the page covers, as above.
- Line 11, "First, the endpoint must be registered. It is done in…": rewrite as "Register your endpoint in the dashboard under **Settings > Webhooks**." Steps should be numbered.
- Line 12, "Simply paste the URL": drop "Simply". It tells a stuck reader the fault is theirs. Also say what to paste and what the reader should see afterward.
- Line 22, "It should be stored safely": make it an imperative, "Store the secret now: the dashboard shows it once." This depends on question 3, and the warning should come before the step it guards.
- Lines 27-29: split the verification into numbered steps, with the header name and a short sample that runs. This needs the facts from question 5.
- Lines 33-34: replace "retried", "some attempts" and "is disabled" with named actors and exact counts, once you answer question 6.
- The page uses "webhook", "endpoint", "delivery" and "secret". Use each consistently and use the terms your dashboard and code use. I can't check those here.

I haven't run anything.
