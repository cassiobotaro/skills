I made no changes to `docs/rotate-signing-key.md`, because it's already a good how-to.

- **Structure:** It follows the usual order of purpose, prerequisites, then numbered steps.
- **Steps:** Each step is one action with a copy-pasteable command.
- **Verification:** The restart step says what output means success.
- **Timing:** The 15-minute wait between steps 3 and 4 is explained by the token lifetime.
- **Consequences:** The doc says what breaks after step 4.
- **Style:** The writing is direct and uses the active voice.

One optional addition: a note on how to roll back if the rollout in step 3 fails. I didn't add it, because that would mean inventing operational behavior I can't check from the repository.
