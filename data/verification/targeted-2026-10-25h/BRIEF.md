# Second reading: alcohol, hangover mood and sleep, and caffeine (AI reader 128, 2026-10-25)

You are a second reader for Pharmakon, an evidence library about drugs for the public and for people who use drugs. The project is `/home/claude/drug-encyclopedia`. AI reader 119 wrote 41 evidence anchors from five papers, in eight claims about hangover mood, alcohol and sleep, water, caffeine and sleep, and caffeine-withdrawal headache. You wrote none of them. Check each one at the place it cites.

First read `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/batch5/LEAN-RULES.md` and follow its hard rules.

**Tasks:** `data/verification/targeted-2026-10-25h/tasks.json` (n = 1 to 41).

**Output:** `data/verification/targeted-2026-10-25h/out_reader128.json`, with `"reader": "AI reader 128 (second reader)"` and `"date": "2026-10-25"`. Write it as you go.

Follow the method, verdicts and rules in `data/verification/targeted-2026-10-18o/BRIEF_a.md` (the sections "For each task", "Output" and "Rules"). Ignore its PDF table.

## Sources

Local PDFs only, with no browser and no web. All are under `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/`:

| reference | PDF | pages |
|---|---|---|
| rothman_2026 | `Alcohol/Rothman_2026_HangoverNegativeAffectSR.pdf` | printed pages |
| gardiner_2025 | `Alcohol/Gardiner_2025_AlcoholSubsequentSleepMA.pdf` | journal pre-proof: anchors cite PDF pages; it has no figures |
| mackus_2024 | `Alcohol/Mackus_2024_HangoverDehydrationWater.pdf` | printed pages |
| gardiner_2023 | `Caffeine/Gardiner_2023_CaffeineSubsequentSleepMA..pdf` (two dots before pdf) | printed pages |
| hampl_1995 | `Caffeine/Hampl_1995_PerioperativeCaffeineHeadacheRCT.pdf` | printed pages; text extraction is poor, so check numbers on page images |

- Extract each PDF once with `pdftotext -layout` into `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/reader128/`.
- Render only the pages with the tables or figures you need, with `pdftoppm -r 110`. Check every negative number on a rendered page.
- Recompute any "editors' calculation". The first reader reports an impossible standard deviation and a wrong unit in Hampl 1995: check them yourself.

## What else to check

Some of these claims are **section 7 drafts** (what people do themselves). They go to the senior author before anything is published. For every claim, besides each number, check that:
- the anchor says no more than the paper;
- every comparison names its comparison group as the paper does;
- funding and interests are reported as printed;
- nothing reads as advice, and doses appear only as study conditions (no amounts or timings of anything).

Then check the plain-language lines in `data/verification/targeted-2026-10-25h/plain.json` (question, short answer, main limit and 2 to 4 "how" points per claim). For each claim, add one entry to a `plain` list in your output: `{"claim_id", "verdict": "ok" | "fix", "fix": "<the corrected line, if any, as 'short: ...' or 'how 2: ...' joined by ' | '>", "note"}`. A line needs a fix if it says more than the paper, leaves out the comparison group, gives an amount or a timing, or reads as advice.

Do not open `data/claims/`, `data/study-cards/_incoming/`, or the first reader's files (`scratchpad/dayafter/r119/`, `scratchpad/dayafter/reader119_*`).

**Final message:** under 150 words. Give how many tasks were confirmed, corrected, wrong-location and not-found, the corrections that change a number, and the plain lines that need a fix.
