# Notices and attribution

This skill contains material adapted from a third-party source. Changes were made
throughout (rewording, reorganization, added guidance).

## pstack — Lauren Tan

The idea of one skill that owns a numbered catalog of machine-writing patterns, which
other skills apply by name, and most of the patterns in that catalog are adapted from the
`unslop` skill of **pstack** by **Lauren Tan**, version 0.15.46:
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

- The rules are renumbered. The rules that hold in any language are `S1` to `S21` in
  `SKILL.md`, and the word lists are in one file per language under `references/`.
- A rule that asked the editor to supply something ("name the source", "give the number")
  now deletes the claim or asks the user, because this repository's skills never add a
  fact the user did not give.
- The skill names what it never edits: code, diagram source, quotations, text a tool
  parses, and files that record history.
- pstack bans parentheses in place of a dash and requires straight quotes. This skill has
  neither rule.

## Material that is not from pstack

- Rules S2, S12 and S21 restate the typography guidance of this repository's `design-doc`
  skill.
- `references/pt-br.md` was written for this skill. It has no upstream source.
