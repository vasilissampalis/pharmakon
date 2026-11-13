# Targeted checks, round 3, Alcohol round (alc-a-2026-10-27), 30 October 2026

You are a new, independent reader for Pharmakon (METHODS §5.5). You have not read these sources for us before, and you
wrote none of these anchors or the findings behind them. Each anchor was written or reworded at adjudication (AI readers
221 and 223), sometimes from another reader's finding. You check each one at the place it names.

Project: `/home/claude/drug-encyclopedia`. Scratch folder: `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/`;
your own folder is `scratchpad/alc-a/t<N>/` (N = your reader number; create it).

## Read first

1. `data/verification/alc-a-2026-10-27/targeted/BRIEF.md`: the procedure, the three steps for each task, the verdicts
   (`confirmed`, `corrected`, `wrong-location`, `not-found`), the 40-word note and the output format. Everything in it
   applies, with the changes below.
2. `scratchpad/batch5/LEAN-RULES.md` for reading PDFs economically.

## Changes for this round

- **Tasks:** `data/verification/alc-a-2026-10-27/targeted3/tasks_reader<N>.json`. `kind` says whether the anchor is new
  or a checked anchor whose wording or place was edited; for an edited one, check the whole anchor as it now reads.
- **Sources:** PDFs only, from `/mnt/user-data/uploads/DrugEncyclopedia/` + the task's `source_read`. Extract the text
  yourself (`pdftotext -layout`) into your folder and render pages (`pdftoppm -r 150`) for every table and figure value
  you check. Cite printed pages (Mukamal and Askgaard are online-first PDFs: "p. N of the online-first PDF"). Do not use
  a browser.
- **Independence:** do not open anything in `data/verification/alc-a-2026-10-27/` other than this brief, the round-1
  brief and your task file; nor any other reader's folder in `scratchpad/`; nor the study cards. You may read the claim
  named in each task in `data/claims/alcohol.json` for context, as in round 1. If you find that you did write an anchor
  or the finding behind it, say so in its note.
- **Output:** `data/verification/alc-a-2026-10-27/targeted3/out_reader<N>.json`, written as you go, with
  `"reader": "AI reader <N> (second reader)"` and `"date": "2026-10-30"`. Change no other file.

Final message under 150 words: counts by verdict, and every correction that changes a number.
