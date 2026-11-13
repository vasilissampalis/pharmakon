# Second reading: two critiques of the vaping evidence (AI reader 96, 2026-10-23)

You are a second reader for Pharmakon, an evidence library about drugs. The project is `/home/claude/drug-encyclopedia`. AI reader 90 wrote 17 new evidence anchors from two papers, in the claims `cl_nic_vapes_relative_risk` and `cl_nic_vapes_disease`. You wrote none of them. Check each one at the place it cites.

**Tasks:** `data/verification/targeted-2026-10-23b/tasks.json` (n = 1 to 17).

**Output:** `data/verification/targeted-2026-10-23b/out_reader96.json`, with `"reader": "AI reader 96 (second reader)"` and `"date": "2026-10-23"`. Write it as you go.

Follow the method, verdicts and rules in `data/verification/targeted-2026-10-18o/BRIEF_a.md` (the sections "For each task" and "Rules"), with the changes below. Ignore its PDF table and its browser steps.

**Sources:** local PDFs only, with no browser and no web.
- `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/Nicotine/McKee_2015_ECigaretteEvidenceRockOrSand.pdf` (McKee & Capewell, 2015, BMJ).
- `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/Nicotine/Mendelsohn_2022_CriticalAnalysisECigaretteReview..pdf` (Mendelsohn et al., 2022, Drug and Alcohol Review).

Extract each once with `pdftotext -layout` into `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/reader96/`.

These are **section 7 drafts** (ways of taking a drug, compared); they go to the senior author before anything is published. Besides each number, check four things:
- each argument is given as the authors' own, not as fact;
- interests and funding are reported exactly as printed;
- every comparison names its comparison group as the paper does;
- nothing reads as advice on how to use a product.

Do not open the first reader's files (`scratchpad/routes/reader90*`), the study cards in `data/study-cards/_incoming/`, or `data/claims/`.

**Final message:** under 120 words. Give how many tasks were confirmed, corrected, wrong-location and not-found, and any correction that changes a number or an attribution.
