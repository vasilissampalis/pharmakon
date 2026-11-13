# Second reading: cannabis strength, concentrates and dependence (AI reader 98, 2026-10-23)

You are a second reader for Pharmakon, an evidence library about drugs. The project is `/home/claude/drug-encyclopedia`. AI reader 93 wrote 20 new evidence anchors from three papers, in `cl_can_concentrates` and the new claim `cl_can_potency_dependence`. You wrote none of them. Check each one at the place it cites.

**Tasks:** `data/verification/targeted-2026-10-23d/tasks.json` (n = 1 to 20).

**Output:** `data/verification/targeted-2026-10-23d/out_reader98.json`, with `"reader": "AI reader 98 (second reader)"` and `"date": "2026-10-23"`. Write it as you go.

Follow the method, verdicts and rules in `data/verification/targeted-2026-10-18o/BRIEF_a.md` (the sections "For each task" and "Rules"), with the changes below. Ignore its PDF table and its browser steps.

**Sources:** local PDFs only, with no browser and no web. All are in `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/Cannabis/`:
- `Petrilli_2022_PotencySR.pdf` (petrilli_2022)
- `Inman_2026_FlowerConcentratesEdiblesCUD.pdf` (inman_2026)
- `Leung_2020_CUDPrevalenceMA.pdf` (leung_2020)

Extract each once with `pdftotext -layout` into `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/reader98/`. Render only the pages with tables or figures you need, with `pdftoppm -r 110`, and check every number you rely on against the image.

These are **section 7 drafts** (ways of taking a drug, compared); they go to the senior author before anything is published. Besides each number, check:
- the anchor says no more than the paper;
- every comparison names its comparison group as the paper does;
- each review's conclusions are given as the review's;
- the study designs under each finding are named;
- nothing reads as advice on how to use a product or how strong a product to choose.

THC strengths appear only as study conditions or measured product content.

Do not open the first reader's files (`scratchpad/routes/reader93*`, `scratchpad/reader93/`), the study cards in `data/study-cards/_incoming/`, or `data/claims/`.

**Final message:** under 150 words. Give how many tasks were confirmed, corrected, wrong-location and not-found, and any correction that changes a number.
