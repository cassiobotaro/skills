# iteration-11 — smoke test of the dsl-reference prune (structurizr 1.6.3)

**Change under test.** `references/dsl-reference.md` (always read before writing DSL) kept
only the include/exclude expressions and style properties a typical workspace uses; the full
expression grammar and the full style property list moved to `references/dsl-advanced.md`
§7 and §8 (read on demand). The condensed examples were validated against the parser before
the run (`structurizr/structurizr validate`, exit 0). Always-read bytes: `dsl-reference.md`
16 859 → 16 155 (−4.2%); `SKILL.md` 17 226 → 17 401 (+175, the two pointers to the new
sections). `dsl-advanced.md` grew 5 706 → 8 422 but is loaded only when needed.

**Method.** One run of eval 2 (`complete-workspace-from-clear-spec`), the eval whose
assertions exercise styles (cylinder, pipe, external colour) and view syntax. Single arm, no
baseline. The grader re-ran `validate` from `outputs/` and grepped for legacy keywords.

**Result.** 6/6 assertions. The workspace uses only the condensed set (tag-based styles with
`shape`, `background`, `color`; `include *`), validates with exit 0, and carries no legacy
keyword. Tokens 60 302 against 66 753 for the same eval in iteration-9 — single-run noise, not
a measured saving.
