I didn't edit `docs/rotate-signing-key.md`. It already meets the skill's rules, and a rewrite would only change the author's wording.

- **What it already does well:** The first paragraph says what the page is for and when to use it. Prerequisites come before the steps. Each step is one imperative action with a bare command block, and step 3 shows the expected output. The only passive, "is written in Go", describes a state, which the skill allows.
- **Reader I assumed:** An operator with cluster access who is rotating the key.

Two questions for you, because I can't answer them from the repository:
1. **Step 2:** Does `kubectl apply` of that generated manifest keep the existing `SIGNING_KEY` entry in the `signing` secret? I didn't run it. If it replaces the secret's data, the `auth` service loses its current key at the restart in step 3. If it merges, the step is fine.
2. **Wait time:** Is the 15-minute token lifetime in the final paragraph configured somewhere I should cite? I couldn't check it.

If you want one optional change, I'd move the "wait 15 minutes between step 3 and step 4" line into step 4, ahead of the action it guards. I held back because it changes the structure.
