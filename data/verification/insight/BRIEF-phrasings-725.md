# Insight: ways of asking for the newest answers (AI reader 725)

Pharmakon (project `/home/claude/pharmakon`; read `CLAUDE.md` there first, above all "Demand first") has a search,
Insight, that finds the checked answer for a question as people type it. It matches meaning, so it works best when each
answer carries the different ways real people ask for it. Eighteen of the newest answers, which answer some of the
most-asked questions, do not have them yet. You write them.

## Input (your only input)

`data/verification/insight/answers-725.json`: 18 answers (`id`, `pages`, `questions` as worded on the site, `short`,
`but`). Street names are in `data/site/aliases.json`. Read `data/verification/insight/BRIEF-phrasings.md` (section "What
to write") and `data/verification/insight/BRIEF-nearmiss.md` (section "For every answer, write") for the rules and the
kinds of wording; they apply here word for word.

## What to write

- For **every** answer, `more`: **six** ways a person would type a question that this answer fully answers (the six
  forms of BRIEF-phrasings.md: casual, worried, myth check, short fragment, a street or other name, any other natural
  wording). Each must be fully answered by the answer's `short` and `but`: never wider than the answer.
- For the answer marked `new` (`cl_mdma_empathy`) also: three more wordings typed in a hurry (so nine in `more`), and
  `near`: **five** questions that sound close but that this answer does **not** answer (the five kinds of
  BRIEF-nearmiss.md).
- At most 15 words each, as people write. Never a wording about amounts, doses, when or how often to take a drug, how
  to take it, how to make it stronger, getting drugs, hiding use or beating a drug test.

## Output

`data/verification/insight/nearmiss_725.json`:
`{"reader": "AI reader 725 (ways of asking)", "date": "2026-11-15", "items": {"cl_...": {"near": [], "more": ["...",
"...", "...", "...", "...", "..."]}}, "skipped": []}` (`near` is an empty list except for the new answer).

Check your own file: 18 answers; six wordings each (nine and five for the new one); none repeats a site question word
for word; none asks about amounts, doses, timing of taking, routes, getting drugs or hiding use.

Commit and push only your own file:
`cd /home/claude/pharmakon && git add data/verification/insight/nearmiss_725.json && git -c user.name="Claude (Anthropic), AI co-editor" -c user.email="noreply@anthropic.com" commit -q -m "Ways of asking: reader 725" -m "Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>" -m "Claude-Session: https://claude.ai/code/session_018eyT8uK1o68qcrMFU7AWHn" -- data/verification/insight/nearmiss_725.json && git push -q origin main`
(if the push is refused because the remote moved, wait a few seconds and push again; do not rebase or stash).

## Rules

- Open nothing else under `data/verification/` (the forum questions and their labels are the test set; your wordings
  must not be copied from them) and nothing under `scripts/insight/`. Change no file except your output. `python3 -I`.
  Person-first, non-judging words.
- If an automatic filter stops you, do not retry or reword that step: save what you have and finish.
- Final message under 100 words.
