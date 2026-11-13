# Second reading: MDMA at a Saturday night dance (AI reader 95, 2026-10-23)

You are a second reader for Pharmakon, an evidence library about drugs. The project is `/home/claude/drug-encyclopedia`. AI reader 94 wrote 4 new evidence anchors from one paper, in the claims `cl_mdma_tolerance_chronic` and `cl_mdma_feelings`. You wrote none of them. Check each one at the place it cites.

**Tasks:** `data/verification/targeted-2026-10-23a/tasks.json` (n = 1 to 4).

**Output:** `data/verification/targeted-2026-10-23a/out_reader95.json`, with `"reader": "AI reader 95 (second reader)"` and `"date": "2026-10-23"`. Write it as you go.

Follow the method, verdicts and rules in `data/verification/targeted-2026-10-18o/BRIEF_a.md` (the sections "For each task" and "Rules"), with the changes below. Ignore its PDF table and its browser steps.

**Source:** a local PDF only, with no browser and no web: `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/MDMA/Parrott_1998_SaturdayNightDance.pdf` (Parrott & Lasky, 1998).
- Extract it once with `pdftotext -layout` into `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/reader95/`.
- Render only the pages whose tables you need, with `pdftoppm -r 110`, and check every number on the image.

Besides each number, check two things:
- the anchor says no more than the paper;
- every comparison names its comparison group as the paper does.

Tablet counts are self-reported use in that sample. They are a study condition, never guidance. Flag any wording that reads otherwise.

Do not open the first reader's files (`scratchpad/routes/reader94*`, `scratchpad/reader94/`), the study cards in `data/study-cards/_incoming/`, or `data/claims/`.

**Final message:** under 120 words. Give how many tasks were confirmed, corrected, wrong-location and not-found, and any correction that changes a number.
