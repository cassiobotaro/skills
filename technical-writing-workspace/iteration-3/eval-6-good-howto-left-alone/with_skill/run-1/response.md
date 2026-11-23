I made no edits to `docs/rotate-signing-key.md`. It already does what the skill asks of a how-to guide:

- **Structure:** it has one reader (an operator with `secrets-admin`) and one job. Prerequisites come before the steps, and each step is a single action with its command.
- **Actors:** every verb has one. The only passive, "The `auth` service is written in Go", describes a state, which is one of the two cases the skill allows.
- **Checks:** step 3 shows what success prints, and the 15-minute wait is tied to the token lifetime.

Rewriting it would only change the author's wording.

One question for the author, which I couldn't settle without running the command against a cluster: in step 2, does `kubectl apply` keep the existing `SIGNING_KEY` in the `signing` secret? The command builds the secret from `SIGNING_KEY_NEXT` alone. If the apply replaces the secret instead of merging into it, `SIGNING_KEY` would disappear, and the restart in step 3 would fail. If it merges, nothing needs to change. A one-line note either way would help.

I assumed the reader is an operator who already knows `kubectl` and this cluster. I ran no commands.
