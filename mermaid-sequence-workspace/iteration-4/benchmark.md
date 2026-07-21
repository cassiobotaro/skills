# iteration-4 — targeted re-run of eval 1 against 1.1.2

**Scope.** Not a full set. Iteration-3 failed exactly one assertion (eval 1, "no invented
endpoints, headers, TTLs, or payload fields"): the diagram had added
`Content-Type: application/json` to two Notes, including on the third-party SendGrid call.
1.1.2 amends contract rule 4 to name protocol boilerplate as invented detail. This run
re-executes eval 1 only, to check that the amendment lands.

**Method.** One `with_skill` run against the working-tree skill, hosted Mermaid MCP
connected, `mermaid-cli` absent, installs forbidden.

## Result — the failing assertion now passes

`grep -rniE 'content-type|accept:|charset|user-agent'` over the outputs finds the string
in exactly one place, and it is not in the diagram:

> "I also left the request `Content-Type` out of the note: you said the body is JSON, but
> not which header the endpoint actually expects, and a guessed header is the kind of
> detail that misleads someone debugging a 415."

So the run did more than omit the header — it told the user it had omitted it, and why.
The 415 reasoning is the rationale added to the skill body surfacing in the hand-off,
which is the behavior the amendment was written to produce.

The remaining notes carry only established detail: the public no-auth endpoint with the
`{"email": ...}` body and the 5/hour rate limit, the always-202 anti-enumeration reply,
`Authorization: Bearer (API key)` on the SendGrid leg, and the `Retry-After` header on the
429 branch.

The other five assertions of eval 1 were spot-checked against the output and hold
(fenced block, the given technical details, the rate-limit branch, always-202, `actor`
plus async `-)` for the event legs). They were **not** re-graded by an independent grader —
this iteration only re-tests the one that failed.

## Unchanged: the gate still fires here

The hosted MCP was skipped again (endpoints, header names, payload fields, partner names),
`mmdc` was absent, and the answer states plainly that the code was not validated, pointing
at GitLab's native rendering and mermaid.live, and offering MCP validation if remote
rendering is acceptable. Iteration-3's grader accepted that path — `expected_output`
sanctions "validated, **or** an explicit notice of how to validate".

Tokens 35,691; wall clock 544s (unloaded machine this time, but still not comparable to
iteration-3's concurrent runs).
