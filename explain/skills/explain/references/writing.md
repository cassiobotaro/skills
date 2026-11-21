# Writing for someone else

Before/after pairs for the steps of section 5 of `SKILL.md`, then the ordering formats,
replies, and bad news. Every example was written for this skill, and the names, dates and
numbers in them are made up.

Contents:

1. [The request first](#1-the-request-first)
2. [Jargon](#2-jargon)
3. [Un-nesting](#3-un-nesting)
4. [Subtracting](#4-subtracting)
5. [Intent said literally](#5-intent-said-literally)
6. [Structure only where there are parts](#6-structure-only-where-there-are-parts)
7. [Numbers](#7-numbers)
8. [Ordering formats](#8-ordering-formats)
9. [Replying to a question](#9-replying-to-a-question)
10. [Bad news and refusals](#10-bad-news-and-refusals)

## 1. The request first

Readers of practical text scan before they read. The request or the answer goes where
the scan lands: the opening. Context comes after, for whoever wants to check it.

> **Before:** "Hi Bruno. As you know, we have been reworking the billing module since
> last sprint, and a few things came up with the rounding of installments, which behaved
> differently in staging... [three paragraphs] ...so I wanted to know if you could take a
> look at the pull request before Thursday."
>
> **After:** "Hi Bruno. Can you review pull request 412 by Wednesday, March 4? The
> release branch is cut on Thursday, and this change fixes the rounding of installments
> that would otherwise ship wrong. What to look at is below."

The exception: when the conclusion cannot be understood without one fact, that fact
comes first, in one sentence. "Problem, then answer" beats "answer" alone when the answer
alone is unintelligible.

## 2. Jargon

Replace the term with common words. A definition placed elsewhere (footnote, glossary,
tooltip) improves how accessible the text looks and not what the reader learns.

> **Before (definition parked):** "Version 3 goes out as a canary* on Monday. (*A
> release exposed to a small share of traffic before the full rollout.)"
>
> **After (term replaced):** "On Monday we release version 3 to 5% of users. If the error
> rate holds for a day, everyone gets it on Tuesday."

When the reader will need the term afterwards, give the idea first and the name after,
once:

> "On Monday we release version 3 to 5% of users (the dashboard calls this the canary).
> If the canary's error rate holds for a day, everyone gets the version on Tuesday."

Jargon is relative to the reader. Do not replace a term the recipient works with: for
them a paraphrase is longer and vaguer. Replacing every technical word with a
circumlocution ("food-heating radio box" for microwave) is harder to read than one
defined term.

## 3. Un-nesting

The structure that hurts most is a clause wedged in the middle of another. Find the main
clause, write it whole, and give each condition its own sentence.

> **Before:** "The tenant who, having paid the deposit, except where the lease provides
> otherwise, vacates the unit before the end of the term shall forfeit the deposit."
>
> **After:** "If you leave the unit before the lease ends, you lose the deposit. The
> lease may list exceptions to this."

The same in Portuguese, where legal and administrative prose nests the same way:

> **Antes:** "O condômino que, estando em dia com as taxas condominiais, salvo nos casos
> previstos no regimento interno, reservar o salão de festas com menos de 7 dias de
> antecedência, pagará a taxa adicional."
>
> **Depois:** "Se você reservar o salão de festas com menos de 7 dias de antecedência,
> paga uma taxa adicional. Para reservar, é preciso estar em dia com as taxas do
> condomínio. O regimento interno prevê algumas exceções."

Short sentences are not the goal. Editing toward a readability score removes the
connectives that carry the reasoning:

> **Worse, edited for the score:** "The backup can fail. Check the log. Look for
> 'timeout'. Run it again."
>
> **Better, edited for the reader:** "Check the log after the backup, because it can fail
> without showing an error on screen. If the log says 'timeout', run the backup again."

Use the active voice when the reader needs to know who does what. As a blanket rule it
has mixed support, and there is no evidence for a fixed word limit per sentence.

## 4. Subtracting

Ask of each sentence: can the reader act without it? Template openers and closers go
first ("I hope this message finds you well", "please do not hesitate to contact me").
Keep the request itself intact, and keep the context the reader needs to say yes.

> **Before:** "I hope this message finds you well. My name is Rafael and I maintain an
> open source library for parsing bank statements, which I started in 2019 after years
> of frustration with the existing tools. I have long admired the work your team does...
> Would you be open to letting us use your sample files in our test suite?"
>
> **After:** "I maintain an open source library that parses bank statements. May we use
> the sample files from your repository in our test suite? We would credit your project
> in the README. Thank you."

The evidence for shortening comes from first-contact and low-stakes messages. It does not
say where shortening starts to hurt, so do not cut context the reader needs in order to
decide.

## 5. Intent said literally

> **Before (tone carries the message):** "Great, another last-minute change. Love it."
>
> **After:** "This change arrived after the deadline, so I cannot include it in Friday's
> delivery. I can deliver it on the 21st. Does that work for you?"

The same holds for urgency ("ASAP" is read as anything from an hour to a week: write the
date) and for softening ("it would be nice if" is read as optional: write what is
required).

## 6. Structure only where there are parts

Headings and previews help the reader recall the main ideas and cost some recall of
detail, and they help only when the content has a structure to show. A message with one
point gets a paragraph.

- A sequence the reader will follow: numbered steps.
- Options to compare: one line per option, the same attributes in the same order.
- Content the reader returns to: headings that say what the section holds.
- An argument: prose. Bullets drop the "because" and the "so".

## 7. Numbers

**A risk: absolute figures with the baseline.**

> **Before:** "The new firmware cuts drive failures by 50%."
>
> **After:** "With the old firmware, about 4 drives in 1,000 fail in a year. With the new
> one, about 2 in 1,000."

When the baseline is not known, do not invent one. Say that a relative figure cannot be
judged without it, and show with an explicitly hypothetical baseline why.

**A conditional probability: counts out of one group.**

> **Before:** "The condition affects 2% of people. The test detects it 90% of the time
> and gives a false positive 5% of the time."
>
> **After:** "Out of 1,000 people tested, 20 have the condition, and 18 of them test
> positive. Of the 980 who do not have it, 49 also test positive. So of 67 positive
> results, 18 are real."

**An uncertain estimate: the number and its range.**

> **Before:** "The migration should take a while, but it is hard to say and it could be
> different."
>
> **After:** "The migration should take about 6 hours (between 4 and 9, depending on how
> long the index rebuild runs)."

## 8. Ordering formats

These are conventions from practice. None was shown to beat another, so choose by the
reader's situation. The example is one scenario, a database migration.

| Format | Fits | Shape |
|---|---|---|
| Answer first (BLUF) | A busy reader who has to decide and would understand the full answer | "I am asking you to approve the database switch: hosting drops by about R$ 4,000 a month from August and it takes one weekend of downtime, July 12 and 13. The technical reasons are below." |
| Context, then answer | The answer is unintelligible without one fact | "Our hosting contract ends in August and the renewal costs more. I am asking you to approve switching databases before that." |
| Inverted pyramid | News or a changelog the reader may leave at any point | "The switch was completed on Sunday with no data loss. The system was down from 10 p.m. Saturday to 6 a.m. Savings start in August. [Cuttable context after this.]" |
| Situation, complication, question, answer | A recommendation with several supporting reasons | "We have used the current database from the start. Hosting got more expensive and the contract ends in August. Renew or switch? Switch, because (1) it costs R$ 4,000 less a month, (2) the migration fits in a weekend, (3) the team already runs the new database in another product." |
| Problem, then solution | A thing whose purpose is not clear to the reader | "Every report reads the whole table and takes minutes. An index on the date column takes the database straight to the rows of the period." |
| Compare and contrast | A choice between options | "Queue or direct call. Reply to the user: immediate, or only when processing ends. If the worker dies: requests wait, or the request fails. Cost: one more component to operate, or none." |
| What happened, so what, now what | An incident report | "The migration took three hours longer than planned. The system came back at 9 a.m. and support received tickets. Next time we rehearse the copy with real volume." |

Answer-first formats presume a reader who would understand the conclusion. For a reader
new to the subject, build up to it.

## 9. Replying to a question

- Answer what was asked, first, in the terms the person used.
- When the message has several questions, answer each one, in their order. An
  unanswered question is the most common reason for a second round.
- When you cannot answer one, say that, and say who can or when you will know. Do not
  commit the user to something they did not say they would do (rule 2 of the contract).
- Match the register of the thread. A two-line question does not get a memo.

> **Message received:** "Can you reissue the March invoice with our new address? And does
> the due date change?"
>
> **Before:** "Thanks for reaching out! We are always happy to help our customers keep
> their records up to date. Our billing team handles a large number of requests..."
>
> **After:** "Yes. I will send the reissued March invoice with the new address tomorrow,
> [date?]. On the due date: I do not decide that, so I have asked the billing team and
> will tell you what they say."

## 10. Bad news and refusals

Say it in the first or second sentence, in plain words. Then the reason, in one sentence
the reader can verify. Then what you can do instead. Padding before the news makes the
reader search for it and trust the rest less.

> **Before:** "We really appreciate your interest and the time you invested in the
> proposal. After careful consideration of many factors, and given the current
> circumstances, we find ourselves in a position where..."
>
> **After:** "We are not going ahead with the proposal this quarter. The budget for
> external tools is already committed through March. If it helps, I can bring it back to
> the planning meeting in February."
