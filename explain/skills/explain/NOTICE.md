# Notices and attribution

This skill restates, in its own words, findings and practices from the sources below. No
text and no example from any of them is reproduced: every example in `SKILL.md` and in
`references/` was written for this skill.

The findings were taken from the papers themselves, from their abstracts, or from
secondary summaries of them. For that reason the skill states no effect size, and it
claims no gain in learning or comprehension: no explanation prompt or skill, this one
included, has published outcome data.

## Research on explanation and instruction

- **The reader's prior knowledge decides which device works**: Kalyuga, Ayres, Chandler
  and Sweller (2003), the expertise reversal effect.
- **The explainer misjudges the reader, and warnings do not fix it**: Camerer, Loewenstein
  and Weber (1989), the curse of knowledge; Tullis and Feder (2023); Nückles, Wittwer and
  Renkl (2005), on giving the explainer information about the reader.
- **What separates explanations that work**: Wittwer and Renkl (2008); Kulgemeyer (2018);
  Kulgemeyer and Wittwer (2022), which also shows that a fluent wrong explanation feels
  as clear as a correct one.
- **Explanations are contrastive and selected**: Miller (2019), "Explanation in
  Artificial Intelligence: Insights from the Social Sciences".
- **Worked examples and fading**: Barbieri and colleagues (2023); Renkl, Atkinson and
  colleagues.
- **Concrete to abstract, and cutting interesting but irrelevant detail**: McNeil and
  Fyfe (2012); Sundararajan and Adesope (2020).
- **Analogies, their mapping and their limits**: Gick and Holyoak (1983); Alfieri,
  Nokes-Malach and Schunn (2013); Spiro and colleagues (1989); Glynn's
  Teaching-With-Analogies model.
- **Refutation texts**: Schroeder and Kucera (2022); Kendeou and colleagues.
- **The illusion of explanatory depth**: Rozenblit and Keil (2002).
- **Contrasting cases before the rule**: Schwartz and Bransford (1998).
- **Defining the parts first, signaling, segmenting, addressing the reader**: Richard
  Mayer's principles of multimedia learning.
- **Narrative, and one case standing for many**: Mar and colleagues (2021); Dahlstrom
  (2014).
- **Checking understanding by asking the reader to restate or apply**: the teach-back
  method of the AHRQ Health Literacy Universal Precautions Toolkit.
- **Easy explanations raise confidence**: Scharrer, Rupieper, Stadtler and Bromme (2017),
  the easiness effect.

## Research on clear writing

- **Jargon and where to put its replacement**: Bullock and colleagues (2019); Kerwer and
  colleagues (2021).
- **Nested clauses as the main source of difficulty**: Martínez, Mollica and Gibson
  (2022, 2023).
- **Clarity judged by what the reader can do**: ISO 24495-1:2023, Plain language, and in
  Brazil ABNT NBR ISO 24495-1:2024 and Lei 15.263/2025.
- **Shorter messages and the editor's bias toward adding**: Todd Rogers and Jessica
  Lasky-Fink, *Writing for Busy Readers* (2023).
- **Tone misread in writing**: Kruger, Epley, Parker and Ng (2005).
- **Risk as absolute figures and counts**: Gigerenzer and colleagues (2007).
- **Uncertainty as a number with a range**: van der Bles and colleagues (2020).
- **Information alone does not persuade**: National Academies of Sciences, Engineering,
  and Medicine, *Communicating Science Effectively* (2017).

## Research on machine-written explanations

- **Level adaptation that changes only length and vocabulary**: Joshi and colleagues
  (2025), ELI-Why.
- **Overgeneralization when summarizing**: Peters and Chin-Yee (2025).
- **Longer explanations raising confidence without accuracy**: Steyvers and colleagues.
- **Analogies raising confidence without accuracy**: Shao and colleagues (2025).
- **Tutors that help and tutors that harm**: Bastani and colleagues (2024); Kestin and
  colleagues (2025).

## Practices

- **Explanation as a genre apart from how-to, tutorial and reference**: Diátaxis, by
  Daniele Procida, <https://diataxis.fr>.
- **The defects of confusing explanations**: Julia Evans,
  <https://jvns.ca/blog/confusing-explanations/>.
- **Context before the bottom line when the bottom line needs it**: Bryan Garner.
- **A one-off question is answered, not turned into a tutoring session**: the boundary
  drawn by the `socratic-tutor` skill of Jane Street's `agent_skills`.
- **"And, but, therefore" as a test of whether a text has a point**: Randy Olson, who
  credits Trey Parker and Matt Stone.

## Not from these sources

These parts are this skill's own:

- The rule for choosing a device by the reader's situation. No study compares the named
  formats, and no validated procedure for choosing among them was found.
- "Facts are recorded, illustrations are built": the form the repository's "record,
  don't invent" contract takes in a skill that has to build examples.
- Applying teach-back, which was tested in spoken clinical encounters, to written
  explanation.
- The checks of a draft against the stated reader. The research shows that information
  about the reader helps and that warnings do not; the checklist itself was not tested.
