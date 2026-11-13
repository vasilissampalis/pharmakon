# Second reading: MDMA, LSD, PCP, cannabis and synthetic cannabis, the day after (AI reader 131, 2026-10-25)

You are a second reader for Pharmakon, an evidence library about drugs for the public and for people who use drugs. The project is `/home/claude/drug-encyclopedia`. AI reader 121 wrote 39 evidence anchors from eight papers, in 11 claims about the day after ecstasy, the mid-week low, LSD the next day, long psychosis after PCP, how long THC impairs driving, cannabis and sleep, cannabis hyperemesis treatment, and synthetic cannabis. You wrote none of them. Check each one at the place it cites.

First read `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/batch5/LEAN-RULES.md` and follow its hard rules.

**Tasks:** `data/verification/targeted-2026-10-25k/tasks.json` (n = 1 to 39).

**Output:** `data/verification/targeted-2026-10-25k/out_reader131.json`, with `"reader": "AI reader 131 (second reader)"` and `"date": "2026-10-25"`. Write it as you go.

Follow the method, verdicts and rules in `data/verification/targeted-2026-10-18o/BRIEF_a.md` (the sections "For each task", "Output" and "Rules"). Ignore its PDF table.

## Sources

Local PDFs only, with no browser and no web. All are under `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/`:

| reference | PDF | pages |
|---|---|---|
| curran_1997 | `MDMA/Curran_1997_WeekendHighMidweekLow..pdf` (two dots) | printed pages; a scan: check numbers on page images |
| scott_2013 | `MDMA/Scott_2013_SubacuteMoodRiskFactors.pdf` | printed pages |
| wiessner_2022 | `LSD/Wiessner_2022_AfterglowHangoverCognition24h.pdf` | printed pages |
| rainey_1975 | `PCP/Rainey_1975_ProlongedPsychosisThreeCases.pdf` | printed pages; a scan, and the article starts after the end of another |
| mccartney_2021 | `Cannabis/McCartney_2021_THCImpairmentDurationMA.pdf` | printed pages |
| velzeboer_2025 | `Cannabis/Velzeboer_2025_SleepArchitectureMA.pdf` | printed pages |
| sabbineni_2024 | `Cannabis/Sabbineni_2024_CHSCapsaicinDopamineAntagonistsSR..pdf` (two dots) | printed pages |
| winstock_2013 | `Synthetic-cannabinoids/Winstock_2013_SyntheticVsNaturalGlobalSample.pdf` | article in press, numbered 1 to 6 |

- Extract each PDF once with `pdftotext -layout` into `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/reader131/`.
- Render only the pages with the tables or figures you need, with `pdftoppm -r 110`. Check every negative number on a rendered page.
- Recompute any "editors' calculation". The first reader reports a borderline P value in Curran 1997, effect sizes with the wrong sign in Velzeboer 2025's text against its figures, and a table in McCartney 2021 that contradicts its abstract: check each yourself.

## What else to check

For every claim, besides each number, check that:
- the anchor says no more than the paper;
- every comparison names its comparison group as the paper does;
- funding and interests are reported as printed;
- nothing reads as advice, and doses appear only as study conditions (no amounts or timings of anything).

Then check the plain-language lines in `data/verification/targeted-2026-10-25k/plain.json` (question, short answer, main limit and 2 to 4 "how" points per claim). For each claim, add one entry to a `plain` list in your output: `{"claim_id", "verdict": "ok" | "fix", "fix": "<the corrected line, if any, as 'short: ...' or 'how 2: ...' joined by ' | '>", "note"}`. A line needs a fix if it says more than the paper, leaves out the comparison group, gives an amount or a timing, or reads as advice.

Do not open `data/claims/`, `data/study-cards/_incoming/`, or the first reader's files (`scratchpad/dayafter/r121/`, `scratchpad/dayafter/reader121_*`).

**Final message:** under 150 words. Give how many tasks were confirmed, corrected, wrong-location and not-found, the corrections that change a number, and the plain lines that need a fix.
