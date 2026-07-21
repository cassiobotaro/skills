# iteration-6 — full eval set against 1.1.3

**Question.** Iterations 4 and 5 were both targeted single-eval re-runs (eval 1). 1.1.3's
changes — the sensitivity gate declining mermaid.live, the canonical example losing its
`Content-Type` header — had never been measured against the rest of the set.

**Method.** All six evals, one `with_skill` run each, against the working-tree skill. Hosted
Mermaid MCP connected, `mermaid-cli` absent, installs forbidden. Evals 4 and 5 carry
environment constraints in the prompt (eval 4: no MCP at all; eval 5: MCP present but the
flow is confidential) and their runs were held to them.

## Result — 33/33 (100%), no failures

| Eval | Passed | Tokens |
|---|---|---|
| 0 vague-checkout-asks-questions | 3/3 | 25,735 |
| 1 detailed-password-reset-flow | 6/6 | 30,678 |
| 2 order-api-from-code | 6/6 | 35,204 |
| 3 large-delivery-saga-split | 7/7 | 40,499 |
| 4 no-validator-available-says-so | 5/5 | 29,015 |
| 5 sensitive-flow-skips-remote-validator | 6/6 | 30,038 |

Total 191,169 tokens, mean 31,861.

## What the grader established independently

- **Machine parse where it was legitimate.** The grader (not the run) put eval 2's block and
  all five of eval 3's blocks through the hosted MCP. Eval 3's five all rendered. Eval 2's
  returned only `Generated PNG exceeds size limit of 512000 bytes` — an output-byte cap, not
  a parse error; the grader proved the distinction with a deliberately broken control that
  returns `Parse error on line N`.
- **Manual syntax review where a machine parse would have defeated the test.** Evals 1, 4
  and 5 are precisely the diagrams the skill withheld from a remote renderer. Sending them
  to the hosted MCP to grade them would have leaked exactly what the skill refused to leak,
  so those three were reviewed against `references/syntax.md` instead.
- **The split rule holds.** Eval 3's five blocks run 14 / 18 / 10 / 13 / 13 messages — max
  18, under the ~25 ceiling, with consistent participant ids across diagrams.
- **The sensitivity gate fired on four of six evals** (1, 2, 3, 5) and in every case declined
  the hosted validator, pointed at the repo's own native rendering, and left the hosted
  route to the user as an explicit choice. mermaid.live was never offered as the fallback.

## Assertions worth rewording

- **eval 0 a3** ("any mermaid code included parses cleanly") is vacuous when the run
  correctly delivers no diagram — the pass is accidental rather than earned. It should read
  "…or no mermaid code at all".
- **evals 4 and 5**, "does not install anything" / "does not call the hosted MCP" are
  negative claims about tool use, but the only preserved artifact is the response text. The
  grader inferred them from the absence of install strings and of a hosted-preview link
  (`l.mermaid.ai`), which is what a hosted call always returns. To make them genuinely
  verifiable the harness would have to persist the tool-call log next to the response.
- **eval 1 "nothing invented"** passed, with two soft glosses flagged: a note reads
  `Authorization: Bearer (API key)` — the "(API key)" is the run's — and the web app's UI
  replies were not in the prompt. Neither is an endpoint, header, TTL or payload field, so
  neither counts under the assertion as written.
