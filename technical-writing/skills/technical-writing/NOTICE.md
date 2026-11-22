# Notices and attribution

This skill condenses and adapts guidance from the sources below. Changes were made in
all cases (selection, rewording, reorganization, added guidance). No text and no example
is reproduced from any of them: every before and after pair in `SKILL.md` and under
`references/` was written for this skill.

## pstack — Lauren Tan

The idea of a layered writing standard (the kind of document first, then the sentence,
then the word), the delegation of machine-writing patterns to a separate `unslop` skill,
and the treatment of pull request descriptions and commit messages as writing come from
the `technical-writing` skill of **pstack** by **Lauren Tan**, version 0.15.46:
<https://github.com/cursor/plugins/tree/main/pstack>

pstack is licensed MIT:

> MIT License
>
> Copyright (c) 2026 Lauren Tan
>
> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all
> copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
> SOFTWARE.

What differs from the pstack skill:

- The pstack skill is a list of rules in four named layers (Diátaxis, Google developer
  style, Simplified Technical English, Global English). This skill is a procedure (reader,
  job, facts, draft, actor pass) followed by the rules, and it drops the limits counted in
  words.
- pstack allows the passive "when the actor is unknown or beside the point". This skill
  makes the actor the first rule of its contract, says where the actor is looked up, and
  says what happens when the source does not name one.
- The pstack skill runs only when the user names it. This skill also runs when the user
  asks for a document it covers.
- Rules about typography (dashes, semicolons, slashes) are left to this repository's
  `unslop` skill.

## Diátaxis — Daniele Procida

The four kinds of documentation (tutorial, how-to guide, reference, explanation), the two
questions that tell them apart (action or cognition, acquisition or application), the
rule that one document does one job, and most of what `references/documents.md` says
about those four kinds are condensed from **Diátaxis**:
<https://diataxis.fr/>

## Technical Writing One and Two, and the developer documentation style guide — Google

The definition of a document as what the audience needs minus what it already knows, the
opening sentence that states the point of a paragraph, the choice between a numbered
list, a bulleted list, and a table, parallel list items, the replacement of "there is"
and of weak verbs, one term per thing, the rule for pronouns, scope and non-scope stated
up front, the properties of sample code, and the condition placed before the instruction
are condensed from:

- <https://developers.google.com/tech-writing/one>
- <https://developers.google.com/tech-writing/two/sample-code>
- <https://developers.google.com/style/highlights>

## Microsoft Writing Style Guide

One action per step, the imperative verb at the start of a step, and the place of the
action stated before the action are condensed from:
<https://learn.microsoft.com/en-us/style-guide/procedures-instructions/writing-step-by-step-instructions>

## Federal plain language guidelines (United States)

The verb hidden in a noun, the preference for the positive form, and the warning against
stacked negatives are condensed from:
<https://digital.gov/guides/plain-language>

## Write the Docs

"Incorrect documentation is worse than missing documentation", which stands behind
contract 2, and the advice to begin a paragraph with its key concept come from the
documentation principles of **Write the Docs**:
<https://www.writethedocs.org/guide/writing/docs-principles/>

## The Science of Scientific Writing — George D. Gopen and Judith A. Swan

The subject kept next to its verb and the sentence that starts with what the reader
already has and ends with what is new are condensed from **George D. Gopen** and
**Judith A. Swan**, "The Science of Scientific Writing", *American Scientist* 78 (1990).
The article also argues for a passive that names its actor when the paragraph is about
the object. This skill does not follow it there: it keeps the object at the front of the
sentence with an active verb instead.

## The Staff Engineer's Path — Tanya Reilly

The first rule of the contract (be clear about who or what does the action of every
verb, because a passive makes the reader guess, and write an active verb whose subject
does the action) follows a passage of **Tanya Reilly**'s *The Staff Engineer's Path*
(O'Reilly Media, 2022). The same passage quotes Rebecca Johnson's test, credited below,
and that is how the test reached this skill. The passage was supplied by this
repository's author, who read it in the book. The book was not consulted while the skill
was written, and no sentence and no example of it is reproduced.

## The "by zombies" test — Rebecca Johnson

The detector for the grammatical passive in step 4 of `SKILL.md` and in
`references/actors.md` (if "by zombies" fits after the verb, the verb is passive) is
**Rebecca Johnson**'s, then a professor at Marine Corps University, who published it on
Twitter on 18 October 2012. The wording was taken from Tanya Reilly's quotation of it
(above) and from secondary reports of that post.
The examples and the two limits stated next to the test were written for this skill.

## Material that has no upstream source

- Contract 2 ("look the actor up, never pick one") and everything the skill says about a
  gap the source leaves open. They are this repository's "record, don't invent" applied
  to documentation.
- The six places where the actor hides and the two passives that stay, as lists. The
  individual observations are common to the sources above.
- The notes for Portuguese in `references/actors.md`.
- The entries for the README, the runbook, release notes, the pull request description,
  and the commit message in `references/documents.md`. They record common practice and
  cite no single source.
