# Insight: ways of asking for the newest answers (AI reader 814, 27 November 2026)

Pharmakon (project `/home/claude/pharmakon`; read `CLAUDE.md` there first, above all "Demand first") has a search,
Insight, that finds the checked answer for a question as people type it. It matches meaning, so it works best when each
answer carries the different ways real people ask for it. Thirty-seven answers in section 7 (practical safety: vaping and smoking, edibles,
hangovers and other everyday questions) wait for the senior author's approval and have none yet. You write them, so
that people find them by their own words as soon as he approves them.

## Input (your only input)

`data/verification/insight/answers-814.json`: 37 answers (`id`, `pages`, `questions` as worded on the site, `short`,
`but`). Street names are in `data/site/aliases.json`. Read `data/verification/insight/BRIEF-phrasings.md` (section "What
to write") and `data/verification/insight/BRIEF-nearmiss.md` (section "For every answer, write") for the rules and the
kinds of wording; they apply here word for word.

## What to write

- For **every** answer, `more`: **six** ways a person would type a question that this answer fully answers (the six
  forms of BRIEF-phrasings.md: casual, worried, myth check, short fragment, a street or other name, any other natural
  wording). Each must be fully answered by the answer's `short` and `but`: never wider than the answer.
- These answers are about practical safety, so take extra care: a wording asks what the answer answers ("is vaping
  safer than smoking", "do edible labels get the THC right"), never which way of taking a drug is stronger or how to
  get a stronger effect, how much to take, or how to use.
- At most 15 words each, as people write. Never a wording about amounts, doses, when or how often to take a drug, how
  to take it, how to make it stronger, getting drugs, hiding use or beating a drug test.

## Output

`data/verification/insight/nearmiss_814.json`:
`{"reader": "AI reader 814 (ways of asking)", "date": "2026-11-27", "items": {"cl_...": {"near": [], "more": ["...",
"...", "...", "...", "...", "..."]}}, "skipped": []}` (`near` is an empty list).

Check your own file: 37 answers; six wordings each; none repeats a site question word
for word; none asks about amounts, doses, timing of taking, routes, getting drugs or hiding use.

Commit and push only your own file:
`cd /home/claude/pharmakon && git add data/verification/insight/nearmiss_814.json && git -c user.name="Claude (Anthropic), AI co-editor" -c user.email="noreply@anthropic.com" commit -q -m "Ways of asking: reader 814" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" -m "Claude-Session: https://claude.ai/code/session_018eyT8uK1o68qcrMFU7AWHn" -- data/verification/insight/nearmiss_814.json && git push -q origin main`
(if the push is refused because the remote moved, wait a few seconds and push again; do not rebase or stash).

## Rules

- Open nothing else under `data/verification/` (the forum questions and their labels are the test set; your wordings
  must not be copied from them) and nothing under `scripts/insight/`. Change no file except your output. `python3 -I`.
  Person-first, non-judging words.
- If an automatic filter stops you, do not retry or reword that step: save what you have and finish.
- Final message under 100 words.
