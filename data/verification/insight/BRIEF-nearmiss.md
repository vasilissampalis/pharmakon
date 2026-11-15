# Insight: the questions an answer does NOT answer (AI readers 707 and 708)

Pharmakon (project `/home/claude/pharmakon`; read `CLAUDE.md` there first) has a search, Insight, that finds the checked
answer for a question as people type it. It still confuses neighbours: asked "how can you die from alcohol" it offered
"How many deaths does alcohol cause worldwide?", which is about a count, not about how. We are teaching it the
difference with examples. You write the examples: for each answer, the questions that **sound close but that this
answer does not answer**.

## Input (your only input)

`data/verification/insight/answers-2026-11-15.json`: the site's answers (`id`, `pages`, `questions` as worded on the
site, `short`, `but`, `part`). Reader 707 writes the answers with `part` 1, reader 708 those with `part` 2. Leave out
the ids listed under `skip`. Street names are in `data/site/aliases.json`.

## For every answer, write

- `near`: **five** questions a real person might type into a search box or a forum that this answer does **not**
  answer, although a careless search would match them. Vary the kind:
  1. same drug, same subject, a different thing asked (how or why instead of how many; what it feels like instead of
     how common; is it risky instead of how it works; what to do instead of what happens);
  2. same drug, a neighbouring subject;
  3. the same question about a different drug;
  4. a wider or vaguer question of which this answer covers only a corner;
  5. a personal version that asks for something the answer does not give (is this normal, will I be ok, what helps).
  A reader of the answer's `short` and `but` must agree at once: "no, that is not what this answers".
- `more`: **three** further questions this answer **does** fully answer, typed as people type in a hurry: lowercase, a
  typo or missing letter, slang or a street name, no punctuation, or very short. Never wider than the answer.

At most 15 words each. Write them as people write, not as a textbook. Never write a question about amounts, doses, when
or how often to take a drug, how to take it, how to make it stronger, getting drugs, hiding use or beating a drug test
(the site handles those elsewhere): if an answer is only about such things, skip it and list its id under `skipped`.

## Output

`data/verification/insight/nearmiss_<N>.json`, saved every 40 answers:
`{"reader": "AI reader <N> (near-miss questions)", "date": "2026-11-15", "items": {"cl_...": {"near": ["...", "...",
"...", "...", "..."], "more": ["...", "...", "..."]}}, "skipped": []}`

Then check your own file: every answer of your part is there or skipped; five and three; no question repeats a site
question word for word; none asks about amounts, doses, timing of taking, routes, getting drugs or hiding use.

Commit and push after every 80 answers and at the end (add only your own file):
`cd /home/claude/pharmakon && git add data/verification/insight/nearmiss_<N>.json && git -c user.name="Claude (Anthropic), AI co-editor" -c user.email="noreply@anthropic.com" commit -q -m "Near-miss questions reader <N>" -m "Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>" -m "Claude-Session: https://claude.ai/code/session_018eyT8uK1o68qcrMFU7AWHn" && git push -q origin main`
(if refused: `git pull -q --rebase origin main`, then push again).

## Rules

- Open nothing else under `data/verification/` (the forum questions and their labels are the test set; your questions
  must not be copied from them) and nothing under `scripts/insight/`. Change no file except your output and your scratch
  folder `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/insight/r<N>/`. `python3 -I`.
  Person-first, non-judging words.
- If an automatic filter stops you, do not retry or reword that step: save what you have and finish.
- Final message under 100 words.
