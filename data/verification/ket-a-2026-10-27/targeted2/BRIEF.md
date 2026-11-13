# Targeted checks, round 2, Ketamine round (ket-a-2026-10-27), 30 October 2026

You are a new, independent reader for Pharmakon (METHODS §5.5). You have not read these sources for us before, and you
wrote none of these anchors or the findings behind them. Three adjudicators (AI readers 231, 232 and 233) reviewed the
ketamine claims against the sources: they added new anchors and edited the wording or place of some anchors that a
second reader had already checked. You check each one at the place it names. For an edited anchor, check the whole
anchor as it now reads.

Project: `/home/claude/drug-encyclopedia`. Scratch folder:
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/`; your own folder is
`scratchpad/ket-a/t<N>/` (N = your reader number; create it).

## Read first

1. `data/verification/ket-a-2026-10-27/targeted/BRIEF.md`: the three steps for each task, the verdicts (`confirmed`,
   `corrected`, `wrong-location`, `not-found`), the 40-word note and the output format. Everything in it applies, with
   the changes below.
2. `scratchpad/batch5/LEAN-RULES.md` for reading PDFs economically.

## Changes for this round

- **Tasks:** `data/verification/ket-a-2026-10-27/targeted2/tasks_reader<N>.json`. `kind` says whether the anchor is new
  or a checked anchor whose wording or place was edited.
- **Sources:** PDFs only, from `/mnt/user-data/uploads/DrugEncyclopedia/` + the task's `source_read`. A plain text
  extraction of each PDF, made by the editor, is in `scratchpad/ket-a/numtext/` (pages separated by form feeds); several
  are old scans whose machine-read text has errors (Lahti 1995, Malhotra 1996, Newcomer 1999 and others), so check every
  number on a page you render yourself (`pdftoppm -r 150`). Cite printed pages; Peltoniemi et al. (2016) is an
  online-first PDF ("p. N of the online-first PDF"). Do not use a browser.
- **Independence:** do not open anything in `data/verification/ket-a-2026-10-27/` other than this brief, the round-1
  brief and your task file; nor any other reader's folder in `scratchpad/`; nor the study cards. You may read the claim
  named in each task in `data/claims/_incoming/ket_joined.json` for context. If you find that you did write an anchor or
  the finding behind it, say so in its note.
- **Output:** `data/verification/ket-a-2026-10-27/targeted2/out_reader<N>.json`, written as you go, with
  `"reader": "AI reader <N> (second reader)"` and `"date": "2026-10-30"`. Change no other file. Quotations at most 15
  words. No advice on amounts, routes, timing or combinations.

Final message under 150 words: counts by verdict, and every correction that changes a number.
