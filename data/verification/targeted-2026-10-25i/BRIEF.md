# Second reading: nicotine withdrawal, the cocaine crash, and sleep on ADHD stimulants (AI reader 129, 2026-10-25)

You are a second reader for Pharmakon, an evidence library about drugs for the public and for people who use drugs. The project is `/home/claude/drug-encyclopedia`. AI reader 120 wrote 45 evidence anchors from seven papers, in eight claims about nicotine withdrawal and what helps, the crash and first weeks after cocaine, and sleep on ADHD stimulant medicines. You wrote none of them. Check each one at the place it cites.

First read `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/batch5/LEAN-RULES.md` and follow its hard rules.

**Tasks:** `data/verification/targeted-2026-10-25i/tasks.json` (n = 1 to 45).

**Output:** `data/verification/targeted-2026-10-25i/out_reader129.json`, with `"reader": "AI reader 129 (second reader)"` and `"date": "2026-10-25"`. Write it as you go.

Follow the method, verdicts and rules in `data/verification/targeted-2026-10-18o/BRIEF_a.md` (the sections "For each task", "Output" and "Rules"). Ignore its PDF table.

## Sources

Local PDFs only, with no browser and no web. All are under `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/`:

| reference | PDF | pages |
|---|---|---|
| hughes_2007 | `Nicotine/Hughes_2007_AbstinenceSymptomsTimeCourse..pdf` (two dots) | printed pages (a single-author narrative review) |
| haasova_2013 | `Nicotine/Haasova_2013_PhysicalActivityCravingsIPD_MA.pdf` | printed pages |
| west_2001 | `Nicotine/West_2001_OralNicotineWithdrawalSR.pdf` | printed pages |
| gawin_1986 | `Cocaine/Gawin_1986_AbstinenceSymptomatologyCrash.pdf` | printed pages; a scan: check numbers on page images |
| weddington_1990 | `Cocaine/Weddington_1990_ShortTermAbstinenceControlled.pdf` | printed pages; a scan: check numbers on page images |
| weiss_2006 | `Methylphenidate/Weiss_2006_MelatoninSleepHygieneRCT..pdf` (two dots) | printed pages |
| kidwell_2015 | `_Cross-cutting/Kidwell_2015_StimulantSleepYouthMA.pdf` | online-first, numbered 1 to 10: anchors cite those pages |

- Extract each PDF once with `pdftotext -layout` into `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/reader129/`.
- Render only the pages with the tables or figures you need, with `pdftoppm -r 110`. Check every negative number on a rendered page.
- Recompute any "editors' calculation". The first reader reports that Haasova's "standardized" effects are differences in scale points, that Weiss's effect size comes from uncontrolled, responder-only data, and that Weddington's figure shows a second mood rise its text calls steady: check each yourself.

## What else to check

Some of these claims are **section 7 drafts** (what people do themselves). They go to the senior author before anything is published. For every claim, besides each number, check that:
- the anchor says no more than the paper;
- every comparison names its comparison group as the paper does;
- funding and interests are reported as printed;
- nothing reads as advice, and doses appear only as study conditions (no amounts or timings of anything).

Then check the plain-language lines in `data/verification/targeted-2026-10-25i/plain.json` (question, short answer, main limit and 2 to 4 "how" points per claim). For each claim, add one entry to a `plain` list in your output: `{"claim_id", "verdict": "ok" | "fix", "fix": "<the corrected line, if any, as 'short: ...' or 'how 2: ...' joined by ' | '>", "note"}`. A line needs a fix if it says more than the paper, leaves out the comparison group, gives an amount or a timing, or reads as advice.

Do not open `data/claims/`, `data/study-cards/_incoming/`, or the first reader's files (`scratchpad/dayafter/r120/`, `scratchpad/dayafter/reader120_*`).

**Final message:** under 150 words. Give how many tasks were confirmed, corrected, wrong-location and not-found, the corrections that change a number, and the plain lines that need a fix.
