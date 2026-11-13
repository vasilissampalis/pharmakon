# Second reading: opioid withdrawal and its treatment (AI reader 125, 2026-10-25)

You are a second reader for Pharmakon, an evidence library about drugs for the public and for people who use drugs. The project is `/home/claude/drug-encyclopedia`. AI reader 112 wrote 26 evidence anchors from three papers (two Cochrane reviews and one cohort study), in five claims about opioid withdrawal and the medicines used to manage it. You wrote none of them. Check each one at the place it cites.

First read `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/batch5/LEAN-RULES.md` and follow its rules for web papers, the browser and safety.

**Tasks:** `data/verification/targeted-2026-10-25d/tasks.json` (n = 1 to 26).

**Output:** `data/verification/targeted-2026-10-25d/out_reader125.json`, with `"reader": "AI reader 125 (second reader)"` and `"date": "2026-10-25"`. Write it as you go.

Follow the method, verdicts and rules in `data/verification/targeted-2026-10-18o/BRIEF_a.md` (the sections "For each task", "Output" and "Rules"). Ignore its PDF table and page notes.

## Sources

All three are free full texts in PubMed Central; each task's `source_read` gives the address. The Cochrane reviews are long: read only the sections and tables the tasks cite. Read them in the desktop app's built-in browser:
- open your own tab with `tabs_create` and pass its tabId on every browser call;
- open each paper once, save its text to `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/reader125/`, and search that copy;
- close your tab at the end.

Never open a PDF link, download a file or try a CAPTCHA. If the browser cannot be reached, stop and say so; never fetch pages with the shell. Where an anchor gives a review's illustrative risks (for example 'about 59 in 100'), check them against the review's summary of findings table.

## What else to check

These claims go on the site once you have checked them. Besides each number, check that:
- the anchor says no more than the paper;
- every comparison names its comparison group as the paper does;
- funding and interests are reported as printed;
- nothing reads as advice, and doses appear only as study conditions.

Then check the plain-language lines in `data/verification/targeted-2026-10-25d/plain.json` (question, short answer, main limit and 2 to 4 "how" points per claim). For each claim, add one entry to a `plain` list in your output: `{"claim_id", "verdict": "ok" | "fix", "fix": "<the corrected line, if any>", "note"}`. A line needs a fix if it says more than the paper, leaves out the comparison group, gives an amount or a timing, or reads as advice.

Do not open `data/claims/`, `data/study-cards/_incoming/`, or the first reader's files (`scratchpad/dayafter/r112/`, `scratchpad/dayafter/reader112_*`).

**Final message:** under 150 words. Give how many tasks were confirmed, corrected, wrong-location and not-found, the corrections that change a number, and the plain lines that need a fix.
