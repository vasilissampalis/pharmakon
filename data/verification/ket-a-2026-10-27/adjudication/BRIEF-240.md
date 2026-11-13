# Ketamine round: adjudication of the two web-source claims (AI reader 240), 31 October 2026

You are an independent methodologist and adjudicator for Pharmakon. You did not write these claims or cards and you
took no part in the second reading. Read `data/verification/ket-a-2026-10-27/adjudication/BRIEF.md` first: everything in
it applies (what to read, what to do, output format, hard rules), with the changes below. Your reader number is 240;
your own folder is `scratchpad/ket-a/a240/`.

## Your group

| Claims | Cards |
|---|---|
| `cl_ket_acute_psychosis_dissociation` (only the points that turn on Beck et al., 2020: reader 233 adjudicated the rest on 30 October; its log is `233_log.json`, and its `deferred` items are yours) | `sc_beck_2020` |
| `cl_ket_mechanism_nmda_metabolites` (all of it; it rests on narrative reviews and stays `draft` under METHODS §6.3, but its text must still be right) | `sc_zanos_2018` |

## What you work from

- Second reader 229's blind outputs: `data/verification/ket-a-2026-10-27/out/zanos_2018.json` and `out/beck_2020.json`
  (claim verdicts with overstatement notes; `card_check` with key findings, reporting issues and `missed`). Reader 229
  says its own blind anchor giving 20 studies without a rating time was wrong; the Table gives 19.
- The reconciliation for these two sources: `data/verification/ket-a-2026-10-27/report-1031-zanos-beck.md`.
- Reader 229's targeted checks, already applied to the claims: `targeted/out_reader229.json`. Seven Zanos anchors were
  corrected or relocated; the claims' statements and magnitudes have not yet been brought into line with them (for
  example the statement may still say most other targets lie above the blood levels reached in people, or call the
  human cortex values post-mortem). Bring the statement, magnitude, PECO, grade reasoning and debate fields into line
  with the anchors as they now read.
- The sources are web full texts, not PDFs: Zanos et al. (2018), PMC6020109, and Beck et al. (2020), PMC7243091. Reader
  229's saved texts are in `scratchpad/ket-a/s229/` (`zanos_2018_full.txt`, `beck_2020_full.txt`); work from them. If a
  point cannot be settled there, you may read the PMC page in one tab of your own in the app's browser (load the tools
  once with ToolSearch, query `mcp__remote-devices__Claude_Browser__`, max_results 20; `tabs_create`, its tabId on every
  call, closed at the end; never `preview_start`; never touch another tab; no search engines, no PDFs or downloads;
  stop at any check page). Cite web texts by section and running-text paragraph (a table or figure legend is not a
  paragraph). Beck's supplement and its conflict-of-interest panel were not readable; say so where it matters.
- Erratum: Zanos et al. (2018) has an erratum (10.1124/pr.116.015198err) that corrects only the copyright line; no
  number is affected.

## Points to settle (at least)

1. `cl_ket_acute_psychosis_dissociation`: the recovery-time sentence must not read as coming from Beck (Beck gives no
   recovery time and says the time course is not yet characterised); "salt water ... on another day ... in every study
   read here" must not cover Beck's set (2 of its studies gave both conditions on the same day, with a larger effect);
   whether to say the positive and negative analyses did not rest on exactly the same studies; Beck's abstract I2
   range (77% to 83%) matching nothing in its Results; Newcomer et al. (1999) being among Beck's pooled studies (no
   double counting in what the claim concludes).
2. `cl_ket_mechanism_nmda_metabolites`: reader 229's five points (other targets within the clinically relevant range
   by the review's own account; post-mortem; species; spread labels; human recombinant dopamine receptors), and the
   corrected author-patent count.
3. Plain lines: `cl_ket_acute_psychosis_dissociation` has none yet in `data/site/simple.json`; write `q`, `short`,
   `but`, `how` (2 to 4) and, if a count fits, `freq`, in the format of the existing ketamine lines there (read three of
   them first). Start from `scratchpad/ket-a/w220/simple.json` if it has this claim, and from `233_simple.json`.

## Output

As in BRIEF.md, with N = 240 and `"date": "2026-10-31"`: `240_log.json`, `240_patch.json` (check it with
`python3 -I scripts/claim_patch.py <patch> --dry-run` against `data/claims/_incoming/ket_joined.json`), `240_simple.json`,
and the corrected cards `data/study-cards/_incoming/ketamine/sc_beck_2020.json` and `sc_zanos_2018.json`. Any number you
add needs a new anchor (`evidence_add`, ai-located, `located_by`: "AI reader 240 (adjudicator), from the PMC full text");
a fresh reader will check it. Change no other file. Final message as in BRIEF.md.
