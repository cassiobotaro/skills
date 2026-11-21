---
name: unslop
license: MIT
description: >
  Edit prose to remove the patterns that mark a text as machine-written, in English or
  Brazilian Portuguese, without changing its meaning and without adding a fact. Explicit only.
  Use this skill when the user asks for it by name ("unslop this", "/unslop", "run unslop on
  the README", "passa o unslop nesse texto"), or when another skill tells you to apply it to
  prose that skill produced. Do not use it for a general request to write, review, improve,
  shorten, translate, or proofread a text.
---

# Unslop

Edit prose to remove the patterns a reader recognises as machine-written. The meaning, the
facts, the tone, and the language of the text stay as they are.

## The contract

1. **Remove, never supply.** An edit cuts or rewords. It never adds a fact, a number, a
   source, an example, or a reason that the text did not contain. When a rule asks for
   something the text lacks (the source behind "studies show", the number behind "much
   faster"), delete the claim or ask the user for the missing fact. When another skill
   called you, a gap goes where that skill puts its open questions.
2. **Edit prose only.** Leave these unchanged: code blocks and inline code, diagram and DSL
   source, commands, paths, identifiers, URLs, quotations, and every heading, label, or
   keyword that a tool parses. When another skill called you, the text that skill treats as
   fixed stays fixed, such as the headings of a template.
3. **Keep the language.** Edit in the language of the text. Never translate, and keep the
   spelling variant the text already uses.
4. **Edit only what was asked.** That is the text, file, or section the user named, or the
   prose the calling skill wrote in this turn. A file that records history, such as an
   accepted decision record or a published changelog entry, is out of reach unless the user
   names it.

## Procedure

1. Read the whole text before changing anything.
2. Read the vocabulary file for the language of the text: `references/en.md` for English,
   `references/pt-br.md` for Brazilian Portuguese. For any other language, apply only the
   rules below and tell the user that no vocabulary list exists for that language.
3. Rewrite each hit. When a rule makes a sentence worse, fix the sentence another way or
   leave it alone.
4. Compare the result with the original, one claim at a time. Every fact is still there
   and none is new.

## Rules

Rule ids are stable so that other skills can cite them. A removed rule leaves a gap. The
vocabulary files continue the list with their own prefixes.

- **S1.** No em dash, en dash, or spaced hyphen as a sentence connector. Use a period or a
  comma. A dash in a number range, a compound word, or Portuguese dialogue is not a
  connector.
- **S2.** A colon introduces a list, an example, or a quotation. It does not set up a
  reveal ("The central trade-off: users lose the download"). Write the sentence.
- **S3.** No "not just X, but Y" and no "it is not X, it is Y" when nobody claimed X.
  State Y.
- **S4.** No forced group of three. List what there is.
- **S5.** No trailing participle phrase that adds no fact ("..., ensuring reliability",
  "..., garantindo a confiabilidade").
- **S6.** No vague attribution ("experts believe", "studies show"). Contract 1 applies.
- **S7.** One name per thing. Repeat the name instead of rotating synonyms.
- **S8.** No "from X to Y" unless X and Y are the two ends of a real scale.
- **S9.** Bold marks a term at its definition or a UI label. No bold for emphasis on a
  word, on every proper noun, or on a label that restates its own line.
- **S10.** A heading says what its section holds, in the capitalisation the document
  already uses, and in sentence case when the document has none.
- **S11.** No decorative emoji.
- **S12.** No opening that lists what the text is about to cover, and no closing that
  repeats what the text already said.
- **S13.** No chatbot address to the reader: praise, an agreement opener, an offer of more
  help.
- **S14.** One hedge per claim at most. When the text is sure, state the claim. When it is
  not, say what is unknown.
- **S15.** Cut a sentence that could appear unchanged in a text about a different subject.
- **S16.** One idea per sentence. Split a sentence that the reader has to reread.
- **S17.** Active voice with the actor named, unless the actor is unknown or does not
  matter. When the text never says who the actor is, contract 1 applies.
- **S18.** Cut intensifiers and vague adverbs ("very", "significantly", "extremamente").
  Keep the number when the text has one.
- **S19.** Literal wording where a literal phrase exists. No metaphor, aphorism, or
  software described as if it had intentions.
- **S20.** Whole sentences, with their articles and verbs. In prose, spell out arrows,
  symbols, and abbreviations the text never defined.
- **S21.** No sentence shape that repeats across consecutive paragraphs or sections, such
  as the same opener in each one.

## Deliver

- **Text pasted in the conversation.** Reply with the edited text and nothing around it.
- **A file.** Edit it in place and report its path.
- **Called by another skill.** Edit the prose before that skill's own final check, and
  add no report of your own.

In the first two cases, add a short list after the result only when contract 1 made you
delete a claim or ask a question. Name each deleted claim and each question. When the
text needed no edit, say so and return it unchanged.

## Attribution

The rule catalog is adapted from the `unslop` skill of
[pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan, licensed MIT.
See `NOTICE.md`.
