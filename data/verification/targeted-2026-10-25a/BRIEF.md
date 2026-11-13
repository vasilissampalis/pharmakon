# Second reading: one new anchor from the Callaghan 2013 supplement (AI reader 108, 2026-10-25)

You are a second reader for Pharmakon, an evidence library about drugs. The project is `/home/claude/drug-encyclopedia`. The AI co-editor added one evidence anchor to `cl_can_smoked_cancer` from the supplement of Callaghan et al. (2013). You wrote none of it. Check it at the place it cites.

**Task:** `data/verification/targeted-2026-10-25a/tasks.json` (n = 1).

**Output:** `data/verification/targeted-2026-10-25a/out_reader108.json`, with `"reader": "AI reader 108 (second reader)"` and `"date": "2026-10-25"`.

Follow the method, verdicts and rules in `data/verification/targeted-2026-10-18o/BRIEF_a.md` (the sections "For each task" and "Rules"). Ignore its PDF table and its browser steps.

**Source:** a local Word file, no browser and no web: `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/Cannabis/Callaghan_2013_Supplement.docx`. Read its text from `word/document.xml` with Python's zipfile into `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/reader108/`. Check every count and hazard ratio in the anchor against the table, and that the sum the claim relies on (men who used cannabis but no tobacco: 678, with one lung cancer) is right.

This is a **section 7 draft**; it goes to the senior author before anything is published. Check that the anchor says no more than the table, and names its comparison group as the table does.

Also check this sentence, now in the claim's statement, against the same table, and say in your note whether it says no more than the table shows: "in the paper's supplementary table, the 678 men who reported using cannabis but no tobacco had one lung cancer between them (in the 216 who had used cannabis once), so no hazard ratio could be estimated for men who had used cannabis more than once without tobacco."

Do not open `data/claims/` or any other file. **Final message:** under 80 words.
