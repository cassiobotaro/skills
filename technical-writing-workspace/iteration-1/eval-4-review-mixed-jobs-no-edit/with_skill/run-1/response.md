I haven't edited `docs/webhooks.md`. The repo holds only this file, so I couldn't check any fact against code. Below are questions only you can answer, then proposed edits.

**Main problem: the page does four jobs at once.** I assumed the reader is a developer integrating webhooks into their own service. The page opens with history (explanation), then gives registration steps (how-to), then lists events (reference), then covers signatures and retries as a mix of description and instruction. I'd split it:
- A how-to guide: "How to register and verify a webhook endpoint".
- A reference page for the events, the header, and the retry behavior.
- A short explanation page for the 2023 history and the push-versus-polling decision.

Link the three pages. If you'd rather keep one page, lead with the how-to and move the history to the end or to its own page.

## Questions for you

The page never says who does these things, and the repo doesn't either:
1. "After some attempts, the endpoint is disabled." How many attempts, and how far apart? What counts as a failed delivery: a non-2xx status, a timeout, both? "Some attempts" can't be acted on.
2. "An email is sent." Who sends it, and to whom: the account owner, or the address on the webhook?
3. "The events will be delivered." Who delivers them: the platform, to the registered URL? Does it deliver every event or only the ones you choose? The table lists three events, so is the list complete?
4. "A secret is generated." By what, and where is it shown: in the dashboard right after you register? How does the reader get a new one if they lose it?
5. Signature check: does the HMAC key come from that secret? Is the `X-Signature` value hex or base64? Is there a timestamp the reader should check against replays? You can't write the verification steps without these answers.
6. Is the 2023 history ("several customers asked", "polling was considered wasteful") recorded in a decision log? If not, I'd cut or mark it, since nothing here confirms the reasons.

## Proposed edits

**Opening.** "In this guide you will learn everything about webhooks." This promises everything and tells the reader nothing. Replace it with the point, for example: "A webhook sends an HTTP request to your URL when an event happens in your account. This page shows how to register an endpoint and verify its signatures." Put that first and move the history below it or out.

**Passives to rewrite once you answer the questions above:**
- "the endpoint must be registered. It is done in the dashboard" becomes "Register the endpoint in the dashboard, under **Settings > Webhooks**."
- "the events will be delivered" needs an actor: "`<component>` sends the events to your URL".
- "a secret is generated. It should be stored safely, because it is shown only once." becomes "`<component>` shows a secret once, after you register. Copy it now and store it in your secret manager." Also move that warning before the step it guards.
- "Each delivery is signed. The signature is sent in the `X-Signature` header" becomes "`<component>` signs each delivery and puts the signature in the `X-Signature` header."
- "must be verified before the payload is trusted" is an instruction written as a description. Write "Verify the signature before you trust the payload", and give numbered steps.
- "It is computed with HMAC-SHA256 over the raw body." Say who computes it, and tell the reader to compute it themselves: "Compute HMAC-SHA256 of the raw request body with your secret and compare it to `X-Signature`." Add a short sample that runs, once you confirm the encoding.
- "it is retried", "the endpoint is disabled", "an email is sent" all hide the actor. See question 1 and question 2.

**Wording:**
- Delete "Simply" in "Simply paste the URL". The word tells a stuck reader the fault is theirs.
- The page uses "endpoint" and "URL" for the same thing, and "delivery" and "event" loosely. Pick the one name the code uses for each.
- "First, the endpoint must be registered" is a numbered step in disguise. Number the steps and start each with a verb.
- Retries: replace "some attempts" with the number and the intervals.

**Headings.** "Setup" and "Retries" are fine as reference-style headings. In a how-to guide, the task headings should start with a verb: "Register an endpoint", "Verify a signature".

**Passives I'd leave:** "An invoice is paid" and "A customer is deleted" in the event table. They name states that a reader wouldn't ask "by whom?" about. "`invoice.failed`: A charge fails" is already active.

## What I need from you

Answers to questions 1–5 so I can fill in the actors and numbers. I haven't run or confirmed anything, because the repo has no code or other docs. If you'd like the draft before you have the answers, I can write it with a `TODO` at each gap. Tell me which structure you want, three pages or one, and I'll apply the edits.
