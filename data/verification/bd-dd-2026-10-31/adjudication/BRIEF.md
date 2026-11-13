# Before and during use, and drug-death cards: review and adjudication (AI readers 280 to 285), 1 November 2026

You are an independent methodologist and adjudicator for Pharmakon, an evidence library about drugs for the public and
for people who use drugs. You did not write these claims or cards and you took no part in the second reading. Project:
`/home/claude/drug-encyclopedia`. Scratch folder: `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/`
(`scratchpad/` below); your own folder is `scratchpad/bd-dd/a<N>/` (create it).

The senior author asked, on 31 October, what studies show about the time before, during and after taking a drug, for
every drug, and for an honest, critical look at how drug deaths are counted. First readers (AI readers 246 to 253 and
263) wrote study cards; two claim writers (AI readers 265 and 266) wrote 15 claims; eight blind second readers (AI
readers 268 to 275) re-read every source, gave a verdict on each claim and checked each card; their unmatched anchors
were then checked at the stated place (every anchor of the 15 claims is now ai-checked). The claims are staged in
`data/claims/_incoming/bd_w265.json` and `bd_w266.json`; the cards in `data/study-cards/_incoming/<substance>/`. You
close the round: **the source decides**, not the first reader and not the second reader.

## Read first

1. `docs/METHODS.md`: §4.5, §5.3–5.6, §6 (all of it), §7, §8, §9, §12.
2. `docs/WRITING-RULES.md`: Rule 0, Rule 0b, "One page, three depths", "The answer format", "Sentence rules".
3. `docs/REVIEW-BRIEF-2.md`, "What to check, claim by claim" (A to F): your review standard.
4. `docs/ADJUDICATION-BRIEF.md` Part B (how to correct a card and log it) and `docs/ADJUDICATION-BRIEF-R2.md` "What to do
   with each finding" (verdicts, patches, GRADE rules).
5. `scripts/claim_patch.py` (its docstring): your patch format.
6. The claim writers' brief: `data/verification/bd-dd-2026-10-31/BRIEF-claim-writers-before-during.md`; reader 265's
   report `scratchpad/bd-dd/w265/_report.txt`.

## Your group

| Reader | Claims | Cards you adjudicate |
|---|---|---|
| 280 | `cl_xc_mindset_before`, `cl_xc_setting_support`, `cl_aya_ceremony_setting`, `cl_xc_difficult_how_common` | `sc_haijen_2018`, `sc_aday_2021`, `sc_perkins_2021`, `sc_simonsson_2023` |
| 281 | `cl_xc_music`, `cl_ket_music`, `cl_mdma_response_predictors`, `cl_lsd_response_predictors` | `sc_kaelen_2018`, `sc_kheirkhah_2024`, `sc_studerus_2021`, `sc_vizeli_2024` |
| 282 | `cl_xc_coping_during`, `cl_xc_harm_reduction_habits`, `cl_alc_protective_strategies`, `cl_benzo_own_practices` | `sc_wood_2024`, `sc_piercey_2024`, `sc_pearson_2013` (`sc_palmer_2022` is already ai-checked: change it only for an error) |
| 283 | `cl_benzo_harm_reduction_services`, `cl_opi_using_alone`, `cl_can_cbd_with_thc` | `sc_morrison_2025`, `sc_papamihali_2020`, `sc_zamarripa_2023` |
| 284 | none (cards only: how drug deaths are counted) | `sc_beynon_2007`, `sc_goldberger_2013`, `sc_garnett_2026`, `sc_slavova_2015`, `sc_slavova_2019`, `sc_gutkind_2025`, `sc_buchanich_2018` |
| 285 | none (cards only: how drug deaths are counted) | `sc_horon_2018`, `sc_lundberg_2026`, `sc_quesinberry_2019`, `sc_ferner_2008`, `sc_launiainen_2014`, `sc_strommer_2020` |

A card used by several groups (Simonsson 2023, Palmer 2022, Piercey 2024, Wood 2024, Haijen 2018, Vizeli 2024) is
changed only by the reader named above; a fact two groups state must have the same number in both. You may read other
groups' claims; patch only your own. Four claims are section 7 (`cl_xc_coping_during`, `cl_xc_harm_reduction_habits`,
`cl_alc_protective_strategies`, `cl_benzo_own_practices`): the senior author approves each before it is shown; adjudicate
them the same way.

## What you work from

- The second readers' outputs, one per source: `data/verification/bd-dd-2026-10-31/out/<reference>.json` (`claims`:
  verdict, overstatement and notes, their own anchors; `card_check`: each key finding and reporting issue, risk of bias,
  interpretation gap, `missed`). The reconciliation reports: `data/verification/bd-dd-2026-10-31/report-w265.md` and
  `report-w266.md`.
- The targeted checks: `data/verification/bd-dd-2026-10-31/targeted/out_reader268.json` to `out_reader271.json`
  (already applied to the claims; their notes often flag wording the claim still uses).
- The plain lines the claim writers wrote: `scratchpad/bd-dd/w265/simple.json` and `scratchpad/bd-dd/w266/simple.json`.
- **The sources** (all are web full texts in PubMed Central): the readers' saved copies in `scratchpad/bd-dd/s268/` to
  `s275/` and the first readers' folders `scratchpad/bd-dd/r246/` to `r253/` and `r263/` (for example
  `s269/haijen_2018.txt`, `s269/vizeli_2024.txt`, `s269/studerus_2021.txt`, `s270/perkins_2021.txt`,
  `s270/kaelen_2018.txt`, `s271/morrison_2025.txt`, `s273/slavova_2019.txt`, `s275/strommer_2020.txt`). If a point cannot
  be settled from a saved copy, open the PMC page in one tab of your own in the app's browser (load the tools once with
  ToolSearch, query `mcp__remote-devices__Claude_Browser__`, max_results 20; `tabs_create`, its tabId on every call,
  closed at the end; never `preview_start`; never touch another tab; no search engines, no PDFs or downloads; stop at
  any check page). Other readers use the browser at the same time. Cite web texts by section and running-text paragraph
  (a bulleted or numbered list is not a paragraph; a heading starts a new count).

## Points the editor has already noticed (check each; they are leads, not findings)

- `cl_xc_coping_during` (282): Simonsson Table: smoking cannabis was ticked by 113 (18.4%), more than changing the music
  (99, 16.2%), but the claim lists the music among the most ticked and says "fewer ticked" cannabis.
- `cl_xc_harm_reduction_habits` (282): Piercey's review does not say which drugs the preparedness-scale study covered,
  calls the ketamine paper "one study" without its design, and one MDMA source is a preprint; the claim groups them under
  classic psychedelics.
- `cl_mdma_response_predictors` (281): "one capsule" is wrong (25 or 100 mg capsules; 112 people took MDMA twice, once
  after a pretreatment); "did not differ" should be "did not differ significantly"; whether "this design cannot separate
  sex from dose per kilogram" overstates the limit (dose per kilogram ranged 0.8 to 2.7 mg/kg). Values found only in a
  supplement are not to be used. Also compare the claim with the MDMA page's answers on what MDMA feels like (search
  `data/claims/mdma.json` for Studerus or for sex differences): if they say something different about women and men,
  list it under `for_senior_author`.
- `cl_lsd_response_predictors` (281): "are among the reasons people feel more or less" is causal; earlier hallucinogen
  use is a between-person association.
- `cl_ket_music` (281): whether "the only study comparing music with no music" is exactly what Kheirkhah's review says;
  the second reader corrected Kheirkhah key finding 2.
- `cl_xc_mindset_before` (280): Haijen's 74.2% men and 32.7% with a diagnosis are of the 654 at baseline, not the 379;
  "on their own" means on their own initiative, not alone.
- `cl_aya_ceremony_setting` (280): the fasting finding ("no difference") should be "no detectable difference"; keep the
  finding and say plainly what it is. Whether fasting or other ceremony practices change anything is a judgment the
  senior author will see: list your reading under `for_senior_author`.
- `cl_benzo_harm_reduction_services`, `cl_benzo_own_practices` (282, 283): second reader 271 found both partly supported
  and that Gelberg et al. was left out; Morrison's Discussion says such policies "may differ" from harm reduction, not
  "depart".
- `cl_can_cbd_with_thc` (283): keep to what Zamarripa et al. measured (the CBD and THC amounts as study conditions, the
  people and the setting); no sentence may read as a way to change how strong cannabis feels. List the framing for the
  senior author.
- Drug-death cards (284, 285): every `corrected`, `wrong-location` and `missed` item in the second readers' outputs, for
  example Slavova 2019 (affiliations; the SAMHSA distinction between drug-caused and drug-detected deaths; the NAME,
  SAMHSA, OSAC and CSTE recommendations), Gutkind 2025 ("doubled" is 2.5-fold; Indiana is in the Midwest), Buchanich 2018
  (crude or age-adjusted rates; a before-and-after change read as an effect), Horon 2018 (reference numbering; Table 3
  labels; a rise attributed without data), Quesinberry 2019 (Discussion against Table 2), Ferner 2008 (Rouzioux range;
  reference 75), Launiainen 2014 (key finding 7: trazodone 0.57, dixyrazine 0.33, mesoridazine left off; ratios that
  cannot be reproduced) and Strommer 2020 (how "other" force is described; selection of sources).

## What to do

1. **Every second-reader verdict other than `supported`, every overstatement note, and every targeted-check note that
   flags wording** on your claims: check it at the source and give a verdict (`accept`, `accept-modified`, `reject`,
   `already-fixed`, `deferred`) with what you found.
2. **Your own review** of each claim (REVIEW-BRIEF-2 A to F): numbers against anchors and sources; each finding tied to
   its study condition and population (survey respondents, people at festivals, patients, volunteers in a laboratory
   kept apart); what was recalled afterwards kept apart from what was measured at the time; the comparison group named for
   every difference; the wording against the design (association never as effect; a recalled attribution never as a
   cause; one survey never as general; a review's citation never as its own finding); GRADE start, domains, arithmetic and
   reasoning per §6.3; status flags per §6.4. **Findings only:** an amount, a way of taking it, timing or a combination
   appears only as a study's condition, never as advice; no "safe" wording; authors' recommendations only when
   attributed.
3. **Write the claim patch** (`claim_patch.py` format, one object per claim you change, with a `change` line beginning
   "Review and adjudication, before-and-during round:"). Every number you put into a claim must be in an anchor's
   `extracted` text or be an editors' calculation you have recomputed. A needed number that no anchor carries goes in a
   new anchor (`evidence_add`, page and locator per §6.2, role, `located_by`: "AI reader <N> (adjudicator), from the web
   full text"); it enters as ai-located and a fresh reader will check it (say so in the log). Check with
   `python3 -I scripts/claim_patch.py <your patch> --dry-run` until it passes.
4. **Write the plain lines** for every claim of your group as they should read after your patch:
   `{"<claim id>": {"q", "short", "but", "how": [2 to 4], "freq"?}}` (reading age 8 to 11; `short` about 14 words;
   `but` the main limit; name the comparison group; never more than the claim says; numbers as counts out of 100, or
   1,000 for rare things; a question of 12 words or fewer). Read five existing lines in `data/site/simple.json` for the
   style. Start from the claim writer's lines and change what the claim or the source requires.
5. **Adjudicate the cards** of your group: every `card_check` item the second reader marked `corrected`,
   `wrong-location` or `not-found`, each `missed` item that is true and matters, and the card errors the claim writers'
   reports name (ADJUDICATION-BRIEF Part B). Write each changed card in full to its file in
   `data/study-cards/_incoming/<substance>/<card id>.json` (the editor keeps a backup), log every change in
   `verification.disagreements`, set `verification.checked_by` to "AI reader <second reader> (blind second reading) and
   AI reader <N> (adjudication)" and `checked_on` to today, and set `verification.status` to `ai-checked` when the readers
   agree on the overall risk-of-bias judgment; run `python3 -I scripts/check_card.py <file>` until it passes.
   Domain-level disagreements and interpretation-gap differences go to the senior author, not into the card.
6. **Anything the senior author must decide** goes in your log under `for_senior_author`.

## Output (in `data/verification/bd-dd-2026-10-31/adjudication/`)

- `<N>_log.json`: `{"reader": "AI reader <N> (adjudicator)", "date": "2026-11-01", "items": [{"claim_id" or "card",
  "source": "second reader <M> | targeted | own review", "finding": "...", "verdict": "...", "reason": "what you
  checked and found", "evidence": "page/section or card field", "patch_ref": "index in your patch or null"}],
  "for_senior_author": ["..."], "deferred": ["..."]}`
- `<N>_patch.json`: the claim patch (readers 280 to 283).
- `<N>_simple.json`: the plain lines (readers 280 to 283).
- Corrected cards in `data/study-cards/_incoming/<substance>/`.
Write each file as you go (rewrite it after every claim or card), so nothing is lost if you are stopped.

## Rules (hard)

- Never edit `data/claims/` (including `_incoming/`), `docs/`, `scripts/` or `site/`, or any card outside your group:
  you write proposals and corrected copies; the editor applies them.
- No advice on amounts, ways of taking a drug, timing or combinations; no "safe" wording; findings only. Person-first
  words ("people who use drugs", "people who died"); no words of alarm or reassurance. Quotations at most 15 words, at
  most one per claim, word for word.
- Final message under 250 words: counts by verdict; certainty or status changes (claim, from → to, rule); new anchors;
  cards changed and set to ai-checked; the five most consequential edits; what the senior author must decide. Then a
  short report (at most 300 words).
