# iteration-9 — scope section A/B (mermaid-sequence 1.3.0 vs 1.2.1)

**Change under test.** A "Check the scope first" section was added to `SKILL.md`, before
the contract, mirroring the one in `structurizr`: a sequence diagram has participants
exchanging messages in time order; decision logic is a `flowchart`, a lifecycle is a
`stateDiagram-v2`, static structure is a C4 view for the `structurizr` skill. The model is
told to say in a sentence that this skill covers sequence diagrams, deliver the other
Mermaid types outside the house conventions but still under rules 1, 2 and 5 (record,
don't invent; flag undefined branches; validate), and hand C4 on. Body 12 178 → 13 502
bytes. The shipped 1.2.1 is snapshotted in `../skill-snapshot-1.2.1/`.

**Method.** Eval 6 (`scope-flowchart-request`), two runs per arm, four agents in one batch.
`with_skill` = working tree (1.3.0); `old_skill` = the snapshot. Graded with a programmatic
pre-pass (block extraction, HTML-unescape, re-render with `minlag/mermaid-cli`, gate and
keyword checks) and a manual read for the scope sentence and the invention rule.

**Reading `benchmark.md`.** Configurations are ordered alphabetically, so `old_skill` is the
first column and `with_skill` the second; the delta is old minus new.

| Arm | Runs | Assertions | Tokens | What happened |
|---|---|---|---|---|
| 1.3.0 (with_skill) | 2 | 12/12 | 48 805 · 48 844 | Both open with the scope sentence before the block ("esta skill cobre diagramas de sequência Mermaid … isso é um `flowchart`"), deliver exactly the four gates, mark the undefined failing branches with a "Não definido / A definir" node and ask about them |
| 1.2.1 (old_skill) | 2 | 11/12 | 48 279 · 48 321 | Both deliver the same correct flowchart. Run 1 names the skill's boundary only in a closing note; run 2 says the request is a flowchart, not a sequence diagram, but never mentions the skill or its scope (failed assertion 2, borderline). Undefined branches end in "Não avança" / "Deploy interrompido", flagged in prose |

All four blocks re-render with mermaid-cli (exit 0) and every reply reports the Docker
validation that actually ran.

**Reading.** The old skill does not fail this eval outright — the model reaches the right
diagram type on its own — but it treats the scope as an afterthought and once skips it.
The section moves the scope statement to the front consistently and gives the undefined
branches a uniform treatment (a flagged placeholder node, then a question) instead of a
per-run improvisation. Four runs cannot measure a rate (AGENTS.md); what they show is that
the section costs ~500 tokens per invocation and produces the specified behaviour in both
runs, where the unspecified behaviour was right-but-uneven.
