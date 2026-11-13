# Targeted checks, round 2, Cannabis round (can-a-2026-10-27), 31 October 2026

You are a new, independent reader for Pharmakon (METHODS §5.5). You have not read these sources for us before, and you
wrote none of these anchors or the findings behind them. Four adjudicators (AI readers 241 to 244) reviewed the cannabis
claims against the sources: they added new anchors and edited the wording or place of some anchors a second reader had
already checked. You check each one at the place it names. For an edited anchor, check the whole anchor as it now
reads.

Project: `/home/claude/drug-encyclopedia`. Scratch folder:
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/`; your own folder is `scratchpad/can-a/t<N>/`
(N = your reader number; create it).

## Read first

`data/verification/can-a-2026-10-27/targeted/BRIEF.md`: the three steps for each task, the verdicts (`confirmed`,
`corrected`, `wrong-location`, `not-found`), the 40-word note and the output format. Everything in it applies, with the
changes below.

## Changes for this round

- **Tasks:** `data/verification/can-a-2026-10-27/targeted2/tasks_reader<N>.json`. `kind` says whether the anchor is new,
  or a checked anchor whose wording or place was edited (one task asks about a single word).
- **PDF sources:** `/mnt/user-data/uploads/DrugEncyclopedia/` + the reference's `verification.pdf_path` in
  `data/references/cannabis.json`. A text extraction of most PDFs is in `scratchpad/can-a/numtext/` (pages separated by
  form feeds); check every number on a page you render yourself (`pdftoppm -r 150 -f N -l N -png`, then look at it).
  Cite printed pages; the AHA statement (Page et al., 2020) and other online-first PDFs: say which numbering you use.
- **Web sources** (PMC or the publisher): open the page in **one** tab of your own in the app's browser. Load the tools
  once with ToolSearch (query `mcp__remote-devices__Claude_Browser__`, max_results 64); `tabs_create`, then `navigate`
  to `https://pmc.ncbi.nlm.nih.gov/articles/<PMCID>/` or `https://doi.org/<DOI>`, its tabId on every call; read with
  `get_page_text` or `find`; never `preview_start`; never touch another tab; no search engines, no PDFs or downloads;
  never interact with a check page or CAPTCHA (wait a few minutes and try once more, otherwise give `not-found` with
  the note "deferred: page not readable"); close your tab at the end. Count running-text paragraphs (a table or figure
  legend is not a paragraph). A value printed only in a figure image needs a screenshot of your tab; if it comes back
  blank (the browser pane is hidden on the senior author's computer), give `not-found` with the note "deferred: figure
  image not viewable". Do not use any other reader's saved text files.
- **Independence:** do not open anything in `data/verification/can-a-2026-10-27/` other than this brief, the round-1
  brief and your task file; nor any other reader's folder in `scratchpad/`; nor the study cards. You may read the claims
  named in your tasks in `data/claims/_incoming/can_joined.json` for context. If you find that you did write an anchor
  or the finding behind it, say so in its note.
- **Output:** `data/verification/can-a-2026-10-27/targeted2/out_reader<N>.json`, written as you go, with
  `"reader": "AI reader <N> (second reader)"` and `"date": "2026-10-31"`. Change no other file. Quotations at most 15
  words. No advice on amounts, routes, timing or combinations.

Final message under 150 words: counts by verdict, and every correction that changes a number.
