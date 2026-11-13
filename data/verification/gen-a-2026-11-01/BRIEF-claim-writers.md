# Drug use in general: claim writers (round `gen-a-2026-11-01`)

You write graded answers (claims) for Pharmakon, an evidence library about drugs for the public and for people who use
drugs. Project: `/home/claude/drug-encyclopedia`. Scratch folder:
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/` (`scratchpad/` below); your own folder
is `scratchpad/gen-a/w<N>/` (N = your reader number; create it).

## The task

The senior author asked for answers, and quiz questions built from them, on drug use in general: women and men,
"telescoping", genes and family, starting young, the words used about people who use drugs and other facts people
find useful, each read with a critical, objective eye (decision `s-quiz-v2`). First readers have written study cards
from the full texts (`search-logs/General_DOI-LIST.md` explains why each paper is there and how they answer each other).
Several key papers are still being saved as PDFs; where one matters to your question, name it as not yet read (by
author and year) in the claim's limits and in your report, and do not describe its findings second-hand as if read.

## Read first (only these parts)

1. `scratchpad/batch5/LEAN-RULES.md`: follow it.
2. `docs/WRITING-RULES.md`: Rule 0 and Rule 0b, "One page, three depths", "The answer format", "Sentence rules".
3. `docs/METHODS.md` §6 (all of it), §7 (debate box), §8 (the section numbers), §9 (language), §5.5 point 1.
4. `data/verification/gen-a-2026-11-01/BRIEF-first-readers.md`, "What to record for these topics": the same points
   must reach the claims.
5. Models, printed by id with `json.load` (never read whole files): `cl_mdma_memory` (`data/claims/mdma.json`), a
   contested claim with a debate box `cl_can_psychosis_causation` (`data/claims/cannabis.json`), and a claim built on
   population surveys `cl_can_dependence_how_many` (same file). Plain lines: the entries `cl_mdma_memory` and
   `cl_can_dependence_how_many` in `data/site/simple.json` → `claims`.
6. Your cards (first-pass; print the ones you need): `data/study-cards/_incoming/<folder>/<card id>.json`. Respect the
   reporting issues the first readers found (several tables contradict their text; some p values are wrongly printed).

## Hard rules for this round

- **Samples decide what a difference means.** For every difference between women and men, say whether the sample was
  people in treatment or the general population, how the timing of each step was measured (recalled years later, or
  recorded as it happened), and what was adjusted for. A faster average time to dependence among all drinkers mostly
  reflects who becomes dependent at all; say which quantity each figure is.
- **Cause.** Say what each design can and cannot show (co-twin, adoption, common-factor model, survey, cohort,
  experiment). Animal findings are labelled as such and never stand in for people.
- **Heritability.** A figure applies to one population in one era; say which. A heritability is not the share of one
  person's risk that is genetic; say so in plain words where a figure appears.
- **Words.** Person-first language; no words of alarm or reassurance; quote a study's own labels (for example
  "addict") only in quotation marks, as the study's wording.
- Findings only: no advice on how much, how often or how to use.

## Where everything goes

- **Ids and substances.** Answers about drug use in general: id `cl_gen_…`, `substance` `general`. Answers about one
  drug: its prefix and substance (`cl_alc_…` alcohol, `cl_coc_…` cocaine).
- **Sections** (METHODS §8): progression, dependence and patterns of use, and risk factors for use disorders: **8**;
  treatment entry and outcomes: **12**; how words and labels change the way others see people who use drugs: **11**.
- Claims: a JSON list in `data/claims/_incoming/gen_w<N>.json` (validate with the jsonschema line in LEAN-RULES). Your
  claims start at version 0.1.0 with one changelog line and `verification` `{"status": "draft", "drafted_by": "AI
  reader <N> (claim writer)", "drafted_on": "<today>"}`.
- Questions and plain lines: `scratchpad/gen-a/w<N>/simple.json`: `{"<claim id>": {"q": "...", "short": "...", "but":
  "...", "how": ["...", "..."], "how_src": [["ref id"], ...], "freq": {...optional}}}`. `q` as a person would ask it;
  `short` about 14 everyday words; `but` the single most important limit; `how` 2 to 4 points; `how_src` for each
  point the reference ids it rests on (an empty list for a point about the evidence as a whole); reading age 8 to 11;
  name the comparison group; never more than the claim.
- Report: this session does not let you write report files, so put the report (at most 500 words) at the end of your
  final message: per claim what it rests on and its certainty, what is missing (which unread papers would change it),
  and any card error you found (do not edit cards). The rest of the final message under 200 words.

## Anchors

Every paper in this round was read on the web (PubMed Central or the publisher). Take each anchor from the card's key
finding: `reference`, `study_card`, `page` (`PMC HTML` or `publisher HTML`), the card's `locator`, `extracted` (the data
in your own words), `role` (supports, contradicts, qualifies), `anchor_status` `ai-located`, `located_by` `AI reader <N>
(claim writer), from AI reader <M>'s study card`, `located_on`, and `source_read` (the card's source). Do not open the
browser. A value the card marks as read from a figure that was not viewable cannot be used. Quote at most 15 words, at
most one per claim, only where the wording is the evidence.

## Grading (METHODS §6.3)

- Surveys, cohorts, twin and adoption studies start **low**; randomized experiments start **high** (the labels study
  randomized its vignettes). Count each study once: reviews in this round cite the same surveys (NESARC appears in
  several cards).
- Claims resting only on narrative reviews stay at draft and say their figures are second-hand.
- A claim whose evidence points both ways is `contested` and carries the six-part debate box (§7); telescoping is the
  obvious candidate.

---

## Your questions

### Reader 267
Cards: `sc_keyes_2010` (alcohol), `sc_marks_2018`, `sc_mchugh_2018`, `sc_greenfield_2007`, `sc_kendler_2012`,
`sc_prom_wormley_2017`, `sc_pennington_2023` (folder `cross-cutting`), `sc_maimaris_2014`, `sc_irons_2015` (alcohol),
`sc_liu_2018` (cocaine).
1. Do women go from first use to problems faster than men ("telescoping")? (treatment samples against national
   surveys; what the idea's history shows; Randall et al., 1999, is not read yet)
2. Are women less likely to start treatment for drug or alcohol problems, and do they do as well in it?
3. How much do genes and the family people grow up in shape drug problems? (the Swedish adoption study and the
   review; Visscher et al., 2008, on what heritability means, is not read yet)
4. Does drinking at a young age lead to alcohol problems later, or do the same things lead to both? (the review of
   cohorts and the twin study; Grant & Dawson, 1998, is not read yet)
5. Do the words used about people who use drugs change how others see them? (the randomized labels study)
6. How often do people who use cocaine also use alcohol or cannabis, and why does it matter for research on cocaine?
