# Maintaining the skills

Read this before changing anything under a `skills/` directory. It is not loaded automatically:
`AGENTS.md` points here so that a description of what the skills are expected to do stays out of
the context of eval runs (see `eval-tools/README.md`).

Each note says what the skill does, which decisions are easy to undo by accident, the numbers
that made them, and what is open. Numbers are on claude-sonnet-5-5 unless a model is named; the
runs behind them are in the git tag `archive/evals-2026-11-23`, under the path given in
parentheses. Few runs measure no rate: read "4/4" as "every time", not as 100%.

## Shared contract

- **Record, don't invent** is the shared contract across every skill: a skill states as fact only what the user or the repository established, and a gap is never filled with a guess. What a skill does with the gap depends on what it delivers. The skills that write a document or a diagram (`adr`, `design-doc`, `structurizr`, `mermaid-sequence`) ask: when the request is too vague to fill the sections honestly, they ask 2–4 targeted questions instead of fabricating, and the questions are the deliverable. Every other skill states its own form of the contract in its note below, and a new skill does the same instead of being added here as an exception.
- **Validation tooling**: no skill uses an MCP, and `adr`, `design-doc`, `unslop`, `code-comments`, `explain` and `technical-writing` use no external tooling. `structurizr` validates, previews and exports through the `structurizr/structurizr` Docker image (PNG/SVG only through its `<version>-playwright` variant; the regular image refuses them), and `mermaid-sequence` validates through the `minlag/mermaid-cli` Docker image with a local `mmdc` as fallback. Without Docker (or the CLI), both ship the artifact with an explicit "not validated" notice plus the command to run later — **never an install attempt, never a remote validator**.
- **Calling `unslop`**: `adr`, `design-doc`, `explain` and `technical-writing` invoke `unslop`, when installed, on the prose they wrote, and each keeps its own short floor of prose rules for an install without it. On opus, in one session that follows the caller, every caller reaches it (see the `unslop` note); on sonnet and haiku `technical-writing` and `explain` mostly do not.

## adr

adr-tools-compatible decision log: `NNNN-slug.md`, `doc/adr` by default, `.adr-dir` override, an `adr init`-style seed on a fresh log, supersede and amend by editing the *old* record's Status section only; records are otherwise immutable.

Do not undo:

- The slug is ASCII-only, as adr-tools computes it on Linux (`tr -Ccs [:alnum:] -`): an accented letter becomes a hyphen (`decisões` → `decis-es`), never transliterated and never kept.
- `Superseded`/`Supersedes` on write; the legacy `Superceded` is recognized on read.
- Tool-parsed scaffolding (`Date:`, the `## Status/Context/Decision/Consequences` headings, status words, supersede/amend verbs) stays canonical English in a log in any language, because Structurizr's `!adrs` importer and `adr generate` parse those literals. Only the prose is translated.
- A scope check up front hands an open design to `design-doc`, refuses to record a choice not yet made, and leaves `!adrs` wiring to `structurizr`.
- Since 1.6.0 the third ingredient of a record is the *trade-off* (what the decision gives up for what it gets), not a negative consequence. With none given, the skill asks once and never supplies one; if the answer is that there was none, it writes the record without one and says so (eval 12).
- `unslop` (since 1.5.0) touches only the title text and section bodies of the record being written; scaffolding, the seed and every existing record are out of its reach.

Measured: what a session without the skill already does is in iteration-17 (`adr-workspace/iteration-17/README.md`); read it before cutting anything. In a project holding the log, 16/16 sessions invoked the skill as the first tool call, including two requests that never say "ADR" (`adr-workspace/trigger-evals/in-project-2026-11-22/`).

## design-doc

Writes, reviews and updates design docs through interactive discovery; trade-offs are mandatory, and a doc with no cons is a red flag.

Do not undo:

- A change with no choice left open gets no doc: the skill says so and asks once, writing a terse mini-doc only when the team's process requires one.
- A doc whose design changed is edited in place until the system ships; after that its body is left alone and the change goes into a linked amendment (`Amended by` in the original's header is the only edit).
- Invention by consequence is named in the contract: a fact cannot be asserted in one section and asked in Open questions. The "do nothing" alternative is always written, but only from the pain the user described; with none described it becomes a question.
- **A risk nobody raised is invention and becomes a question** (contract 2, 1.10.0). Without it, a user who cannot answer now got a Riscos section filled with risks nobody gave (a Redis dependency, a 24-hour window): 4 of 20 documents clean with 1.9.0, 8 of 8 with 1.10.0 on sonnet, 4 of 4 on opus (`design-doc-workspace/iteration-28/`, eval 71 in the set). Two rejected attempts are worth knowing: the words "or nobody is there to reply" made the skill write without asking first, and a self-review bullet that deleted unsupplied risks did the same on the plain request (eval 7). Measure eval 7 beside any change of this kind.
- A user-supplied or house template **governs** (its sections become required); only without one are sections suggestions. A review never audits section presence: it analyzes the sections the author wrote and proposes a section only when the content calls for it.
- Diagrams: the C4 architecture is Structurizr DSL (delegated to `structurizr` when present), embedded as a PNG/SVG reference with the DSL folded in a `<details>` block; sequence flows stay Mermaid. No "not machine-validated" disclaimer.
- The write step does **not** call `technical-writing`. 1.7.0 did, and 98/104 against 98/104 checks showed nothing it adds, for ~15% more cost; 1.8.0 went back to 1.6.0's text (`design-doc-workspace/iteration-27/`). Do not put the call back without a check that separates the versions.
- The description names update requests for a design doc (1.9.0). Without that clause, 16/16 sessions asked to update a shipped design doc rewrote its body without consulting the skill; with it, 8/8 invoked the skill and none touched the body. Quoting "update the docs" generically also fired on pages that are not design docs (2/8), so the clause names the design doc on purpose. The description is 1013 characters, eleven under the limit.

Open: on sonnet, 1.10.0 kept the accepted cost (+5 ms) under its own heading in 3 of 8 documents against 8 of 12 with 1.9.0 (check 7.11); it did not show on opus. If it returns, the fix goes in the paragraph or step 3, not in removing the paragraph. On opus, 2 of 4 documents put a `### Visão geral` inside the template's Proposta (check 7.5).

## structurizr

Authors and edits `workspace.dsl` (C4 model, Structurizr DSL v6+). Validation is Docker-only (`structurizr/structurizr validate`); without Docker the workspace is delivered with "not validated, here is the command".

Do not undo:

- ADR authoring is routed to the team's decision log, not written by this skill.
- References are an always-read core (`dsl-reference`) plus conditional pattern files; the export commands are one of them (`export`), so the hand-off carries only the preview.
- Theme tag names in the references are checked against the theme files the image bundles: a tag the theme does not define draws no icon and nothing reports it (1.6.4 carried two that `amazon-web-services-2025.07` had renamed).

Measured: in a project holding the workspace, 8/8 sessions invoked it first on evals 3 and 11, 4/4 on a new workspace, 0/4 on real AWS icons (excluded) (`structurizr-workspace/trigger-evals/in-project-2026-11-23/`). With `adr` installed too (claude-opus-5-5, 2026-11-23, four sessions, `probe_in_project.py`): every session invoked `adr` first and `structurizr` second, added `!adrs docs/adr` at workspace scope, and left the ADR unwritten because the request gives no reason for the decision; each asked for the reason, the trade-off, the status and whether 0004 supersedes or amends 0003, and asked before changing the queue's technology in the model. The two skills split the request as designed.

## mermaid-sequence

Mermaid sequence diagrams as fenced ` ```mermaid ` blocks; the flow and its failure paths are never invented, and technical detail (endpoint, headers, payload, status) goes in Notes.

Do not undo:

- Validation is local-only and ordered: mermaid-cli Docker image → local `mmdc` → "delivered, not validated, here is the Docker command". mermaid.live renders remotely, so for diagrams with internal detail it is the user's call.
- `references/syntax.md` is always read (version portability and escaping gotchas).

Measured: invoked first in 6/6 sessions with the code in the project, 6/6 with the flow in the message, 0/6 on a flowchart (`mermaid-sequence-workspace/trigger-evals/in-project-2026-11-23/`).

## unslop

Edits prose to remove machine-writing patterns; the one skill that owns that catalog, so other skills apply it by name instead of carrying a copy.

Do not undo:

- Rule ids are stable (`S1`–`S21` in `SKILL.md`, `EN*`/`PT*` in one vocabulary file per language); a removed rule leaves a gap, because other skills may cite an id.
- Its form of the shared contract is "remove, never supply": a rule that needs a fact the text lacks deletes the claim or asks. It never edits code, diagram source, quotations, tool-parsed text, or a file that records history.
- **Explicit only, by its description and not by `disable-model-invocation: true`.** With that flag Claude Code's Skill tool refuses a call that comes from another skill (`unslop-workspace/smoke-2026-11-21/`), and the flag is not in the Agent Skills standard. pstack's `unslop` uses the flag; this repository cannot.

Measured: 0/30 false fires in the routine trigger check, including requests for this job that do not name it; 21/21 on positives that carry their text. With the skill read, 109/110 checks against 98/110 without; what it adds is on the "without adding a fact" side (`unslop-workspace/iteration-1/`). It never fired on its own in 56 in-project sessions of other skills.

**Called by another skill, it runs on opus and is mostly skipped on sonnet and haiku.** On claude-opus-5-5, with the current texts, `unslop` followed `technical-writing` in 12/12 sessions (after the document was written, then edits) and `explain` in 4/4 (loaded before the reply was written) (`unslop-workspace/trigger-evals/called-by-skill-opus-2026-11-23/`). On sonnet it followed `technical-writing` in 1/12 and `explain` in 0/4, and `design-doc` in 8/8. An A/B on sonnet ruled out the description as the cause (3/12 without "Explicit only."), and two rewordings of the callers moved it only partly: invoke before replying, 5/12 after `technical-writing`; load before drafting, 3/4 after `explain` and 0/12 after `technical-writing` (`unslop-workspace/trigger-evals/called-by-skill-2026-11-23/`). The author runs opus, so the texts were left as they are (2026-11-23).

**Where it is still skipped on opus: delegation and lost context** (2026-11-24, `probe_in_project.py` with `--spec`, `--allow-agent` and a `followup` turn; runs not kept, the README is in the run directory of that date). On opus `adr` reached `unslop` in 4/4 and `design-doc` in 4/4. In a second turn of the same session neither the caller nor `unslop` is invoked again (0/8), and six of the eight still made the pass from the loaded text: the Skill-call count is not the behavior there, so read the turn's edits. Asked to split eight ADRs among four subagents, the main session wrote every brief with the step as a condition ("Se a skill `unslop` estiver disponível…", "Se for o caso…"), never ran `unslop` itself over what came back (0/6), and 2 of 16 subagents skipped it, both under the weakest wording. The author's real misses match: a `poop` session whose subagent briefs said "If the `unslop:unslop` skill is available to you" (2 of 6 skipped), and ADRs written after the session had been compacted, which the probes did not reproduce. A sentence in each caller fixed the delegation case: the pass stays in the session that loaded the skill, runs on what the subagents wrote once they return, and is never handed on as a condition. With it, on `adr` (1.7.0), every session ran `unslop` in the main session after its subagents (4/4, canaries 2/2, against 0/4), and the single-turn evals 5 and 11 stayed at 4/4. `design-doc` 1.11.0, `technical-writing` 1.1.0 and `explain` 1.1.0 carry the same sentence, unmeasured with delegation. Do not move the step back into the briefs. Open: a compacted-session probe.

## code-comments

Governs the comments of code an agent writes or changes, in any language. The trigger is "whenever you write or modify code", so the `SKILL.md` body is short (it is read on every coding task) and the before/after pairs sit in `references/examples.md`.

Do not undo:

- The guidance condenses chapters 5 and 6 of *The Art of Readable Code* (Boswell & Foucher) in the skill's own words; no text or example from the book is reproduced, and it must stay that way.
- Five rules are not the book's and are listed in `NOTICE.md`: a reason is written only when the user, the repository or the writer established it (an unknown reason goes in the reply, never guessed in the file); comments describe the code and never narrate the edit; the scope is the code being changed plus any comment the change makes false; comments follow the language of the file, then the codebase, then the conversation; an existing identifier with a poor name is **not renamed**, the rename is suggested in the reply.
- It is the one skill that does not stop to ask, because its deliverable is someone else's code change.
- 1.1.0's clause covers pasted code with a one-line change (1/15 → 11/15 on such requests). The description is 1022 characters, two under the limit.

Measured: 84/86 checks with the skill against 79/86 without; the one separation is the rename suggested and not made (`code-comments-workspace/iteration-1/`). **In a project holding the file it is not consulted**: 0/16 on code changes that do not mention comments, while the same description reads 27/30 with the code pasted (`code-comments-workspace/trigger-evals/in-project-2026-11-22/`). The edits of those sessions met every comment assertion except the rename suggestion, so **the author accepted the miss** (2026-11-23). Reopen on evidence that sessions without the skill write bad comments in a project.

## explain

Explains a topic to one reader, and writes or revises texts for other people (messages, emails, replies); one skill for both because the same four questions govern them: who reads and what they know, what contrast is in play, which one or two reasons matter, what the reader does afterwards.

Do not undo:

- **No output template.** The research behind it found no named format (ELI5, Feynman, BLUF, ADEPT) tested against another, and found that instructions by adjective ("be simple", "use analogies") are the conditions under which machine explanations fail. The skill instructs procedures instead.
- It **explains first** at a stated assumed level and asks first only when two readers would get very different answers. A Socratic gate on a one-off question is banned; the teaching loop is opt-in.
- An analogy is optional, covers one aspect, and carries its mapping and its breaking point. A closing check is conditional, never a fixed ending. Simplifying changes the form and keeps the scope of the claim.
- No effect size is stated anywhere in the skill, and no learning gain is claimed.
- Its form of the shared contract is "facts are recorded, illustrations are built": built examples and numbers are shown as illustrations; in a text for someone else a missing fact becomes a bracketed gap listed after the text.
- `unslop` runs only on a text drafted for a third party: never on an explanation (S13 and S19 would strip the closing check and the analogy) and never on the user's own draft.
- All before/after pairs were written for the skill; ones that echoed a source were replaced.

Measured: 165/178 checks with the skill against 151/178 without; the clearest effect is the teaching loop (`explain-workspace/iteration-1/`). Failing in both cells: a borrowed term left undefined (`asyncio`, eval 4), and the three-lines-on-what-changed rule, which the judges count strictly (`explain-workspace/iteration-2/`). Triggering: 33/33 positives, 0/33 false fires; in a project, 12/12 with a fixture (`explain-workspace/trigger-evals/in-project-2026-11-23/`). **A message that is one step of a code task was missed** (2026-11-24, opus): "change MAX_ATTEMPTS and write a short message to #exports" invoked no skill in 0/4, and the messages came out with an emoji title, decorative bold and a courtesy closer, with no gap listed; `technical-writing` on the same shape of request (code plus a new doc) fired 8/8. 1.2.0 adds "and when the text is one step of a larger task ("change the code and tell the team")" to the description (984 characters): 4/4 on that request, `unslop` after it in 4/4, and the routine trigger check the same day gave 33/33 and 0/33 on both texts, canaries 3/3.

## technical-writing

Writes, revises and reviews technical documents (README, how-to, tutorial, reference, concept page, runbook, release notes, changelog entry, pull request description; a commit message only when asked). The body is a procedure (reader, job, facts, draft, actor pass, `unslop`, check) followed by rules in five layers; per-document guidance and pairs sit in `references/documents.md` and `references/actors.md`.

Do not undo:

- **Every verb has an actor**, written as the subject of an active verb. It follows a passage of Tanya Reilly's *The Staff Engineer's Path* that the author supplied; the book was not consulted while writing, and no sentence of it is in the skill. The rule is about information, not grammar, which keeps it from contradicting `explain`. Two passives stay: the actor is unknown and the text says so; the verb describes a state. The "by"-passive in a paragraph about the object was removed before release; do not put it back as a readability fix.
- Its form of the shared contract is "look the actor up, never pick one": it asks only after reading the repository, and every command, flag, path, default and output comes from the repository or from a run that changes nothing.
- In a revision, a passive whose actor the repository does not give **stays** and becomes a question, where `unslop` would delete the claim. The difference is on purpose.
- It owns no typography rule and no list of machine-writing patterns; it calls `unslop` after the actor pass. `design-doc`, `adr` and `explain` do not call it (see their notes).
- A new document follows the language of the repository's docs directory when it has documents, the conversation's otherwise; a request that names a language wins.
- No limit counted in words, and no pair copied from a source.
- A README includes contributing, license and help only when the repository states them (1.0.1; 4/4 against 0/2).

Measured: 231/242 checks with the skill against 203/242 without; what separates is reading the repository before writing a new document (without the skill, a generic runbook with an invented escalation limit), the shape of a review and of a PR description (`technical-writing-workspace/iteration-1/`). 1.0.1 showed no regression on evals 3 to 6 (`iteration-3/`). Triggering: 30/30 positives, 0/30 false fires; in a project, 20/20 (sonnet) and 16/20 (haiku, which writes reviews without it).

Accepted (2026-11-23): the three-line rule after a revision stays; its checks were amended, since the sentence mapping each component to its actions is the change asked for. A one-value change ("subimos o limite pra 250 mil linhas") is not routed to the skill (0/8); the sessions changed only the number and flagged the code's value, so the miss was accepted. Open: "Once the upload is done" survives in 5 of 6 documents, and judges split on whether it is a passive or a state.
