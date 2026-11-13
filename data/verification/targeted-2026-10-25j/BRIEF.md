# Second reading: sleeping pills: next-day driving, crashes and morning caffeine (AI reader 130, 2026-10-25)

You are a second reader for Pharmakon, an evidence library about drugs for the public and for people who use drugs. The project is `/home/claude/drug-encyclopedia`. AI reader 119 wrote 26 evidence anchors from three papers, in four claims about next-day driving after sleeping pills, crashes and falls, whether morning effects fade with nightly use, and morning caffeine. You wrote none of them. Check each one at the place it cites.

First read `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/batch5/LEAN-RULES.md` and follow its hard rules.

**Tasks:** `data/verification/targeted-2026-10-25j/tasks.json` (n = 1 to 26).

**Output:** `data/verification/targeted-2026-10-25j/out_reader130.json`, with `"reader": "AI reader 130 (second reader)"` and `"date": "2026-10-25"`. Write it as you go.

Follow the method, verdicts and rules in `data/verification/targeted-2026-10-18o/BRIEF_a.md` (the sections "For each task", "Output" and "Rules"). Ignore its PDF table.

## Sources

Local PDFs only, with no browser and no web. All are under `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/`:

| reference | PDF | pages |
|---|---|---|
| vermeeren_2004 | `Benzodiazepines/Vermeeren_2004_ResidualEffectsHypnotics.pdf` | printed pages (a narrative review) |
| fornaro_2024 | `Benzodiazepines/Fornaro_2024_ResidualDrivingNMA..pdf` (two dots before pdf) | accepted manuscript: anchors cite manuscript pages |
| johnson_1990 | `Benzodiazepines/Johnson_1990_MorningCaffeineAfterHypnotic.pdf` | printed pages |

- Extract each PDF once with `pdftotext -layout` into `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/reader130/`.
- Render only the pages with the tables or figures you need, with `pdftoppm -r 110`. Check every negative number on a rendered page.
- Recompute any "editors' calculation". The first reader reports misprinted triazolam figures in Fornaro 2024 and a negative reaction time in Johnson 1990: check them yourself.

## What else to check

Some of these claims are **section 7 drafts** (what people do themselves). They go to the senior author before anything is published. For every claim, besides each number, check that:
- the anchor says no more than the paper;
- every comparison names its comparison group as the paper does;
- funding and interests are reported as printed;
- nothing reads as advice, and doses appear only as study conditions (no amounts or timings of anything).

Then check the plain-language lines in `data/verification/targeted-2026-10-25j/plain.json` (question, short answer, main limit and 2 to 4 "how" points per claim). For each claim, add one entry to a `plain` list in your output: `{"claim_id", "verdict": "ok" | "fix", "fix": "<the corrected line, if any, as 'short: ...' or 'how 2: ...' joined by ' | '>", "note"}`. A line needs a fix if it says more than the paper, leaves out the comparison group, gives an amount or a timing, or reads as advice.

Do not open `data/claims/`, `data/study-cards/_incoming/`, or the first reader's files (`scratchpad/dayafter/r119/`, `scratchpad/dayafter/reader119_*`).

**Final message:** under 150 words. Give how many tasks were confirmed, corrected, wrong-location and not-found, the corrections that change a number, and the plain lines that need a fix.
