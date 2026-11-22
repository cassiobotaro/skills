I wrote `README.md` at the repo root. I ran nothing: it's drafted from the Makefile, `pyproject.toml`, the source, the script and `docs/pipeline.md`.

It covers what the service is, the prerequisites, the four environment variables, a local run with the `make` targets, a sample `curl` request, requeuing failed exports with `scripts/requeue_dead.py`, and `make test`. Every command and variable name comes from the repo.

**Reader I assumed:** a developer who wants to run the service locally or handle failed exports.

**Holes, each marked as a `TODO` in the file:**
- **Queues:** nothing in the code declares `exports` and `exports.dead`. Who creates them, and with what settings?
- **AWS setup:** which AWS region does the code use, and what must be set up in SES for the `MAIL_FROM` sender?
- **Tests:** `make test` runs pytest, but the repo has no tests.
- **License and help:** there is no `LICENSE` file and no contact or channel to name.

**Left out on purpose:** `docs/pipeline.md` says backups of the bucket rotate weekly. No code or config shows that, so I didn't repeat it.

**Check before you rely on it:** the README leaves out how to generate the `EXPORT_KEY` value. The worker uses a Fernet key, so `Fernet.generate_key()` from `cryptography` makes one. I didn't add that command because I haven't run it.
