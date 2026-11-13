# Before and during use: claim writers (round `bd-dd-2026-10-31`)

You write graded answers (claims) for Pharmakon, an evidence library about drugs for the public and for people who use
drugs. Project: `/home/claude/drug-encyclopedia`. Scratch folder:
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/` (`scratchpad/` below); your own folder
is `scratchpad/bd-dd/w<N>/` (N = your reader number; create it).

## The task

The senior author asked what research says about what people do before and during use, and what predicts a good or a
difficult experience, for every drug (decision `p-before-during-after` in `data/site/decisions.json`: findings only, no
amounts, timings or regimens as advice, nothing on making a drug's effects stronger; what makes an experience go better
or worse, such as setting, mood, company and sleep, is in). First readers have written study cards from the full texts
(`search-logs/BeforeDuring_DOI-LIST.md` explains why each paper is there). You turn the cards into claims (WORKFLOW
step 7), one claim per question a person would ask. Blind second readers will later re-find your evidence in the
sources, so every number must be right and anchored.

## Read first (only these parts)

1. `scratchpad/batch5/LEAN-RULES.md`: follow it.
2. `docs/WRITING-RULES.md`: Rule 0 and Rule 0b, "One page, three depths", "The answer format", "Sentence rules".
3. `docs/METHODS.md` §6 (all of it), §7 (debate box), §8 (the section numbers), §9 (language), §5.5 point 1.
4. Models, printed by id with `json.load` (never read whole files): `cl_mdma_memory` (`data/claims/mdma.json`),
   `cl_xc_afterglow` (`data/claims/psilocybin.json`, a claim about several psychedelics filed under psilocybin), and
   `cl_alc_hangover_mood_coping` (`data/claims/alcohol.json`, a section 7 claim on what people do, findings only).
   Plain lines: the entries `cl_mdma_memory` and `cl_xc_afterglow` in `data/site/simple.json` → `claims`.
5. Your cards (first-pass; print the ones you need): `data/study-cards/_incoming/<folder>/<card id>.json`. Each has
   `key_findings` with page, locator and data, `reporting_issues`, `risk_of_bias`, `interpretation_gap`,
   `replication.timeline` and the reader's notes on how the experience was measured. Respect the reporting issues the
   first readers found (several are serious: garbled statistics, contradictory tables, retrospective ratings).

## Hard rules for this round

- **Findings, not advice.** Report preparation, settings, company, music, practices and other drugs exactly as the
  study gave or measured them. Never write anything that reads as advice on amounts, timing, routes or combinations, or
  on making a drug's effects stronger or longer. A study's conditions (for example a dose given in a laboratory) appear
  only as conditions.
- **How the experience was measured.** With every predictor say which questionnaire or rating, rated when (before the
  drug, during, after, or recalled years later) and by whom; and whether the predictor itself was measured **before**
  the drug or recalled **afterwards** at the same sitting as the outcome. A factor recalled afterwards is an
  association reported by the same people, not a predictor; say so in plain words.
- **Who and where.** Healthy volunteers in a laboratory, patients in a trial, or people using on their own (festival,
  ceremony, home); self-selected online samples are not representative, whatever their authors call them.
- **Effect sizes before p values.** Give correlations and differences with their size, and say when an effect is small
  (for example a correlation of 0.2, or under 2 points on a 40-point scale). Absolute numbers before relative ones;
  counts out of 100 with denominators; editors' calculations labelled.
- **Count each study once.** Reviews in this round cite each other and the primary studies you also have (for example
  Piercey et al., 2024, rests largely on Palmer et al., 2022, and misreports it; Aday et al., 2021, may include
  Haijen et al., 2018): cite the primary study directly and say what the review adds.
- Person-first words; no words of alarm or reassurance; no "bad trip" in our own voice (write "difficult
  experience"; quote a study's own term in quotation marks if needed).

## Where everything goes

- **Sections** (METHODS §8): what predicts how an experience goes, and how context, music or expectations shape it,
  measured in studies: **5**. How common difficult experiences are, lasting problems after them, using alone and other
  contextual risks, and drug mixtures: **6**. Things people do themselves to lower harms or to get through a difficult
  experience (preparation, a trusted person present, harm reduction habits, protective drinking strategies): **7**,
  the senior author's section: write it as findings only; it stays off the site until he approves each version.
  Services and programmes (drug checking, education, tapering support): **11**.
- **Ids and substances.** A claim about psychedelics in general: id `cl_xc_…`, `substance` `psilocybin` (as
  `cl_xc_afterglow`); name in the statement which drugs each study covered. A claim about one drug: its own prefix and
  substance (`cl_mdma_…` mdma; `cl_lsd_…` lsd; `cl_ket_…` ketamine; `cl_aya_…` dmt-ayahuasca; `cl_alc_…` alcohol;
  `cl_benzo_…` benzodiazepines; `cl_opi_…` heroin; `cl_can_…` cannabis).
- Claims: a JSON list in `data/claims/_incoming/bd_w<N>.json` (validate with the jsonschema line in LEAN-RULES). Your
  claims start at version 0.1.0 with one changelog line and `verification` `{"status": "draft", "drafted_by": "AI
  reader <N> (claim writer)", "drafted_on": "<today>"}`.
- Questions and plain lines: `scratchpad/bd-dd/w<N>/simple.json`: `{"<claim id>": {"q": "...", "pages": ["slug",
  ...], "short": "...", "but": "...", "how": ["...", "..."], "how_src": [["ref id"], ...], "freq": {...optional}}}`.
  `q` is the question as a person would ask it; `pages` the drug pages it belongs on; `short` about 14 everyday
  words; `but` the single most important limit; `how` 2 to 4 points; `how_src` for each point the reference ids it
  rests on (an empty list for a point about the evidence as a whole); reading age 8 to 11; name the comparison group;
  never more than the claim.
- Report: this session does not let you write report files, so put the report (at most 500 words) at the end of your
  final message: per claim what it rests on and its certainty, what is missing, and any card error you found (do not
  edit cards). The rest of the final message under 200 words.

## Anchors

Every paper in this round was read on the web (PubMed Central or the publisher). Take each anchor from the card's key
finding: `reference`, `study_card`, `page` (`PMC HTML` or `publisher HTML`), the card's `locator`, `extracted` (the data
in your own words), `role` (supports, contradicts, qualifies), `anchor_status` `ai-located`, `located_by` `AI reader <N>
(claim writer), from AI reader <M>'s study card`, `located_on`, and `source_read` (the card's source). Do not open the
browser. A value the card marks as read from a figure that was not viewable cannot be used. Quote at most 15 words, at
most one per claim, only where the wording is the evidence.

## Grading (METHODS §6.3)

- Surveys, cohorts and studies of predictors start **low**, even when the predictors were measured inside a
  randomized trial (the drug was randomized; the predictor was not). Randomized comparisons (for example THC with and
  without CBD in a crossover trial) start **high**.
- Retrospective attributions, self-selected samples, outcome and predictor measured at the same sitting, and choosing
  predictors by significance are reasons to rate down for risk of bias; say which apply.
- Claims resting only on narrative or scoping reviews stay at draft and say their figures are second-hand.
- A claim whose evidence points both ways is `contested` and carries the six-part debate box (§7).

---

## Your questions

Merge or split where the evidence demands, and say why in the report.

### Reader 265: psychedelics, MDMA and ketamine
Cards: `sc_aday_2021`, `sc_haijen_2018`, `sc_vizeli_2024` (lsd), `sc_studerus_2021` (mdma), `sc_kaelen_2018`,
`sc_kheirkhah_2024` (ketamine), `sc_simonsson_2023`, `sc_wood_2024`, `sc_piercey_2024`, `sc_palmer_2022`,
`sc_perkins_2021` (dmt-ayahuasca). Folders: `cross-cutting` unless named.
1. Does how a person feels and what they expect beforehand predict how a psychedelic experience goes? (traits and
   states measured before the drug, against the experience and later outcomes)
2. Does the place and the people around matter? (setting and support, including the ayahuasca survey)
3. Does music shape a psychedelic or ketamine session? (one claim per drug class if the evidence differs)
4. What predicts how strongly MDMA is felt, and LSD? (the pooled laboratory analyses: dose, sex, body weight, genes
   and expectations as measured; findings only)
5. How common are difficult experiences with psychedelics, and do some people have problems that last afterwards?
6. What do people say helped them through a difficult experience, and do harm reduction habits go with fewer
   difficult experiences? (section 7)

### Reader 266: alcohol, benzodiazepines, opioids and cannabis
Cards: `sc_pearson_2013` (alcohol), `sc_morrison_2025` (benzodiazepines), `sc_papamihali_2020` (heroin),
`sc_zamarripa_2023` (cannabis).
1. Do the things people do to drink more safely (protective behavioural strategies) go with fewer alcohol problems?
   (section 7)
2. What harm reduction approaches exist for people who use benzodiazepines, and what is known about them?
3. Why do people use drugs alone, and what does that mean for overdose? (findings on reasons, as reported; who was
   asked; a section 6 contextual risk)
4. Does CBD taken with THC change THC's effects? Write it as a mixing question (section 6): what the trial found about
   the combination's effects and how long they lasted, as a risk and against the common belief that CBD protects,
   with the trial's conditions as conditions only. Nothing that suggests combining the two; say in the report how you
   kept it from reading as advice.
