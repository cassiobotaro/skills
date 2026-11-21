# Smoke test — unslop 1.0.0, 2026-11-21

Not an eval. Six headless sessions, one per case, on `claude-sonnet-5-5`
(`claude -p --setting-sources project,local --allowedTools Skill Read`), each in a scratch
project outside this repository with the skills under `.claude/skills/`. One run per case
measures no rate: it separates "works at all" from "does not".

## Can another skill call a skill that sets `disable-model-invocation: true`?

No. A caller skill told the model to apply a second skill that carried the flag. The Skill
tool answered:

> Skill zunslop cannot be used with Skill tool due to disable-model-invocation. Ask the
> user to run /zunslop themselves — it cannot be invoked via the Skill tool. Do not
> replicate this skill's workflow by other means — it is reserved for explicit user
> invocation.

So `unslop` ships without the flag and is explicit by its description.

## The shipped skill

The same Portuguese paragraph went into the first four cases. It carried an em-dash aside,
"não é apenas ... mas também", "Vale ressaltar que", "Especialistas afirmam que caches
reduzem custos", "muito mais rápido", inline code, and an "Em resumo" closing with a group
of three.

| Case | Prompt | Skill tool called `unslop` | What happened |
|---|---|---|---|
| Named | "passa o unslop nesse texto: ..." | yes | Read `references/pt-br.md`. Returned two sentences in Portuguese with the inline code intact, then listed three deleted claims by rule id (S6, PT1, S5/S12) and asked for the numbers and the source. |
| Not named | "melhora esse texto pra mim: ..." | no | The model rewrote the text unaided. |
| Not named | "revisa esse parágrafo e me diz o que acha: ..." | no | The model reviewed the text unaided and offered to run `unslop`. |
| Boundary | "esse texto tá com cara de IA, dá um jeito: ..." | no | The model rewrote the text unaided. |
| Called by a skill | a scratch skill that writes one paragraph, then says "when the `unslop` skill is installed, apply it" | yes | Read `references/en.md`. The paragraph kept the four facts of the prompt and changed "much faster" to "faster". |

Nothing was invented in the two runs that used the skill. The unaided rewrite of the second
case moved "reduz custos" from the experts to the service, which the original did not say.

Cost: US$ 0.27 for the six sessions, as reported by the CLI.
