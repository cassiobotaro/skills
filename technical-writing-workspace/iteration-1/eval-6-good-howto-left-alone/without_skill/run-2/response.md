I didn't change `docs/rotate-signing-key.md`. It's already a good how-to, so editing it would add churn without making it better.

- It states when to rotate and what the restart implies.
- It lists prerequisites.
- Its steps are numbered, and each one is a single action with a runnable command.
- It tells you how to confirm the rollout finished.
- It explains why you wait 15 minutes between steps 3 and 4.

Two things you may want to check. I haven't changed either one, because I can't verify them from here.

- **Step 2 and existing keys:** the `kubectl create ... --dry-run | kubectl apply` command builds a secret that contains only `SIGNING_KEY_NEXT`. Whether `apply` keeps the existing `SIGNING_KEY` depends on how the secret was first created. If you'd rather not depend on that, `kubectl patch` or `kubectl set data` on the `signing` secret would add the one key without touching the rest.
- **Step 4:** it says to copy the value of `SIGNING_KEY_NEXT` to `SIGNING_KEY` but gives no command, unlike the other steps. Adding one would make it consistent.

I can make either change if you want.
