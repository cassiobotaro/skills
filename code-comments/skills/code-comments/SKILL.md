---
name: code-comments
license: MIT
description: >
  Decide which comments belong in the source code you are writing or changing, and word
  them, following The Art of Readable Code (Boswell & Foucher). Every code change is also a
  set of comment decisions, and the usual defaults are wrong: comments that restate the
  line below, comments that narrate the edit ("added null check", "fixed the bug"), a
  header that repeats the signature, an invented reason next to a constant, an old comment
  left contradicting the new code. Use this skill whenever you write or modify code in any
  language — implementing a feature, fixing a bug, refactoring, writing a script or a test
  — even when the user never mentions comments, and before handing the change back. Also
  use it for "comment this code", "add docstrings", "clean up these comments", "are these
  comments any good".
---

# Code comments

A comment exists to help the reader know as much as the writer did. The reader is someone
opening this file later, without the conversation that produced it. Everything below
follows from that: write down what you know and the code does not show; write nothing the
code already shows.

## The contract

1. **A comment earns its place.** It must tell the reader something they could not get
   quickly from the code itself. A comment that fails this test is deleted, not reworded.

2. **Record, don't invent.** A *why* comes from the user, from the repository (an issue, a
   test, a commit message, the surrounding code), or from a choice you made yourself while
   writing, in which case you state what you actually know. Never supply a measurement, an
   incident, a requirement or a motive that nobody established. A value you picked without
   a strong reason is commented as that ("arbitrary; any value above the page size
   works"), or not commented. When you cannot establish why existing code is the way it
   is, write no guess: say so in your reply instead.

3. **Comments describe the code, not the edit.** No "added", "fixed", "changed to", "now
   uses", "as requested", no reference to the conversation. That text belongs in the
   commit message and in your reply; in the file it is stale the moment the change lands.

4. **Stay inside the change.** Write and revise comments only in the code you are writing
   or changing. One exception is mandatory: a comment your change makes false is updated
   or deleted in the same change. When the user asks you to comment or review existing
   code, the scope is what they named, and the code itself stays untouched.

5. **Fix the name instead of explaining it.** A comment that exists only to say what an
   identifier means is a sign the name is wrong. For an identifier you are introducing,
   choose the better name and drop the comment. For one that already exists, do not rename
   it: suggest the rename in your reply and leave the decision to the user.

6. **Follow the file.** Write comments in the language of the comments already in the file
   (or, when it has none, in the rest of the codebase); only when there are none anywhere,
   in the language of the conversation. Use the doc-comment form and the marker style the
   project already uses.

## What not to write

- **What the code says.** A restatement of the next line, or of a block whose purpose is
  clear on reading it. The test is *quickly*: a comment over a dense regex or a bit trick
  is worth keeping even though the information is technically in the code.
- **Comments for the sake of commenting.** A function header that repeats the signature
  in prose says nothing. Either it carries something the signature does not (what happens
  at the edges, units, side effects, what is returned on failure) or it is left out. When
  the project requires a doc comment on every function, write it, and make it say one of
  those things.
- **A crutch for a bad name** (rule 5).

## What to write

- **Your thinking.** Why this approach and not the obvious one, what was tried and
  rejected, how good the result needs to be. Only from what is known (rule 2).
- **Known flaws**, with the marker the project uses. Without a project convention:
  `TODO:` for work not done yet, `FIXME:` for code known to be broken, `HACK:` for an
  inelegant solution to a problem, `XXX:` for a serious problem. Say what is wrong, not
  only that something is.
- **Constants.** Why this value, or how much freedom there is to change it: a hard limit
  imposed from outside, a tuned value, or a value that only has to be large enough.
- **The questions a reader will ask.** Read the code as someone new to it; where they
  would stop and wonder ("why not just …?", "can this be empty?"), answer in place.
- **Pitfalls.** What surprises a caller who reads only the name and the signature: a slow
  path, an argument that is modified, a call that can block, an input that is not handled.
- **The big picture**, at the top of a file or a class: what the piece is for and how it
  fits with its neighbors, in a few sentences.
- **Summaries** over the steps of a long function, so the reader gets the outline before
  the detail. A summary states the step's purpose; it does not narrate its statements.

Whether a comment says what, why or how matters less than whether it helps the reader.

## How to word it

- **Compact.** The most information in the least space. Cut words that carry nothing.
- **No ambiguous pronouns.** When "it" or "this" could refer to two things, name the
  thing.
- **Precise about behavior.** Say exactly what a function does where a reader could
  assume otherwise: which characters count, whether a bound is inclusive, what an empty
  input gives.
- **An example for the corner case.** One well-chosen input and output often replaces a
  paragraph. Choose the example that settles the doubtful case, not the easy one.
- **Intent, not mechanics.** State what the code is for at a higher level than the code:
  "show the most expensive items first", not "iterate over the list in reverse".
- **Name opaque arguments.** At a call such as `connect(10, false)`, use keyword arguments
  where the language has them and an inline comment per argument where it does not.
- **Dense words.** A term that packs a whole idea ("cache", "canonicalize", "heuristic",
  "brute force") beats the sentence that describes it.

`references/examples.md` has before/after pairs for each of these. Read it when a comment
passes the test of rule 1 but you cannot get it precise or short.

## Before handing the change back

Go over your own diff once, as the future reader:

1. For each comment you added: does it pass rule 1? Does it describe the code (rule 3)?
   Can you trace every claim in it to the user, the repository or your own decision
   (rule 2)?
2. For each comment near code you changed: is it still true (rule 4)?
3. For the code you wrote: is there a constant, a surprising choice or a pitfall with no
   comment?
4. In your reply, list separately from the change: the renames you suggest (rule 5) and
   the reasons you could not establish (rule 2). Skip the list when it is empty.

Fewer comments is a correct outcome. Code that needs none gets none.

## Attribution

The guidance on what to comment and how to word it is condensed from *The Art of Readable
Code* by Dustin Boswell and Trevor Foucher (O'Reilly, 2011), chapters 5 and 6. See
`NOTICE.md`.
