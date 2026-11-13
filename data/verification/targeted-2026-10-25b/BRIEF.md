# Second reading: the day after, alcohol (AI reader 113, 2026-10-25)

You are a second reader for Pharmakon, an evidence library about drugs for the public and for people who use drugs. The project is `/home/claude/drug-encyclopedia`. AI reader 110 wrote 40 evidence anchors from eight papers, in eight alcohol claims about hangovers and the day after drinking. You wrote none of them. Check each one at the place it cites.

First read `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/batch5/LEAN-RULES.md` and follow its rules for web papers, the browser and safety.

**Tasks:** `data/verification/targeted-2026-10-25b/tasks.json` (n = 1 to 40).

**Output:** `data/verification/targeted-2026-10-25b/out_reader113.json`, with `"reader": "AI reader 113 (second reader)"` and `"date": "2026-10-25"`. Write it as you go.

Follow the method, verdicts and rules in `data/verification/targeted-2026-10-18o/BRIEF_a.md` (the sections "For each task", "Output" and "Rules"). Ignore its PDF table and page notes.

## Sources

All eight are free full texts in PubMed Central; each task's `source_read` gives the address. Read them in the desktop app's built-in browser:
- open your own tab with `tabs_create` and pass its tabId on every browser call;
- open each paper once, save its text to `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/reader113/`, and search that copy;
- close your tab at the end.

Never open a PDF link, download a file or try a CAPTCHA. If the browser cannot be reached, stop and say so; never fetch pages with the shell. If PMC links a correction to the Coppersmith 2021 paper, read it too.

## What else to check

Most of these claims are **section 7 drafts** (whether something people do reduces a hangover). They go to the senior author before anything is published. Besides each number, check that:
- the anchor says no more than the paper;
- every comparison names its comparison group as the paper does;
- funding and interests are reported as printed;
- nothing reads as advice, and doses appear only as study conditions.

Then check the plain-language lines in `data/verification/targeted-2026-10-25b/plain.json` (question, short answer, main limit and 2 to 4 "how" points per claim). For each claim, add one entry to a `plain` list in your output: `{"claim_id", "verdict": "ok" | "fix", "fix": "<the corrected line, if any>", "note"}`. A line needs a fix if it says more than the paper, leaves out the comparison group, gives an amount or a timing, or reads as advice.

Do not open `data/claims/`, `data/study-cards/_incoming/`, or the first reader's files (`scratchpad/dayafter/r110/`, `scratchpad/dayafter/reader110_*`).

**Final message:** under 150 words. Give how many tasks were confirmed, corrected, wrong-location and not-found, the corrections that change a number, and the plain lines that need a fix.
