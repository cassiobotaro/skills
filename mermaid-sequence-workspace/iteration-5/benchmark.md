# iteration-5 — targeted re-run of eval 1 against 1.1.3

**Scope.** Not a full set. 1.1.3 made three changes that iteration-4 could not have
measured: step 5.3 no longer offers mermaid.live when the fallback was reached *because*
of the sensitivity gate; the canonical example in `SKILL.md` no longer carries
`Content-Type: application/json` (it was teaching by imitation the pattern 1.1.2 banned);
and the parse assertions now name both verification routes. This run re-executes eval 1,
the case that exercises all three.

**Method.** One `with_skill` run against the working-tree skill, hosted Mermaid MCP
connected, `mermaid-cli` absent, installs forbidden.

## Result — both new behaviors hold

**No protocol boilerplate.** `grep -rniE 'content-type|accept:|charset|user-agent'` over
the outputs returns nothing at all. In iteration-3 the same grep found the header twice in
the diagram; in iteration-4 it found only the run's explanation of why it was omitted.
Now the question no longer comes up — which is what removing it from the canonical example
was meant to achieve. Correlation, not proof, on a single run: the example was one of two
changes 1.1.2/1.1.3 made to this behavior.

**mermaid.live is declined, not offered.** The gate fired again (broker topology, event
name, Postgres, partner bearer header), `mmdc` was absent, and step 5.3 produced:

> "I'd skip pasting it into mermaid.live. The best preview is the one you already own: put
> the file (or the fenced block) on a GitLab wiki page or a branch and let GitLab's native
> renderer draw it. If you'd rather have a rendered preview link, say so and I'll run it
> through the hosted validator."

That is the whole rule: private preview first, hosted validator offered as the user's
explicit choice. The only occurrences of "mermaid.live" in the outputs are this refusal
and the transcript note explaining it.

The remaining assertions of eval 1 were spot-checked and hold (fenced block, the given
technical details, the rate-limit branch, always-202, `actor` plus async `-)`). They were
**not** re-graded by an independent grader. Per the amended assertion wording, the parse
check on this run was a **manual syntax review**, not a machine parse — `mermaid-cli` is
not installed here and the diagram was correctly withheld from the remote renderer, so no
machine parse was possible without defeating the behavior under test.

Tokens 34,514; wall clock 258s.
