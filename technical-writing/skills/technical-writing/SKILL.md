---
name: technical-writing
license: MIT
description: >
  Write, revise, and review technical documents so that the reader can act after one
  reading: a README, a how-to guide, a tutorial, a reference page, a concept page, a
  runbook, release notes, a changelog entry, a pull request description. The skill fixes
  the reader and the one job of the document, then writes in the active voice, where every
  verb has a named actor, looked up in the code and never guessed, and where every
  command and output comes from the repository. Use this skill whenever the user asks to
  write, update, improve, or review documentation or one of those documents ("write the
  README", "document how to deploy this", "review this runbook", "write the PR
  description", "escreve a documentação", "melhora esse README"), even if they never say
  "technical writing", and when another skill tells you to apply it to prose that skill
  wrote. Do not use it for a design doc, an ADR, a diagram, code comments, an email or a
  chat message, an explanation asked in conversation, or a request to run unslop by name.
---

# Technical writing

A technical document works when its reader can act after one reading: run the service,
clear the alert, review the change. Two things decide that more than style does. The
document does one job for one reader, and every sentence says who does what.

## The contract

1. **Every verb has an actor.** For each verb, the sentence says who or what performs the
   action: a person, a team, a component, a command, the reader. "The payload is
   validated" withholds a fact the reader needs: which service to open, whom to page,
   whether the step is theirs. The reader fills the hole with a guess. Write the actor as
   the subject of an active verb: "The gateway validates the payload". Section 4 has the
   test and the few passives that stay.

2. **Look the actor up, never pick one.** A passive is a question: who does this? The
   answer is in the code, the configuration, the existing docs, or the conversation, so
   read them. When none of them answers, the question goes to the user. A plausible
   component written as the actor is a fabrication that reads like knowledge. The same
   rule covers every command, flag, path, default, version, and output: copy it from the
   repository or from a run of the command, never from how such tools usually work. It
   also covers behavior: write what the code does. A likely cause, or what systems of
   this kind usually do, is marked as a guess or left out.

3. **One reader, one job.** Fix who reads and what they do next before writing a
   sentence (section 1). A document does one of four jobs (section 2). A page that
   teaches, instructs, lists, and argues at once serves no reader well.

4. **The house governs.** A style guide, a template, or the docs already in the repository
   set the terms, the heading style, and the structure. A new document follows the
   language of the repository's docs directory (`docs/`, `doc/`, or the like) when there
   is one with documents in it, and the language of the conversation otherwise. A
   language the user names wins over both. In a revision, the author's language,
   structure, voice, and facts stay.

## Writing a document

### 1. Fix the reader and the task

Settle two things from the request and the repository: who reads (their role, and what
they already know about this system) and what they must be able to do after reading. The
document holds what the task needs minus what the reader already knows. The usual failure
is the writer's own knowledge: a term the team uses every day is unknown one team away.

Do not interview. Ask only when two plausible readers would get very different documents
and nothing decides between them. Otherwise write for the most likely reader and name that
reader in one line of the reply, so that one word corrects it.

### 2. Choose the job

Ask what the reader is doing when they open the page.

| The reader is | Job | It holds | It leaves out |
|---|---|---|---|
| learning by doing | Tutorial | one path that works, a visible result at every step | options, alternatives, explanation beyond a clause |
| working toward a goal | How-to guide | the steps to that goal, for a competent reader | teaching, background, the full list of options |
| looking up a fact mid-task | Reference | description only, complete, in the shape of the thing described | instructions, opinion, history |
| trying to understand | Explanation | context, reasons, alternatives, consequences | steps, exhaustive detail |

When the material spans two jobs, write two documents and link them. A README is the one
mixed page: a short piece of each job, with links to the rest. Before writing any of
these, or a runbook, release notes, a changelog entry, a pull request description, or a
commit message, read the entry for that document in `references/documents.md`.

### 3. Collect the facts

Read the source before drafting: the code paths the document describes, the build and
task files, the configuration, the existing docs. For each action the document will
mention, find its actor now. Run a command to confirm it only when the run changes
nothing (a read, `--help`, a dry run). Keep a list of what you could not confirm.

When the repository leaves a hole the document cannot work around (what the service is
for, who is on call, which environment the steps target), ask before writing: two to four
questions, batched, in the conversation language. Do not ask what you can read yourself.
When the user wants the document before they can answer, write it and mark each hole
where it falls, as a `TODO` that says what is missing. Never paper over a hole, and list
every one in the reply.

### 4. Draft, then run the actor pass

Draft with the rules of the next section. Then go through the draft one verb at a time
and ask "who or what does this?" The sentence has to answer.

Rebecca Johnson's test finds the passives fast: if "by zombies" fits after the verb, the
verb is passive ("por zumbis" in Portuguese). "The cache is invalidated [by zombies] on
deploy." Zombies fit because the sentence never said who invalidates the cache, and that
missing name is what you now look up. The test catches only the first of the six places
where the actor hides, so the question still goes to every verb:

- **A passive without its agent.** "The cache is invalidated on deploy" becomes "The
  deploy job invalidates the cache".
- **A noun that swallowed the verb.** "After validation of the token" becomes "After the
  gateway validates the token".
- **A subject that means nothing.** "It is recommended to", "there is a retry", "é
  necessário configurar". Write who recommends, what retries, who configures.
- **A catch-all actor.** "The system", "the application", "the process", when the system
  has several parts. Name the part.
- **An instruction written as a description.** "The variable must be set" becomes "Set
  the variable". The actor is the reader, so use the imperative.
- **In Portuguese, the forms with "se".** "Envia-se", "configura-se", "deve-se" hide the
  actor as "é enviado" does.

Two passives stay:

- **The actor is unknown, and the text says so.** "The index was dropped at 14:02. The
  audit log does not record by whom."
- **The verb describes a state, and no reader would ask "by whom?"** "The service is
  written in Go." "This endpoint is deprecated."

A passive that names its actor with "by" is rewritten like any other. When the paragraph
follows one thing through the system and that thing should stay at the front of the
sentence, give it an active verb: "The request then goes to the gateway, which signs it".

`references/actors.md` has before and after pairs for each case, in English and in
Portuguese. Read it when a sentence resists the rewrite, when the document is in
Portuguese, or when you review a text you did not write.

### 5. Apply `unslop`, then check

When the `unslop` skill is installed, invoke it on the prose you wrote or rewrote in this
turn, after the actor pass. It owns the catalog of machine-writing patterns, and this
skill does not repeat that catalog. A fact that skill finds missing is a question for the
user (contract 2). Then check:

- Every verb has an actor, and each passive left is one of the two that stay.
- Every command, flag, path, name, and output exists in the repository or came from a run.
- The first paragraph alone tells the reader what this is and whether to read on.
- The document does one job. Material for another job is a link.
- Each thing has one name, and it is the name the code uses.
- A final read as the reader fixed in step 1, from the top, doing what the page says.
- After a revision, the reply says what changed in three lines at most and retells
  nothing the document says. The user has the file.

## The rules

### The document

- Lead with the point. The first paragraph says what the thing is and what the reader
  gets from the page, in words they would search for. Many readers stop there.
- State what the document covers, and what it leaves out that a reader would expect to
  find. Put prerequisites before the first step.
- A heading says what its section holds. A heading for a task starts with a verb.
- Cut what the reader's task does not need. Link to a detail instead of repeating it.

### The paragraph

- The first sentence states the point of the paragraph. One topic per paragraph.
- Start a sentence with what the reader already has, and end it with what is new. The
  end of the sentence is where the reader puts the emphasis.
- Use a numbered list for a sequence, bullets for parallel items, a table for items
  compared on the same attributes, and prose for reasoning, because a list drops the
  connectives. Introduce a list with a full sentence and keep its items parallel.

### The sentence

- Actor, verb, object, in that order, with the subject next to its verb.
- Let the verb carry the action: "validates", not "performs the validation of".
- One idea per sentence. Put the condition before the instruction: "To roll back, run…",
  "If the check fails, restart the worker".
- Present tense. Address the reader as "you", in the form of address the house uses.
- Prefer the positive form, and never stack negatives: "the job retries once the lock
  is free", not "the job does not retry unless the lock is not held".
- Write the number with its unit, and the exact name. "Slow" and "some errors" cannot be
  acted on, and "p95 above 800 ms" and "`ERR_QUOTA`" can.

### The words

- One name per thing, everywhere, and the name the code uses. A second name reads as a
  second thing.
- Define a term where it first appears. Spell an acronym out once, and only when the
  document uses it several times.
- "It", "this", and "they" point at one noun the reader has just read. Otherwise repeat
  the noun.
- Identifiers, commands, paths, and values go in code font, spelled as in the source.
- Leave "simply", "just", "easy", and "obviously" out of instructions. They tell the
  reader who is stuck that the fault is theirs.

### Procedures and samples

- One action per step, numbered, each step starting with an imperative verb. Say where
  before what: "In `config/app.yaml`, set…".
- Put a warning before the step it guards.
- After a step with a result the reader can check, show that result.
- A command block holds only what the reader types, with no prompt character. Mark a
  placeholder as `<name>` and say what replaces it.
- A sample runs as written, is as small as the point allows, and says how to run it and
  what it prints.

## Revising and reviewing

**"Improve", "revise", "update".** Edit the file. Keep the author's structure, voice, and
every fact (contract 4), and change what the rules above call for. A passive whose actor
the repository does not give stays as it is and becomes a question in the reply. Do not
delete the sentence and do not guess.

**"Review".** Report before editing, in two groups: questions for the author (an actor
or a fact that only they know, a reader the document never settles) and proposed edits,
each with its reason. Quote the sentence. Apply what the user chooses.

## When another skill calls this one

Apply the actor pass (step 4) and the rules for the sentence and the words to the prose
that skill wrote in this turn, before `unslop` runs. Structure, headings, templates, and
tool-parsed text belong to the calling skill and stay as they are. An actor nobody
established goes where that skill puts its open questions. Add no report of your own.

## Deliver

- **A new document.** Write it where the repository keeps its docs and report the path.
- **A revision.** Edit in place, report the path, and say in at most three lines what
  changed.
- **A short text** (a pull request description, a commit message). Reply with the text
  ready to paste. Do not post or commit it unless the user asked.

After the result, list only what applies: the reader you assumed, the questions left
open, and the commands you did not run. Do not summarize the document.

## Reference files

| File | Read it when |
|---|---|
| `references/documents.md` | Before writing or reviewing a specific kind of document: what each one must hold, its order, and its usual failure. |
| `references/actors.md` | A sentence resists the actor pass, the document is in Portuguese, or you review a text you did not write. |

## Attribution

The layered structure follows the `technical-writing` skill of
[pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan, licensed MIT.
The rule that every verb has an actor follows Tanya Reilly's *The Staff Engineer's Path*.
The four jobs are Daniele Procida's Diátaxis. The rules condense Google's Technical
Writing courses and developer documentation style guide, the Microsoft Writing Style
Guide, the US federal plain language guidelines, Write the Docs, and George Gopen and
Judith Swan's "The Science of Scientific Writing". The "by zombies" test is Rebecca
Johnson's. See `NOTICE.md`.
