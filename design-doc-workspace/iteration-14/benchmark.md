# iteration-14 — eval 4 against 1.3.3, closing the prose half of the never-invent leak

**Why this run exists.** Iteration-13 verified 1.3.2's diagram fix on evals 1 and 3 but left
eval 4 unmeasured, and eval 4 carried a second, different failure. Running it produced the
useful result: the fix was **partial**.

## The three-version trace on one eval

| Version | Score | Mode (a): invented tech in a diagram | Mode (b): prose exclusivity |
|---|---|---|---|
| 1.3.1 (it-12) | 8/9 | `"HTTPS"` on a DSL relationship | "o Redis … é a **única** infraestrutura de contadores rápidos" |
| 1.3.2 (it-13) | 8/9 | **closed** | **recurred, reworded** — "o **único** freio disponível durante o incidente foi a intervenção manual" |
| 1.3.3 (it-14) | **9/9** | closed | **closed** |

1.3.2 targeted the notation, so mode (a) stopped. Mode (b) had nothing aimed at it and simply
found new words — which is the strongest evidence in this whole sweep that the two are
different failures and that fixing one does not fix the other. 1.3.3 adds the missing rule:
invention also arrives as *inference*, and exclusivity superlatives are the shape an unstated
absence takes when written down as fact.

The reasoning the rule now carries: "there is no per-client limit today" does not license
"manual intervention was the only brake". A global throttle, a WAF rule, or the client fixing
its own integration are all equally unmentioned — you cannot rule out what was never
discussed.

## What the grader established

- **Exclusivity sweep** (`unic|únic|sempre|nunca|apenas|somente|todo|toda`) returned 6 hits,
  each adjudicated individually; all are restatements. `"por causa de um único integrador"`
  counts the single cause the user gave ("um cliente com integração mal feita … derrubou a
  API pra todo mundo") — it does not infer that no other mitigation existed, which is exactly
  what the 1.3.1 and 1.3.2 sentences did. The distinction the rule needs the model to make is
  being made.
- **Mode (a) has no opportunity to recur here**: this run produced only a Mermaid sequence
  diagram, no Structurizr DSL, so there were no technology slots. Participants (Kong, Redis)
  and every message label trace to the prompt; no protocol label anywhere.
- **NAT**: zero `\bNAT\b` matches in the document — the retracted false positive stayed out,
  and appears only in the reply as a deliberate exclusion.
- **Template extensibility** passed all three legs: the extra `Objetivos` and `Alternativas
  consideradas` carry user-supplied substance, the house order survives, and the reply says
  outright "Duas seções fora do padrão da casa" and offers to fold them back.

## One line to watch

`"Já operamos um Redis para sessão, compartilhado pelos serviços da plataforma"` — the
"compartilhado pelos serviços da plataforma" mildly expands the prompt's "o Redis que já
usamos pra sessão". The grader did not score it as invention: it names no new product and the
prompt's own contention risk implies sharing. It is the nearest miss in the run and worth
watching if this failure family reappears.

## Scope

One eval, one run. It verifies that mode (b) is closed **on this eval**; it is not a variance
measurement, and the other five evals were not re-run at 1.3.3 — they passed at 1.3.1/1.3.2
under the same corrected assertions, and 1.3.3 only adds a constraint.

Tokens 56,523.
