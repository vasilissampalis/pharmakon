# Ketamine, Tier A: blind second readers (round `ket-a-2026-10-27`)

You are an independent **second reader** for Pharmakon (METHODS §5.5). First readers wrote study cards for the core
papers on ketamine, and claim writers turned 18 of them into 13 draft answers: how much reaches the blood by route and
how long it stays, brain imaging, the two mirror-image forms, effects during controlled sessions in volunteers and in
people with schizophrenia, how ketamine acts, and memory, thinking and wellbeing in people who use ketamine. You check
that work against the sources **without seeing their anchors first**.

Project: `/home/claude/drug-encyclopedia`. Scratch folder:
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/` (`scratchpad/` below). Your own folder:
`scratchpad/ket-a/s<N>/` (N = your reader number; create it).

## Read first

1. `docs/VERIFICATION-BRIEF.md` in full: it is your procedure (step 1 blind extraction per claim, step 2 the card check,
   the output format, where to read, the hard rules). Everything in it applies, with the changes below.
2. `docs/METHODS.md` §4.5, §5.3 to §5.5, §6 and §9.
3. `scratchpad/batch5/LEAN-RULES.md` for reading PDFs economically.

## Changes for this round

- **Round folder** `data/verification/ket-a-2026-10-27/`. Your task files are `tasks/<reference>.json` for the
  references assigned to you below; write `out/<reference>.json` for each, as you go, with
  `"reader": "AI reader <N> (second reader)"`.
- **Cards** for step 2: `data/study-cards/_incoming/ketamine/sc_<reference, hyphens as underscores>.json` (print it with
  python; never edit it).
- **Blindness.** Until your step 1 for a source is finished, do not open that source's card. Never open
  `data/claims/` (any file, including `_incoming/`), `data/site/`, anything in `scratchpad/ket-a/` other than your own
  folder, or any file in the round folder other than this brief, your task files and your own outputs.
- **PDFs** (the senior author's): `/mnt/user-data/uploads/DrugEncyclopedia/` + the task file's `pdf_path`. Extract the
  text yourself (`pdftotext -layout`) into your own folder and render pages (`pdftoppm -r 150`) for tables and figures.
  Several are old scanned pages whose machine-read text has errors (Krystal 1994, Malhotra 1996, Lahti 1995, Clements
  1982 and others with few fonts): check every number on the rendered page. Cite printed pages. Peltoniemi et al.
  (2016) is an online-first PDF without journal page numbers: cite "p. N of the online-first PDF". Ait Bentaleb et al.
  (print 2024) has an unnumbered cover page before printed pp. 211–224.
- **Numbers.** Check every number in each claim's statement and magnitude that comes from your source. Recompute every
  count, percentage, conversion and "editors' calculation"; say whether you get the same. Check that each blood level,
  time and effect is tied to the study condition it came from (route, preparation, infusion or dose as given, when
  measured).
- **Who and when.** Check that the claim keeps healthy volunteers, patients, and people who use ketamine outside a
  laboratory apart; effects during a session apart from lasting ones; and that it names the comparison group and the
  time since last use for every difference.
- **Wording.** Say whether a claim's wording overstates the source: association presented as effect, one laboratory or
  one small sample presented as general, a review's citation presented as its own finding, an animal or laboratory
  finding presented as shown in people. Flag anything that reads as advice on amounts, routes, timing or combinations,
  and any dose given other than as a study's condition.
- Report under 250 words: sources done, verdicts other than `supported`, card findings corrected, relocated or not
  found, and anything you could not read.

## Assignments

Task files are in `data/verification/ket-a-2026-10-27/tasks/` (18 sources; each lists only the claims that cite it and
the number and roles of the first reader's anchors from that source).

| Reader | Sources | How to read |
|---|---|---|
| 224 | `clements_1982`, `yanagihara_2003`, `peltoniemi_2016` | PDFs |
| 225 | `krystal_1994`, `malhotra_1996`, `newcomer_1999`, `lahti_1995` | PDFs |
| 226 | `vollenweider_1997a`, `vollenweider_1997b`, `ait-bentaleb_2024` | PDFs |
| 227 | `curran_2000`, `curran_2001`, `morgan_2012` | PDFs |
| 228 | `morgan_2004a`, `morgan_2009`, `morgan_2010b` | PDFs |
| 229 | `zanos_2018`, `beck_2020` | web (PMC), later: waits for the app's browser |
