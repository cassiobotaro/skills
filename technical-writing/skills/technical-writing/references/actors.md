# Finding the actor

Before and after pairs for the actor pass, in English and in Portuguese. Every pair was
written for this skill. The components in them are invented for illustration: in a real
document the actor comes from the source, never from this file.

## Contents

- The test
- Where the actor hides
- When the source does not name the actor
- The passives that stay
- Notes for Portuguese
- "We", "you", and the software

## The test

Take one verb at a time, including the verbs buried in nouns ("validation",
"configuração"). Ask "who or what does this?" Then check two things: the sentence
answers, and the answer is the grammatical subject. A sentence can pass the first and
fail the second ("validation is performed by the gateway"), and then the fix is only a
reordering.

For the grammatical passive there is a faster detector, Rebecca Johnson's: insert "by
zombies" after the verb, or at the end of the clause when an object is in the way. If
the sentence still reads as a sentence, the verb is passive.

| Sentence | With zombies | Verdict |
|---|---|---|
| The token is validated before the request is forwarded. | The token is validated [by zombies] before the request is forwarded [by zombies]. | Two passives, two actors to look up. |
| The gateway validates the token. | The gateway validates [by zombies] the token. | Not a sentence. Active. |
| O token é validado antes do envio. | O token é validado [por zumbis] antes do envio. | Passive. "Envio" hides a second verb that the zombies do not catch. |

The zombies have two limits. They find the form and not the other five hiding places: a
noun that swallowed the verb, an empty subject, a catch-all actor, a described
instruction, and the Portuguese forms with "se" all pass the test and still hide the
actor. And they also fit a state ("The service is written in Go [by zombies]"), which is
one of the passives that stay. Use the test to find candidates, then decide each one
with the question.

The question is about information, not about grammar. A passive that names its actor has
lost nothing but directness. A passive without one has dropped a fact. Spend the effort
on the second kind.

## Where the actor hides

### A passive without its agent

| Before | After |
|---|---|
| The data is encrypted before it is stored. | The `ledger` service encrypts the data before it writes the data to PostgreSQL. |
| Failed jobs are retried three times. | The worker retries a failed job three times. |
| Os dados são criptografados antes de serem gravados. | O serviço `ledger` criptografa os dados antes de gravá-los no PostgreSQL. |
| Os jobs com falha são reprocessados três vezes. | O worker reprocessa três vezes cada job que falha. |

A sentence often hides two actors. "The token is validated and the request is forwarded"
may be one component or two. Look both up.

### A noun that swallowed the verb

| Before | After |
|---|---|
| After validation of the token, forwarding of the request occurs. | After the gateway validates the token, it forwards the request to the `orders` service. |
| Rotation of the keys happens monthly. | A scheduled job, `rotate-keys`, rotates the keys on the first day of each month. |
| Após a validação do token, ocorre o encaminhamento da requisição. | Depois de validar o token, o gateway encaminha a requisição ao serviço `orders`. |

The nouns to watch end in "-tion", "-ment", "-ance", "-al", and in Portuguese in "-ção",
"-mento", "-agem". Verbs such as "occur", "happen", "take place", "ocorrer", and
"realizar" next to one of them confirm the pattern.

### A subject that means nothing

| Before | After |
|---|---|
| It is recommended to enable the cache. | The platform team recommends enabling the cache. *Or, as an instruction:* Enable the cache. |
| There is a timeout of 30 seconds. | The client gives up after 30 seconds. |
| É necessário reiniciar o serviço após a mudança. | Reinicie o serviço depois de mudar o arquivo. |
| Existe uma verificação de permissão. | O middleware `authz` verifica a permissão. |

"It is recommended" hides who recommends. When nobody in particular does, the sentence
is an instruction, so write it as one.

### A catch-all actor

| Before | After |
|---|---|
| The system sends a notification. | The `notifier` worker sends an email to the account owner. |
| The application handles the error. | The `orders` handler catches the error and returns `503`. |
| O sistema envia uma notificação. | O worker `notifier` envia um e-mail ao titular da conta. |

"The system" is an actor only when the system has one part, or when the document is for
a reader who sees it from outside and has no use for the parts. "Handles", "manages",
"processes", "trata", and "gerencia" usually travel with the catch-all actor. Replace them with
what the component does.

### An instruction written as a description

| Before | After |
|---|---|
| The `DATABASE_URL` variable must be set. | Set `DATABASE_URL`. |
| The migration should be run before the deploy. | Run the migration before you deploy. |
| A variável `DATABASE_URL` deve ser definida. | Defina `DATABASE_URL`. |

When the reader is not the one who acts, say who is: "The CI pipeline runs the migration
before each deploy. You do not run it by hand."

## When the source does not name the actor

Look in this order: the code path, the configuration and the deployment files, the
existing docs, the conversation. Then:

- **Writing a new document.** If the reader's task depends on the actor, ask the user
  before writing. If it does not, leave the sentence out and list the question in the
  reply.
- **Revising someone's text.** Keep the sentence as the author wrote it and put the
  question in the reply: "'Backups are rotated weekly': nothing in the repository says
  what rotates them. Who or what does?"
- **Called by another skill.** The question goes where that skill puts its open
  questions.

Never settle it with "the system", and never promote a likely candidate. A reader who
knows the real actor stops trusting the rest of the document.

## The passives that stay

**The actor is unknown.** Common in a postmortem and in a bug report. Say that it is
unknown, so that the reader does not take the gap for an omission: "The flag was turned
off at 09:40. The audit trail was not enabled, so we do not know by whom."

**The verb describes a state.** "The library is licensed under MIT." "The table is
partitioned by month." "O serviço é escrito em Go." Nobody asks "by whom?", and a rewrite
would invent an actor to satisfy a rule. The check is the question itself. If a reader
could need the answer ("the certificate is renewed every 60 days"), the verb describes
an action.

A passive that names its actor with "by" does not stay. It hides nothing, and it is
tempting in a paragraph that follows one thing through a pipeline, because a sentence
reads best when it begins with what the reader already holds. Keep that thing at the
front and give it an active verb instead:

| Before | After |
|---|---|
| The message is then enriched by the `geo` consumer, which adds the region, and stored by the `archive` consumer. | The message then goes to the `geo` consumer, which adds the region, and to the `archive` consumer, which stores it. |
| A requisição é então assinada pelo gateway. | A requisição segue para o gateway, que a assina. |

Verbs that let the object lead are "goes to", "reaches", "passes through", "arrives
at", and in Portuguese "segue para", "chega a", "passa por".

## Notes for Portuguese

- **Voz passiva analítica**: "é enviado", "foi configurado", "será validado". Same
  rewrite as in English.
- **Voz passiva sintética e sujeito indeterminado**: "envia-se", "configura-se o
  serviço", "precisa-se de", "deve-se executar". Shorter than the analytic passive, and
  the actor is just as absent. In an instruction, use the imperative: "Execute".
- **Infinitivo impessoal**: "É preciso reiniciar", "Basta rodar". Write the instruction
  ("Reinicie") or the actor ("O deploy reinicia").
- **Steps in the infinitive** ("Executar o script", "Abrir o painel") are a house style
  in some teams. Follow the docs already in the repository. With no precedent, use the
  imperative, in the form of address those docs or the conversation use ("Execute",
  "Rode").
- Keep the identifiers and the technical terms the team uses in English as they are. Do
  not translate a component name.

## "We", "you", and the software

- "You" is the reader. In a procedure the imperative already says so.
- "We" is the team that owns the document, and only that. Do not use it for the software
  ("we then parse the file") or for the reader and the writer together, except in a
  tutorial, where "we" walking through the steps is a convention.
- The software is named: the component, the command, the function. In a reference page
  the thing described is the actor of its own entry: "`retry()` returns the last error".
