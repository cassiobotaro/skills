I left `docs/rotate-signing-key.md` unchanged, because it already meets the skill's rules and an edit would only add churn.

- **Reader and job:** it is a how-to for an operator with `kubectl` and the `secrets-admin` role, and it stays on that one job.
- **Actors:** every verb has one. The `auth` service reads the key, accepts both keys, and issues the tokens. The reader runs each step. The only passive, "is written in Go", describes a state.
- **Procedure:** each step has one action and an imperative verb. The commands carry no prompt character. Step 3 gives the output to check, `successfully rolled out`. The 15-minute wait comes with its reason.

I didn't run any command, since they all change the cluster. I also didn't check the document against the `auth` service code, because the repository contains only this file. These are the claims I couldn't confirm:

- The `signing` secret name and the `auth` namespace.
- The 15-minute token lifetime.
- That the service accepts tokens signed with either key while both are present.

One gap is for you to decide. The text doesn't say what to do if step 3 never reaches `successfully rolled out`, for example whether to delete `SIGNING_KEY_NEXT` or restart again. I left it out because the repository doesn't say.
