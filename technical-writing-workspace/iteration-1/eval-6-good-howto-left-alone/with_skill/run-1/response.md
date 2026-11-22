I didn't edit `docs/rotate-signing-key.md`, because it already meets the skill's rules.

- **Reader and job:** it is a how-to for an operator with `kubectl` access, and it stays on that one job.
- **Opening:** the first paragraph says when to rotate and why a restart is needed.
- **Prerequisites:** they come before the first step.
- **Steps:** each is numbered, starts with an imperative verb, and has its command in a block. Step 3 shows the output to wait for.
- **Verbs and actors:** every verb has an actor ("the `auth` service accepts…", "Tokens that the old key signed stop working…"). The only passive is "is written in Go", which describes a state and is one of the two that stay.

Rewording it would only change the author's voice.

I did not run any command. They all change cluster state, and I can't check them from this repository.

**Open questions for you:**
- Step 4 says to wait 15 minutes between step 3 and step 4, but the sentence comes after the steps. Do you want it moved into step 4 as a warning before the action? I left it because it changes the structure.
- Step 4 doesn't give a command for "copy the value … and delete `SIGNING_KEY_NEXT`". Do you want the exact `kubectl` commands added? I can't confirm them from this repository.
