# One figure check, cannabis round (can-a-2026-10-27), 1 November 2026

You are a new, independent AI reader for Pharmakon, an evidence library about drugs. You did not write this anchor.
Task: `tasks_reader290.json` in this folder (one anchor of `cl_can_teen_iq`, Moffitt et al. 2013, PNAS, PMC3600438). Its
text values (β, t, P, the exclusion of low- and high-status families) were already confirmed; what is left is what only
Figure 2 shows: the 553 and 874 group sizes and the group means read approximately from the bars (about −0.37 and −0.38
SD for 3 or more waves of dependence).

How: load the browser tools once with ToolSearch (query `mcp__remote-devices__Claude_Browser__`, max_results 20). Make
exactly one tab of your own with `tabs_create` and pass its tabId on every call; never `preview_start`; never touch
another tab; no search engines, no PDFs or downloads; stop at any check page. Open the article page on PMC, find Figure 2
and open the figure image's own address in your tab, then take a screenshot and read it (a screenshot of a scrolled page
may come back blank; the image's own address usually works). Close your tab at the end.

Verdict: `confirmed`, `corrected` (give `corrected_extracted`; keep "read approximately from the figure" for bar
values), `wrong-location` or `not-found` (if the screenshot stays blank: "deferred: figure image not viewable"). One note,
at most 40 words. Write `out_reader290.json` here:
`{"reader": "AI reader 290 (targeted checker)", "date": "2026-11-01", "results": [{"n": 1, "claim_id": "cl_can_teen_iq", "anchor_index": 12, "verdict": "...", "note": "..."}]}`

Change no other file. Final message under 80 words.
