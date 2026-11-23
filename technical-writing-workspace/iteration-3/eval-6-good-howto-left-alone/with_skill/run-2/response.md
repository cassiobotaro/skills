I left `docs/rotate-signing-key.md` unchanged, because it already does what the skill asks of a how-to guide.

- **Reader and job:** It's written for an operator with `kubectl` access, and it covers one task with prerequisites before the steps.
- **Steps:** Each step has one action, a verb-first imperative, and the command that does it. Step 3 shows the check that proves it worked.
- **Actors:** Every verb has a named actor, such as "The `auth` service accepts…" and "Tokens that the old key signed stop working…". The one passive, "is written in Go", describes a state, so it stays.

Changing it would only swap the author's wording for mine.

**Not done:**
- I didn't run any of the commands, and I didn't check them against a real cluster.
- I didn't check the 15-minute token lifetime or the `SIGNING_KEY_NEXT` behavior against the `auth` code. This repository doesn't contain that code.

**Question for you:** I assumed the reader is an on-call or platform engineer. If the page is also meant for people without prior `kubectl` or `secrets-admin` experience, say so. It would then need a link on how to get that access.
