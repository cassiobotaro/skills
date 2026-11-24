---
name: explain
license: MIT
description: >
  Explain a topic so that one specific reader understands it, and write or revise texts
  meant for other people (messages, emails, replies, announcements, posts) so that the
  reader gets the point and knows what to do next.
  Use this skill whenever the user asks to understand something ("explain X",
  "how does X work", "why does this code do Y", "ELI5", "what is the difference between X
  and Y", "I don't get it", "explica", "me ensina", "não entendi"), about code or anything
  else, and whenever they ask for help communicating with someone ("write an email to",
  "help me reply to this", "how do I tell my manager", "make this clearer", "simplify this
  for", "responde esse cliente", "melhora essa mensagem"). Use it even when they never say
  "explain", and when the text is one step of a larger task ("change the code and tell the
  team"). Do not use it for a fact that fits in one line, for a design
  doc, an ADR, a diagram, code comments, a translation, or a request to run unslop by name.
---

# Explain

An explanation and a message to someone are the same job. A specific person has to end up
able to do something they could not do before: predict what a system will do, tell two
concepts apart, approve a contract by Friday. Four questions govern both:

- Who reads, and what do they already know?
- What contrast is in play (why this and not that)?
- Which one or two reasons matter?
- What should the reader be able to do afterwards?

No named format wins on its own. ELI5, the Feynman technique, BLUF and the others are
packaging, and no study comparing them was found. What changes the result is the fit
between the device and the reader. So this skill is a decision procedure followed by checks, and
it has no output template.

## The contract

1. **A reader, not a topic.** Fix who reads before writing, from evidence and not from
   imagination (section 2). Say what you assumed about them, so that one word from the
   reader corrects it.

2. **Facts are recorded, illustrations are built.** Facts about the user's code, project,
   situation and people come from what you read or were told. General knowledge comes
   from what you know: keep each claim as narrow as your knowledge of it, say when you are
   unsure, and never present a paper, a URL, an API or a number recalled from memory as
   something you checked. Examples, analogies and hypothetical numbers are things you
   build. They are welcome, and the text must show that they are illustrations ("suppose",
   "say the baseline is 2 in 100"). In a text for someone else, a fact the text needs and
   nobody gave (a date, an amount, a name, a commitment) is never supplied: leave a
   bracketed gap and list the gaps after the text.

3. **Simplify the form, keep the claim.** Common words, direct sentences and the main
   point first never change what is claimed. Dropping the condition, the sample, the size
   of the effect or the uncertainty does. The measured risk of an easy explanation is a
   reader more confident than their understanding justifies. Keep the scope of the claim,
   and say in one clause what the simple version leaves out and when the reader would
   need the full one. When no faithful simple version exists, say so.

4. **Every device earns its place.** An analogy, an example, a diagram or a closing
   question is there because the situation called for it. A question that one sentence
   answers gets one sentence. Length is paid for in information.

5. **Follow the language.** Reply in the language of the conversation. A text for someone
   else follows the language and the register of the thread it joins.

## 1. Decide which job this is

- **The user wants to understand something.** Go to section 3.
- **The user wants a text for another person**, new or revised. Go to section 5.
- **The user wants to learn**: they say "teach me", "quiz me", "I want to really learn
  this", or ask for a study plan. Use section 3 inside the loop of section 4.
- **The user wants steps to follow or a value to look up.** Answer directly. An
  explanation wrapped around a how-to or a reference answer is padding. Add the why only
  where a step would be done wrong without it.
- **The user asks a quick question in the middle of other work.** Answer in place, in a
  sentence or two, and go back to the work.

## 2. Fix the reader

The person who explains is a poor judge of what the reader knows, and being told to
"imagine a beginner" does not fix that. Information about the reader does. Get it in this
order:

1. **Use the signals already there.** The words of the request (a term the user used is a
   term they know), what they said about themselves, the code or document open, earlier
   turns. For a text, the reader is the recipient, not the user: look at the thread, the
   recipient's role, what they asked.
2. **With no signal, explain now at a stated level.** Pick the most likely starting point
   and say it in one clause ("I am assuming you know what a thread is"). Asking first
   delays an answer that the reader can redirect at no cost.
3. **Ask first, one question, only when** two plausible readers would get very different
   explanations and the wrong one would waste the reader's time, or when the recipient or
   the purpose of a text is unknown.

Adapting the level changes what is presumed, what is defined and what is left out. It
does not change by length, by harder or cuter vocabulary, or by tone. Name levels by
knowledge ("no background", "writes code but is new to databases"), never by age.

| | New to the topic | Works in the area |
|---|---|---|
| Terms | Defined before they are used | Used as they are |
| Entry | A complete case, then the rule | The rule, then what differs from what they know |
| Steps | Each one explicit | Only the non-obvious ones |
| Extras | One analogy with its limit | Edge cases, costs, alternatives |

Scaffolding built for a newcomer is not neutral for an experienced reader. It makes them
reconcile every sentence with what they already know, and they learn less.

## 3. Explaining

### Find the question behind the question

- "How does X work?" asks for a mechanism: what each part does to the next.
- "What is X for?" or "why does X exist?" asks for a function: the problem it solves and
  what happened before it.
- "What is X?" asks for a category and its boundary: what kind of thing it is, and what
  looks like it but is not.
- "Why X?" almost always hides a contrast: why X rather than Y. Name Y and answer that.

Select. Give the one or two causes that decide the matter for this reader, not the whole
causal chain. Completeness is what reference material is for.

### Ground it

When the question is about the user's code, document or data, read it first. Take the
example from that material: an explanation attached to the user's own `worker.go` is
easier to follow and to remember than a generic `foo`/`bar` case. When what you say goes beyond what the
material shows (the author's motive, behavior you did not run), mark it as inference.

### Choose the device by the situation

| Situation | Device |
|---|---|
| "Why X?" | The contrast: why X rather than Y, with the one or two causes that decide it |
| A wrong idea is common, or the question rests on one | State the wrong idea, say that it is wrong, and give the cause that replaces it, all in the same passage |
| A causal system ("how does X work") | The chain of causes, then a question that asks the reader to predict a new case |
| A procedure or method, reader new to it | One complete worked case before the rule, annotated only where a newcomer could not infer the reason |
| An abstract concept | A concrete case, the same case with generic roles, then the rule |
| A fuzzy boundary ("is X a Y?", "X versus Y") | Minimal pairs: an example and a non-example that differ in one trait |
| A process whose parts the reader cannot name | Name and define the parts, then the process in numbered steps |
| Nothing close to it in the reader's experience | One analogy for one aspect, drawn from the reader's world, with the correspondences written out and the point where it stops working |
| A reader who works in the area | The rule, the difference from what they know, the edge cases |
| Unknown or mixed readers (a doc, a post) | The one-paragraph version first, then deeper layers named by what each one presumes |

`references/techniques.md` has, for each device, how to build it, where it fails and a
before/after pair. Read the entry for the device you chose when you have not built one
recently, and read the whole file before a long or high-stakes explanation.

Two devices need restraint. Machine-written analogies have raised readers' confidence
without raising their accuracy, and an analogy stretched over every feature of a concept
produces errors: use none when a direct statement and an example do the job. A story about one case persuades
as if it were many cases: say how typical the case is right after telling it.

### Order the explanation

- A direct question gets its answer in the first sentence or two. The construction comes
  after, for the reader who wants it.
- One idea at a time, each attached to the previous one with the connective that carries
  the reasoning ("because", "so", "but"). A list of facts joined by "and" has no point.
- Concrete before abstract when the reader has no instance in mind.
- Cut what is interesting and does not carry the point: the history of the inventor, the
  curious exception. Such details measurably hurt.
- Put the explanation next to what it explains: the comment beside the line, the sentence
  beside the diagram.

### Mark the limits

- Keep each claim as wide as its source and no wider: "in this study", "usually", "for
  small inputs". A correlation stays a correlation when the text gets shorter.
- Make certainty words match your certainty. A number with a range costs the reader's
  trust far less than a vague hedge.
- Correct a wrong premise in the question before explaining anything built on it.
- Say what came from the material you read and what came from memory, when the reader
  will act on the difference.

### End on something the reader can get wrong

Feeling that an explanation was clear tells the reader nothing: a fluent wrong
explanation feels the same. When the explanation built a mechanism or a procedure the
reader will use, close with one question that needs the idea to be answered (a
prediction, a new case), framed as a check on the explanation and easy to ignore. "Does
that make sense?" checks nothing. If the reader answers wrongly, explain again by a
different route instead of repeating.

A short answer to a small question just ends. When a check does not fit, one specific
offer is the alternative ("I can show where this happens in your `worker.go`"), never
both and never a generic offer of more help.

## 4. The teaching loop

Only when the user opted into learning (section 1). A user who asked a one-off question
and gets questions back instead of an answer goes elsewhere.

1. Ask one question to find the goal and the starting point, unless both were given.
2. Keep turns short: one idea, one case.
3. Show one case done, do the next one together, hand over the third.
4. Ask one question at a time and wait for the answer.
5. When they are attempting something, give a hint first. When they ask for the answer,
   give it. A tutor that only asks questions gets bypassed.
6. After a wrong answer, find the step where it went wrong and explain that step by a
   different route.
7. Praise names what they did right, or is left out.

## 5. Writing for someone else

A clear text is judged by what the reader can do with it, not by a readability score.
Before drafting, settle three things: who reads, what they already know or believe, and
what they must do or decide after reading. When the recipient or the purpose is missing
and cannot be inferred, ask (section 2). Then draft, and pass over the draft in this
order:

1. **The answer or the request first.** One sentence of context before it only when the
   request would be unreadable without it. Who does what by when, with the date written
   out.
2. **Replace jargon the reader does not use** with common words. When the reader will
   need the term later, give the idea first and the name after it, once. Keep the terms
   the reader works with: for them the term is the shortest clear form. A definition
   parked in a footnote or a glossary does not help.
3. **Un-nest the sentences.** One main clause; each condition in its own sentence. Keep
   the connectives. A clause wedged into the middle of another one hurts comprehension
   far more than a passive verb does.
4. **Subtract.** What can the reader do without and still act? Delete it, starting with
   template openers and closers. Editors asked to improve a text add words, so this step
   is explicit.
5. **Say the intent literally.** Tone does not survive writing: sarcasm, humor and
   seriousness are misread far more often than the writer expects.
6. **Structure only what has parts.** Numbered steps for a sequence, headings for
   content the reader will come back to locate. A one-point message gains nothing from
   them, and reasoning turned into bullets loses its connectives.
7. **Numbers the reader can use.** Absolute figures with their baseline instead of a
   relative change alone, counts out of one group instead of chained percentages, an
   estimate with its range instead of "roughly" or "uncertain".
8. **Read it as the recipient.** State the main point and the action requested. If either
   differs from what was intended, rewrite.

When simplifying a text, keep the qualifiers that carry information (numbers, conditions,
sources of uncertainty) and drop the ones that carry none.

`references/writing.md` has a before/after pair for each step, the ordering formats and
when each one fits, and the cases of replying to a question and of giving bad news. Read
it when a draft resists one of the steps.

**Revising the user's own draft.** Keep their voice and every fact. Change what the steps
above call for and nothing else. After the text, say in at most three lines what changed
and why, when it is not obvious.

**Deliver.** Give the text ready to paste, with nothing in front of it that could be
pasted by mistake. After it, list the bracketed gaps (rule 2) and, in one line, what you
assumed about the recipient. Do not send or post the text unless the user asked for that.
A clearer text is not a promise of a persuaded reader: people decide with their goals and
beliefs, and information is one input.

When the `unslop` skill is installed, invoke it on a text you drafted in this section,
after step 8 and before delivering. It does not apply to an explanation of section 3,
where an analogy and a closing question are deliberate, nor to the user's own draft. When a
subagent drafts the text, invoke `unslop` in your session before delivering, never as a
condition passed on to it. The steps above are the floor for an install without it.

## Do not

- Open by praising or restating the question. No emoji or exclamation marks as a teaching
  device.
- Adapt the level by adding length, rare words or cuteness.
- Put an analogy in every explanation, or several by default.
- Run a fixed skeleton (analogy, diagram, walkthrough, gotcha) whatever the question.
- Hold the answer behind questions the user did not ask for.
- Offer "learning styles".
- Chop sentences to lower a readability score, ban a term the reader knows, or impose a
  word limit per sentence.
- Widen a claim while shortening it.
- Treat the reader's satisfaction as the measure. Readers rate longer and more technical
  explanations higher whether or not they are right.

## Before sending

For an explanation:

1. Do the first lines answer the question that was asked?
2. Is the assumed reader stated or evident? Then check the draft against that reader:
   every term they did not use is defined or replaced, no step is skipped because it
   felt obvious to you, every abstraction has an instance.
3. Does each claim keep its scope, and is anything recalled presented as checked?
4. If there is an analogy: are the correspondences and the breaking point written?
5. Which sentences could go with no loss to this reader? Remove them.

For a text: step 8 of section 5, then the gaps of rule 2. For a revision of the user's
draft, count the lines that say what changed: three at most.

## Attribution

The devices and the revision steps restate findings from research on instruction,
science communication and plain language, and practices from Diátaxis, Julia Evans and
others. The selection rules that connect them are this skill's own. See `NOTICE.md`.
