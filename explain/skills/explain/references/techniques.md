# Explanation devices

One entry per device of the table in `SKILL.md`: how to build it, where it fails, and a
before/after pair. Every example was written for this skill to illustrate the device. The
facts in them are textbook-level.

Contents:

1. [Contrast: why X rather than Y](#1-contrast-why-x-rather-than-y)
2. [Refutation: name the wrong idea and replace it](#2-refutation-name-the-wrong-idea-and-replace-it)
3. [Mechanism and a prediction](#3-mechanism-and-a-prediction)
4. [Worked case, then the rule, then fading](#4-worked-case-then-the-rule-then-fading)
5. [Concrete, then roles, then the rule](#5-concrete-then-roles-then-the-rule)
6. [Minimal pairs](#6-minimal-pairs)
7. [Parts first, then the process](#7-parts-first-then-the-process)
8. [Analogy with a mapping and a limit](#8-analogy-with-a-mapping-and-a-limit)
9. [The same content for two readers](#9-the-same-content-for-two-readers)
10. [Layers for unknown or mixed readers](#10-layers-for-unknown-or-mixed-readers)
11. [A case with its typicality](#11-a-case-with-its-typicality)
12. [A simple version with its limit marked](#12-a-simple-version-with-its-limit-marked)
13. [The check the reader can fail](#13-the-check-the-reader-can-fail)
14. [Auditing a draft against the reader](#14-auditing-a-draft-against-the-reader)

## 1. Contrast: why X rather than Y

People who ask "why P?" are asking "why P and not Q?". Find Q in the question, the code
or the conversation, and answer the difference with the one or two causes that decide
it.

**Fails when** the contrast is guessed wrong. If two contrasts are plausible, name the
one you answered.

Question: "why does this query use LEFT JOIN?"

> **Before:** three paragraphs defining INNER, LEFT, RIGHT and FULL JOIN, with a table
> for each.
>
> **After:** "Because some customers have no orders yet. An INNER JOIN would drop them
> from the report; the LEFT JOIN keeps every customer and fills the order columns with
> NULL."

## 2. Refutation: name the wrong idea and replace it

Three parts, in the same passage: the wrong idea stated, the statement that it is wrong,
and the cause that replaces it. The replacement is what does the work. "That is a myth"
with no mechanism leaves a hole the old idea fills again.

Use it when the wrong idea is common among readers like this one, or when the question
rests on it. **Fails** on beliefs tied to identity, where some readers dig in, and it is
unknown whether naming a wrong idea plants it in a reader who never had it: do not
recite misconceptions the reader shows no sign of holding.

> **Before:** "Git stores a snapshot of every tracked file at each commit and
> deduplicates identical content by hash."
>
> **After:** "It is common to think that a commit stores the differences from the
> previous commit, and that Git replays them to rebuild a file. It does not: each commit
> points to a full snapshot of the project. A file that did not change is not copied
> again, because the snapshot points to the same stored content as before. That is why
> checking out an old commit is fast: Git reads one snapshot instead of replaying a
> history. (Git does compress similar contents together on disk, but that is a storage
> detail and not what a commit means.)"

## 3. Mechanism and a prediction

Knowing what a thing does and the names of its parts feels like knowing how it works.
Write the chain: what each part does to the next one, in order, with the fact that makes
the chain possible stated first. Close with a question about a case the text did not
cover.

**Fails when** the chain is fluent and wrong: the reader cannot tell. This is the device
where rule 2 of the contract matters most.

> **Before:** "A refrigerator has a compressor, a condenser, an expansion valve and an
> evaporator. The refrigerant circulates through them and removes heat from the inside."
>
> **After:** "A refrigerator moves heat from inside to outside using one fact: a liquid
> absorbs heat when it evaporates and gives heat back when it is compressed into a
> liquid again. (1) Inside, the cold fluid runs through a coil at low pressure and
> evaporates, pulling heat out of the compartment. (2) The compressor squeezes that gas,
> which makes it hot, hotter than the kitchen. (3) The hot gas runs through the coil at
> the back. Because it is hotter than the room, heat flows out to the kitchen and the gas
> becomes liquid again. (4) A narrow valve drops the pressure, the liquid cools, and the
> cycle starts over. To check the explanation: if you leave the door open in a closed
> room, does the room get colder?"
>
> (It gets warmer: the heat taken out in step 1 returns to the same room in step 3, plus
> the heat of the compressor.)

## 4. Worked case, then the rule, then fading

For a reader new to a procedure, one complete and correct case before the rule. Annotate
only the steps whose reason a newcomer could not infer. In the next turn, give a similar
case with the last step left to the reader (fading). "Find the mistake" exercises come
later, not first.

**Fails** with a reader who already knows the procedure, for whom the walkthrough is
noise, and the evidence comes from well-structured domains (algebra, physics,
programming). For writing or design, treat it as a reasonable guess.

> **Before:** "Rebase reapplies the commits of the current branch on top of another base
> commit, producing a linear history."
>
> **After:** "Your branch `feature` has commits C and D and started from A. Meanwhile
> `main` moved from A to B. `git rebase main` does three things in order: (1) sets C and
> D aside; (2) moves the start of `feature` to B; (3) reapplies C and then D on top of B,
> as new commits C' and D'. The history is now A, B, C', D'. That is the rule: rebase
> reapplies your commits on a new starting point, and the reapplied commits get new ids."
>
> **Next turn (fading):** "Same situation, but `feature` has three commits E, F and G,
> and `main` moved to H. Steps 1 and 2 are the same. What does the history look like
> after step 3?"

## 5. Concrete, then roles, then the rule

A concrete case helps when its surface carries the structure and hurts when the surface
is rich and unrelated. Three moves: the case, the same case with its parts renamed to
generic roles, the rule. The test for every sentence is whether the detail works for the
point.

> **Before:** "Hash functions were studied by Hans Peter Luhn at IBM in the 1950s, who
> also invented an early form of keyword indexing. A hash function maps data of
> arbitrary size to fixed-size values."
>
> **After:** "A coat check takes any coat, large or small, and hands back a small ticket
> with a number. Same coat, same number, and you cannot rebuild the coat from the ticket.
> Replace 'coat' with 'any data' and 'ticket' with 'a short number of fixed size': that
> is a hash function. In general terms: a function that takes inputs of any size to
> outputs of one fixed size, always the same output for the same input, and in practice
> not reversible."

The "before" is not wrong. Its first sentence is interesting and carries nothing, and
its second is a rule with no instance.

## 6. Minimal pairs

For a concept with a fuzzy edge, show examples and non-examples as alike as possible,
differing only in the trait that decides. Give the pairs first and name the trait after,
so the reader has seen the difference the rule explains. For a direct "what is X?",
answer in one line, then give the pairs.

**Fails when** the pairs differ in several traits at once: the reader cannot tell which
one matters.

> **Before:** "An operation is idempotent when applying it multiple times has the same
> effect as applying it once."
>
> **After:** "`PUT /users/7 {"name": "Ana"}` sent twice: user 7 is named Ana, same as
> after one request. Idempotent. `POST /users {"name": "Ana"}` sent twice: two users
> named Ana. Not idempotent. `DELETE /users/7` sent twice: the second request answers
> 404, but user 7 is gone either way. Idempotent. `x = 5` twice: idempotent. `x = x + 1`
> twice: not. What changes between the pairs is whether the second call leaves the system
> in a different state. The response may differ; the state may not."

## 7. Parts first, then the process

When the reader cannot name the parts, a process description overloads them: they are
learning the vocabulary and the sequence at once. Define the parts in a sentence each,
then run the process in numbered steps, and announce how many steps there are. Address
the reader as "you".

**Fails** with experienced readers and with simple material, where the scaffolding is
all cost, and with emphasis everywhere: a text where everything is highlighted has no
signal.

> **Before:** "Upon issuing a query, the stub resolver forwards it to the recursive
> resolver, which, absent a cached record, iteratively queries the root, TLD and
> authoritative servers, subsequently caching the answer in accordance with the TTL."
>
> **After:** "Three names first. A *resolver* is the server that does the lookup for
> you. An *authoritative server* is the one that actually holds the answer for a domain.
> The *TTL* is how long an answer may be reused. Now the lookup, in three steps. 1. Your
> computer asks the resolver: 'what is the address of example.com?'. 2. If the resolver
> has a recent answer stored, it replies at once. If not, it asks its way down: a root
> server points to the servers for `.com`, which point to the authoritative server for
> example.com, which gives the address. 3. The resolver stores the answer for the TTL
> and returns it to you. This is why a DNS change takes time to show up: resolvers keep
> serving the stored answer until the TTL runs out."

## 8. Analogy with a mapping and a limit

An analogy is the device most likely to leave a wrong idea behind, and machine-written
analogies raise the reader's confidence without raising their accuracy. Conditions for
using one:

- The reader has nothing close to the concept, and a direct statement plus an example
  did not do the job.
- The source is something this reader knows. Their own domain beats a generic one.
- It covers one aspect. Do not stretch it over every feature of the concept.
- The correspondences are written out, not left for the reader to find.
- The text says where the analogy stops working.

A second analogy is justified only when the break of the first one would mislead about
something the reader needs. The two should fail at different points.

> **Before:** "Electricity is like water flowing in pipes."
>
> **After:** "Think of water in a closed loop of pipes. The pressure from the pump is the
> voltage, the amount of water passing a point each second is the current, and a narrow
> stretch of pipe is a resistor. Where the comparison breaks: cut a pipe and the water
> leaks out; cut a wire and the current simply stops. A bicycle chain covers that gap:
> push one link and every link moves at once, and if the chain is broken nothing moves
> anywhere. Both pictures agree on the principle: current flows only in a complete
> circuit, driven by a push (voltage) against an opposition (resistance)."

## 9. The same content for two readers

What changes between levels is what is presumed, defined and omitted. The experienced
version below is shorter, but only because it presumes more.

> **For nobody in particular:** "An index is a data structure, typically a B-tree, that
> the planner can use to avoid sequential scans, at the cost of write amplification."
>
> **New to databases:** "Without an index, the database finds your row the way you would
> find a name in an unsorted list: by reading line after line. An index is a separate,
> sorted list that says 'Silva: row 212', so the database goes straight there. The price:
> every time a row is inserted or changed, the index has to be updated too, and writes
> get a little slower."
>
> **Experienced developer:** "A secondary B-tree on the column, pointing to row
> locations. The planner uses it when selectivity beats a sequential scan. Cost: one more
> tree update per write, per index, plus storage."

A reader who says "I'm a physics grad student" and asks why the sky is blue does not want
the children's version with harder words. They want the dependence on wavelength and the
reason violet does not win.

## 10. Layers for unknown or mixed readers

When the text will be read by people at different levels (a doc, a post, an
announcement), write the one-paragraph version first, complete in itself, then deeper
layers, each one labeled by what it presumes ("if you have used SQL", "for people who
operate the cluster"). In a conversation, give the first layer and offer the next.

Do not produce several levels in parallel for one identified reader: the other levels
are noise. And do not trust yourself to hit a named level without a check against the
reader (entry 14).

## 11. A case with its typicality

A sequence with an agent and explicit causes is remembered better than a statement. The
usable part of narrative is that structure, not fiction or suspense. The risk is that
one case counts as many in the reader's mind, so say how typical it is right after.

**Fails** for taxonomies, reference material and procedures, and with a reader in a
hurry.

> **Before:** "Antibiotic resistance arises from selective pressure favoring resistant
> strains under subtherapeutic exposure."
>
> **After:** "Suppose you stop the antibiotic on day three because you feel fine. The
> weakest bacteria are already dead; the toughest are still alive. With the drug gone,
> those survivors multiply, and the next infection is harder to treat. This does not
> happen every time someone stops early, but each shortened treatment gives resistant
> bacteria one more chance."

A one-line test of whether an explanation has a point, borrowed from screenwriting: can
it be said as "A and B, but C, therefore D"? If it only works as "A and B and C", it is a
list of facts.

## 12. A simple version with its limit marked

Simplify the wording freely. When the simplification removes something true (a matter of
degree, a condition, an exception), say in one clause what was left out and when it
matters. A brief qualifier helps; a long methodological aside costs more than it gives.

> **Before (simple, categorical, closed):** "A vaccine shows your body a harmless copy
> of the germ so it learns to fight it. After that, you are immune."
>
> **After (simple, limit marked):** "A vaccine shows your immune system a harmless piece
> or copy of the germ. Your body trains on it and keeps a memory of what the germ looks
> like, so if the real one arrives the response is much faster. That is the simple
> version, and it leaves out two things that matter in practice. Protection is a matter
> of degree, not an on/off switch. And the memory can fade or the germ can change, which
> is why some vaccines need boosters."

> **Before (the claim grew as the text shrank):** "Standing desks prevent back pain,
> study says."
>
> **After (short, scope kept):** "In a study that followed office workers for two years,
> those who used standing desks reported less back pain. The study does not show that
> the desk is the cause: the two groups may differ in other ways."

Sometimes no simple version is faithful. Then the honest answer is to say so and give the
nearest true statement, with what it does not cover.

## 13. The check the reader can fail

A question the reader can only answer by using the idea: predict a new case, apply the
rule to their own situation, say what must be true before a step. Frame it as a check on
the explanation. One question, after the hard part, not after every paragraph.

> **Before:** "The migration involves steps A, B and C described above. Let me know if
> anything is unclear."
>
> **After:** "One check on my explanation: at 3 a.m. the queue length keeps growing, but
> the API logs no errors. Which component would you look at first, and why?"

## 14. Auditing a draft against the reader

Being warned about the curse of knowledge does not reduce it. Mechanical checks against
the stated reader do more:

- **Terms the reader did not use.** List every technical term in the draft that is absent
  from the reader's own messages. Each one is defined, replaced, or kept on purpose.
- **Steps that felt obvious.** Between each pair of consecutive sentences, is there a
  step you skipped because you make it without noticing?
- **Abstractions without an instance.** Every general statement has a case next to it.
- **Where the plain version stalls.** Say the explanation with no jargon at all. The
  place where you reach for a term because you cannot say what it stands for is a gap in
  your own understanding. Go back to the source for that part.

Reader: started with containers this week and asked why the Docker image is so large.

> **Before:** "You are not using a multi-stage build, so the build dependencies stay in
> the final layer. Use a slim base and copy the artifact from the builder stage."
>
> **After:** "An image is assembled in steps, and the files from every step stay in the
> image. Your steps install the compiler and the tools needed to *build* the program, and
> all of that is still there, although it is needed only once. Two changes fix it. First,
> split the Dockerfile in two parts: one that builds the program, and a new, clean one
> that copies only the finished program (Docker calls this a multi-stage build). Second,
> start that second part from a small base image, one that has only what the operating
> system needs to run the program."
