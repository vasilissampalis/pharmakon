# Targeted checks, round 3 (web papers), Alcohol round (alc-a-2026-10-27), 31 October 2026

Everything in `data/verification/alc-a-2026-10-27/targeted3/BRIEF.md` applies, except where to read: your five anchors
come from three papers read as web full texts (Holmes et al., 2014, PMC4091648; Rumgay et al., 2021, PMC8324483;
Roerecke et al., 2019, PMC6776700, an author manuscript). Read them in the app's browser:

- Load the browser tools once with ToolSearch, query `mcp__remote-devices__Claude_Browser__` (max_results 20).
- Make one tab of your own with `tabs_create`, pass its tabId on every call, open only
  `https://pmc.ncbi.nlm.nih.gov/articles/PMC.../` pages (and their figure and table pages), and close your tab at the
  end. Never use or close any other tab; never use `preview_start`.
- No search engines, no PDFs or downloads; if a page shows a check (a CAPTCHA or "are you a robot"), stop and give
  `not-found` with the note "deferred: web source not reachable".
- Figure values: read them in the figure as PMC shows it (open the figure page; `get_page_text` and `read_page` give the
  text; take a screenshot only when the values are drawn, not printed). Say in the note how you read each value.

Tasks: `data/verification/alc-a-2026-10-27/targeted3/tasks_reader<N>.json`. Output:
`data/verification/alc-a-2026-10-27/targeted3/out_reader<N>.json`, `"reader": "AI reader <N> (second reader)"`,
`"date": "2026-10-31"`.
