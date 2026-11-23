I read `docs/webhooks.md` and made no edits. The only source is the file itself, because the repo has no code or other docs to check. Below are questions for you, then proposed edits.

## Questions for you

These are facts only you know, so I haven't guessed at them.

1. **Who does what in "After registration a secret is generated"?** Does the dashboard generate it? Does the reader copy it from a screen? If so, which screen?
2. **What sends the retry email, and to whom?** The sentence is "an email is sent". Who receives it: the account owner, or the address on the webhook?
3. **What are the retry numbers?** "After some attempts" needs the real count. It also needs the schedule between attempts and what counts as a failed delivery (a timeout? any non-2xx status?).
4. **How does the reader re-enable a disabled endpoint?** The page doesn't say.
5. **How does the reader verify a signature?** Is `X-Signature` the bare hex digest, or does it have a prefix? Which secret is the HMAC key? A reader can't implement the check from "HMAC-SHA256 over the raw body".
6. **Is this page for people integrating webhooks for the first time, or for people who already integrate and need facts?** I assumed the first group.

## The main problem: the page does three jobs

It mixes explanation, a how-to and a reference, and no reader is served well.

- **Explanation:** the history paragraph at the top, the 2023 customer requests and the two designs. It tells the reader nothing they need to act. Move it to a separate concept page or cut it, and link to it if you keep it.
- **How-to:** Setup and the signature section are steps for a reader with a goal. Keep them, but start the headings with a verb ("Register an endpoint", "Verify a signature"). Give the steps in numbered order.
- **Reference:** the event table and the retry behavior are lookup facts. They belong in a reference section with the same fields for every entry. The event table lacks the payload shape for each event.

The first paragraph should say what the page is for. Replace "In this guide you will learn everything about webhooks" with something like "This guide shows how to register a webhook endpoint, verify its signatures, and handle failed deliveries." "Everything" promises more than the page holds.

## Proposed edits, each with its reason

| Sentence | Edit | Reason |
|---|---|---|
| "First, the endpoint must be registered. It is done in the dashboard…" | "In the dashboard, open **Settings > Webhooks** and register your endpoint URL." | Names the actor (you) and puts the location first. |
| "Simply paste the URL and the events will be delivered." | Drop "Simply". Say who delivers: "Paste the URL. Our servers then send the events to it." (Check the actual component name.) | "Simply" blames a reader who gets stuck, and "will be delivered" has no actor. |
| "The following events exist" | "The dashboard offers these events:" | Active, and "exist" is empty. |
| "An invoice is paid", "A charge fails", "A customer is deleted" | State what triggers each event and who acts. For example, "A customer pays an invoice". | These are passives or vague. For `customer.deleted`, say who deletes the customer. |
| "A secret is generated. It should be stored safely, because it is shown only once." | "The dashboard shows the signing secret once. Copy it and store it in your secrets manager." (Edit after Q1.) | It has two missing actors and an instruction written as description. It also puts the warning after the fact. |
| "The signature is sent… and must be verified before the payload is trusted. It is computed with…" | "Each delivery carries a signature in the `X-Signature` header. Before you trust the payload, compute HMAC-SHA256 over the raw request body with your secret and compare the result to the header." | Four passives, and "must be verified" is an instruction. The edit also uses "you", as the other sections should. |
| "If a delivery fails, it is retried. After some attempts, the endpoint is disabled and an email is sent." | "If a delivery fails, `<component>` retries it `<N>` times. After the last attempt, `<component>` disables the endpoint and emails `<recipient>`." (Fill in after Q2 and Q3.) | Four passives. "Some attempts" can't be acted on. |
| "Webhooks were introduced in 2023… polling was considered wasteful" | Move or cut. If it stays, name who discussed the designs and who chose the push model. | "Were discussed", "was chosen" and "was considered" all have no actor. |

I haven't run any commands. Nobody has tested the setup steps against the dashboard, so please walk through them once before you publish.

Tell me which edits you want and I'll apply them to the file. I'll leave a `TODO` where Q1–Q5 stay unanswered.
