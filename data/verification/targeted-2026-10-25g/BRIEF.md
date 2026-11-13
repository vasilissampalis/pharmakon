# Second reading: loperamide, opioid constipation, methadone between doses, poppers and the eyes (AI reader 127, 2026-10-25)

You are a second reader for Pharmakon, an evidence library about drugs for the public and for people who use drugs. The project is `/home/claude/drug-encyclopedia`. AI reader 122 wrote 35 evidence anchors from four papers, in seven claims. You wrote none of them. Check each one at the place it cites.

First read `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/batch5/LEAN-RULES.md` and follow its hard rules.

**Tasks:** `data/verification/targeted-2026-10-25g/tasks.json` (n = 1 to 35).

**Output:** `data/verification/targeted-2026-10-25g/out_reader127.json`, with `"reader": "AI reader 127 (second reader)"` and `"date": "2026-10-25"`. Write it as you go.

Follow the method, verdicts and rules in `data/verification/targeted-2026-10-18o/BRIEF_a.md` (the sections "For each task", "Output" and "Rules"). Ignore its PDF table.

## Sources

Local PDFs only, with no browser and no web. All are under `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/`:

| reference | PDF | pages |
|---|---|---|
| lee_2019 | `_Cross-cutting/Lee_2019_LoperamideMisuseWithdrawal.pdf` | online-first, numbered 1 to 6 after a cover page |
| nee_2018 | `Prescription-opioids/Nee_2018_OpioidConstipationTreatmentsMA.pdf` | accepted manuscript: anchors cite PDF pages |
| dyer_1999 | `Methadone-Buprenorphine/Dyer_1999_InterdoseWithdrawalPKPD.pdf` | printed journal pages |
| bartolo_2023 | `Alkyl-nitrites-and-inhalants/Bartolo_2023_PoppersMaculopathySR..pdf` (two dots before pdf) | online-first, numbered 1 to 9 after a cover page |

- Extract each PDF once with `pdftotext -layout` into `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/reader127/`.
- Render only the pages with the tables or figures you need, with `pdftoppm -r 110`. Check every negative number on a rendered page.
- Recompute any "editors' calculation". The first reader reports three errors in the papers, which you should check yourself: Nee's alvimopan total and side-effect ratios, Dyer's key P value, and Bartolo's table total.

## What else to check

Three of these claims are **section 7 drafts** (what people do themselves: loperamide for withdrawal, shop laxatives, stopping poppers or taking lutein). They go to the senior author before anything is published. For every claim, besides each number, check that:
- the anchor says no more than the paper;
- every comparison names its comparison group as the paper does;
- funding and interests are reported as printed;
- nothing reads as advice, and doses appear only as study conditions (no amounts or timings of loperamide, methadone or anything else).

Then check the plain-language lines in `data/verification/targeted-2026-10-25g/plain.json` (question, short answer, main limit and 2 to 4 "how" points per claim). For each claim, add one entry to a `plain` list in your output: `{"claim_id", "verdict": "ok" | "fix", "fix": "<the corrected line, if any, as 'short: ...' or 'how 2: ...' joined by ' | '>", "note"}`. A line needs a fix if it says more than the paper, leaves out the comparison group, gives an amount or a timing, or reads as advice.

Do not open `data/claims/`, `data/study-cards/_incoming/`, or the first reader's files (`scratchpad/dayafter/r122/`, `scratchpad/dayafter/reader122_*`).

**Final message:** under 150 words. Give how many tasks were confirmed, corrected, wrong-location and not-found, the corrections that change a number, and the plain lines that need a fix.
