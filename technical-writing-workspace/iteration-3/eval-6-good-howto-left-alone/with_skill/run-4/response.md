I made no changes to `docs/rotate-signing-key.md`, because it already meets the skill's rules.

- **Reader and job:** it is a how-to guide for an operator who has `kubectl` and the `secrets-admin` role. The first paragraph says when to rotate and why a restart is needed.
- **Steps:** each step has one imperative action, with the command in a code block. The prerequisites come before step 1, and the 15-minute wait is stated with its reason.
- **Verbs:** each verb has an actor. The only passive left is "is written in Go", which describes a state and stays.

I checked the file against the page only. I ran none of the commands and did not check them against the cluster or the `auth` code.

If you want something changed anyway, tell me what the problem is. Two options are a verification step after the final restart, or a rollback note.
