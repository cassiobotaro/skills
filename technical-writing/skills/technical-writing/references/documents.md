# The documents

One entry per kind of document: who reads it, what it holds and in what order, and how it
usually fails. A house template or the docs already in the repository override the order
given here (contract 4). Read only the entry you need.

## Contents

- README
- How-to guide
- Tutorial
- Reference
- Explanation (concept page)
- Runbook
- Release notes and changelog
- Pull request description
- Commit message

## README

**Reader.** Someone who has just arrived and is deciding whether this is what they need,
then how to get it running. Often two readers: the user of the thing and the person who
will change it. Serve the user first.

**Holds, in this order.**

1. What it is and what it does, in one or two sentences, in words the reader would
   search for.
2. The shortest path to a working result: prerequisites, install, one minimal use, and
   what the reader should see.
3. Where the rest lives: links to the guides, the reference, the design docs.
4. For contributors: how to build, test, and send a change.
5. License, and where to ask for help.

Parts 4 and 5 go in only when the repository states them: a license file, a contribution
guide, a named place to ask. Leave out a part it does not state. A heading over a `TODO`
tells the reader nothing about the project, so say in the reply what is missing instead.

**Usual failure.** Commands written from convention instead of from the repository:
`npm install` in a project that uses pnpm, a `make test` target that does not exist. Take
each command from the build and task files. Other failures: the history of the project
before what it does, and a whole guide inlined where a link belongs.

## How-to guide

**Reader.** A competent user in the middle of work, with a goal.

**Holds.** A title that names the task ("How to rotate the signing key", not "Signing
keys"). The prerequisites. The steps, each one an action, starting where a competent
reader already is and stopping when the goal is reached. A fork where the path really
forks: "If you use the managed database, skip to step 4".

**Leaves out.** Teaching and background. One clause of reason at most, then a link to the
explanation. The full list of options belongs to the reference.

**Usual failure.** A guide organised around the tool ("Using the admin panel") instead
of the reader's goal, and steps that describe the screen instead of saying what to do.

## Tutorial

**Reader.** A newcomer learning by doing. They cannot yet tell an important detail from
an incidental one.

**Holds.** What the reader will build, stated at the top ("In this tutorial you will
deploy a two-service application", not "you will learn about deployments"). One path with
no options. A result the reader can see after every step, with what it should look like.
What to check when the result differs.

**Leaves out.** Alternatives, options, and explanation beyond a clause.

**Usual failure.** A step that does not work from a clean state. A tutorial has to be
followed, not only read: run it from the start when the commands change nothing outside
a scratch directory, and when you cannot, say in the reply that nobody ran it.

## Reference

**Reader.** Someone working who needs one fact: a flag, a field, a default, an error
code.

**Holds.** Description and nothing else. The structure of the page mirrors the structure
of the thing: one entry per command, endpoint, or option, in the order the product
presents them. Every entry has the same fields in the same order (name, type, default,
effect, and a short example where usage is not obvious). Completeness matters here more
than anywhere: a missing option reads as an option that does not exist.

**Leaves out.** Instructions and opinion. Link to the how-to guide.

**Usual failure.** Entries of different shapes, defaults remembered instead of read from
the code, and behavior described from the name of an option instead of from what the
code does with it.

## Explanation (concept page)

**Reader.** Someone away from the keyboard who wants to understand why the thing is the
way it is.

**Holds.** One bounded topic, titled as a topic ("About the retry policy"). The context,
the reasons, the alternatives that exist, and what follows from the choice. Reasons come
from the user, the decision log, or the design docs. A reason nobody recorded is a
question (contract 2), because a plausible reason reads exactly like a real one.

**Leaves out.** Steps and option lists.

**Usual failure.** A second copy of the reference in looser words. A decision that is
still open belongs in a design doc, and one decision already made belongs in the decision
log.

## Runbook

**Reader.** The on-call engineer, under pressure, possibly at night, possibly new to this
service. They read with one eye on a dashboard.

**Holds, in this order.**

1. The alert or symptom, in the words the reader sees on the pager or the dashboard.
2. The impact: who is affected, and how urgent it is.
3. How to confirm: a command or a query, and the output that confirms.
4. The mitigation first, then the diagnosis. Stopping the damage comes before
   understanding it.
5. How to undo each step that changes something.
6. When to escalate, to whom, and how to reach them.

Every step is a command the reader can paste, followed by what they should see. A step
that deletes, restarts, or fails over carries its warning before it, never after.

**Usual failure.** A missing actor, which costs more here than in any other document:
"the cache must be cleared" does not say whether the reader clears it or a job does. The
second failure is an invented contact or threshold. Who is on call, which channel, and
what number counts as bad come from the user or the repository.

## Release notes and changelog

**Reader.** A user of the software deciding whether to upgrade and what the upgrade will
ask of them.

**Holds.** What changed from the reader's side, newest version first. What breaks comes
first, with the action it requires: "The CLI no longer reads `~/.toolrc`. Move your
settings to `~/.config/tool/config.toml`." Then what is new, then what was fixed. Each
entry names the behavior, not the implementation, and links to the change. Follow the
format the changelog already uses.

**Usual failure.** A list of commit subjects. "Refactor config loader" tells the user
nothing, and it may hide the one line they needed: that the location of the file moved.

## Pull request description

**Reader.** The reviewer, who has not seen this branch and will give the description
under a minute before opening the diff. Later, someone reading history to learn why the
code changed.

**Holds.** What the change does and why, in the first two sentences. How to verify it:
the command, and the result to expect. What the reviewer should look at closely, and what
the change deliberately leaves out. A link to the issue. Follow the template of the
repository when it has one.

**Leaves out.** The story of the branch (what was tried first, the order of the commits)
and anything the diff already shows line by line.

**Usual failure.** "Tests were added and the handler was refactored": passives that hide
nothing useful and say nothing new. Write what the code does now: "The handler rejects a
payload above 1 MB with `413`. Before, it read the whole body into memory."

## Commit message

**Reader.** Someone running `git log` or `git blame` months later, asking why this line
is the way it is.

**Holds.** A subject line that completes "this commit will…" in the imperative ("Reject
payloads above 1 MB"), short enough for one line of `git log --oneline`. A blank line.
Then a body, when the reason is not obvious from the subject: why the change was needed
and what it does not do. The convention of the repository (a prefix, a ticket id, a
length limit) governs the form.

**Usual failure.** A subject that says which file changed instead of what the change
does, and a body that narrates the work session.
