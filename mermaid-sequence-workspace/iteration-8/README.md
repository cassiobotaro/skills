# iteration-8 — scope eval 6 (flowchart request) against the shipped skill (1.2.1)

**Question.** The skill has no "check the scope" section; what does it do when asked for a
Mermaid *flowchart* of deploy gates (no participants exchanging messages)? Single arm,
`with_skill` = working tree, one run, no baseline. Graded by a subagent following
`agents/grader.md`; the block was re-rendered with the mermaid-cli Docker image (exit 0).

| Eval | Result | What happened |
|---|---|---|
| 6 flowchart of deploy gates | 5/5 | Opens by naming the skill's scope (sequence diagrams) and that this is decision logic, then delivers a `flowchart TD` with exactly the four gates; adds a "Deploy interrompido" terminal for the undefined failing-tests/smoke branches and flags it as its own choice; validated with Docker |

Tokens: 50,813 (85 s).

**Reading.** The expected failure (no scope statement) did not happen: the model named the
boundary on its own. The body still has no section telling it what to do here, so this is one
run of a behaviour the skill does not specify; a scope section remains the consistent fix.

**Spec changes made from the grader's feedback** (in `evals/evals.json`): the "no invented
steps" assertion now says a *flagged* terminal for the undefined branches is acceptable and an
unflagged route to rollback is not; the unverifiable "does not install" assertion became "states
how the block was validated, never claims a validation that did not run"; a deterministic
"renders with mermaid-cli" assertion was added.
