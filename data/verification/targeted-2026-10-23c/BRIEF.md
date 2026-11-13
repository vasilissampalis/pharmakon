# Second reading: lung cancer, effects by route, edible labels and children (AI reader 97, 2026-10-23)

You are a second reader for Pharmakon, an evidence library about drugs. The project is `/home/claude/drug-encyclopedia`. AI readers 91 and 92 wrote 36 new evidence anchors from four papers, in four cannabis claims: `cl_can_smoked_cancer`, `cl_can_smoked_lungs`, `cl_can_vaped_lungs` and `cl_can_edibles`. You wrote none of them. Check each one at the place it cites.

**Tasks:** `data/verification/targeted-2026-10-23c/tasks.json` (n = 1 to 36).

**Output:** `data/verification/targeted-2026-10-23c/out_reader97.json`, with `"reader": "AI reader 97 (second reader)"` and `"date": "2026-10-23"`. Write it as you go.

Follow the method, verdicts and rules in `data/verification/targeted-2026-10-18o/BRIEF_a.md` (the sections "For each task" and "Rules"), with the changes below. Ignore its PDF table and its browser steps.

**Sources:** local PDFs only, with no browser and no web. All are in `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/Cannabis/`:

| reference | PDF |
|---|---|
| callaghan_2013 | `Callaghan_2013_LungCancerCohort.pdf`. It has no printed page numbers: anchors cite PDF pages. |
| muheriwa-matemba_2024 | `MuheriwaMatemba_2024_CardioRespiratoryByRoute.pdf`. PDF page 3 is printed page 1332; anchors cite printed pages. |
| vandrey_2015 | `Vandrey_2015_EdibleLabelAccuracy.pdf`, and its correction `Vandrey_2015_EdibleLabelAccuracy_Erratum.pdf`. The correction's labels win where the two differ. |
| tweet_2023 | `Tweet_2023_PediatricEdibleExposures.pdf`. Text extraction garbles some signs (for example "+124.7%" can come out as "1124.7%"), so check every number you rely on against a rendered page image. |

- Extract each PDF once with `pdftotext -layout` into `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/reader97/`.
- Render only the pages with the tables or figures you need, with `pdftoppm -r 110`.

These are **section 7 drafts** (ways of taking a drug, compared); they go to the senior author before anything is published. Besides each number, check:
- the anchor says no more than the paper;
- every comparison names its comparison group as the paper does;
- funding and interests are reported as printed;
- nothing reads as advice on how to use a product.

Children's exposures are findings about children, not about the reader's own use.

Do not open the first readers' files (`scratchpad/routes/reader91*`, `scratchpad/routes/reader92*`, `scratchpad/reader91/`, `scratchpad/reader92/`), the study cards in `data/study-cards/_incoming/`, or `data/claims/`.

**Final message:** under 150 words. Give how many tasks were confirmed, corrected, wrong-location and not-found, and any correction that changes a number.
