# Notices and attribution

This skill contains material condensed and adapted from a third-party source. Changes
were made (condensation, reorganization, added guidance).

## The Art of Readable Code — Dustin Boswell and Trevor Foucher

The guidance on what to comment and what not to comment (comments that restate the code,
comments written for the sake of commenting, comments that compensate for a bad name,
recording the writer's thinking, the `TODO` / `FIXME` / `HACK` / `XXX` markers, commenting
constants, anticipating the reader's questions, advertising pitfalls, big-picture and
summary comments) and on how to word a comment (compactness, ambiguous pronouns, precise
descriptions of behavior, input/output examples for corner cases, stating intent, naming
arguments at the call site, information-dense words) is condensed from chapters 5,
"Knowing What to Comment", and 6, "Making Comments Precise and Compact", of **The Art of
Readable Code: Simple and Practical Techniques for Writing Better Code** by **Dustin
Boswell** and **Trevor Foucher** (O'Reilly Media, 2011).

The ideas are restated in this skill's own words. No text and no code example from the
book is reproduced; every example in `SKILL.md` and `references/examples.md` was written
for this skill.

## Not from the book

These rules were added for code written by agents and are not the authors':

- "Record, don't invent": a reason is written only when the user, the repository or the
  writer's own decision established it.
- Comments describe the code and never narrate the edit or the conversation.
- The scope is limited to the code being changed, and a comment the change makes false is
  updated or deleted with it.
- Comments follow the language and conventions already in the file.
- An existing identifier with a poor name is not renamed; the rename is suggested. (The
  book's advice is to fix the name.)
