# Which Myth or fact? cards would a common person care about? (AI raters 699 and 700, each blind to the other)

Pharmakon (project `/home/claude/pharmakon`; read `CLAUDE.md` there first, above all "Demand first") is a drug
encyclopedia for people who use drugs and people curious about them. Its start page and drug pages have "Myth or fact?"
decks: a statement, the reader taps Myth or Fact, then sees a short explanation. The senior author and people he showed
it to found most cards dull. You rate every card, so the site can show only the good ones, best first.

## What the senior author said (15 November 2026)

"i think the myth and fact questions less than half of them are interesting for most users. they feel a lot like an
academic test and most people get confused while reading them". Cards he found **interesting**:
- "In ketamine lab studies, hallucinations mostly meant seeing things that were not there."
- "In one big survey, people sought emergency treatment more often after LSD than after magic mushrooms."
- "In a driving simulator, cannabis and alcohol together made lane weaving worse than either one alone."

A card he found **boring**: "At one drug-checking service, nobody who brought a sample with a newer benzodiazepine
expected it to be there." And: "some people may also understand xanax or valium and not benzodiazepine". "we have to give
out information the common person would find more interesting"; he wants cards based on what people talk and ask about
on forums, and "nice interesting myth busts" in the spirit of Carl Hart (drugs, addiction, wellbeing, policy: what
people believe against what the research found).

## Your input

`data/verification/quiz/interest-2026-11-15/tasks.json`: 396 cards (`n`, `key`, `deck` = the drug or topic, `statement`,
`answer` Myth or Fact, `why` = the explanation shown after the tap). This file is your only input.

## Rate each card as a common person would meet it (not as a scientist)

Picture someone scrolling on a phone: uses or is curious about drugs, did not study science, reads quickly.

- `interest` 1 to 5: would they care, and want to tell a friend?
  5 = "wow, I'd tell a friend tonight"; 4 = "good to know"; 3 = "fine, but I would not miss it"; 2 = "why are you
  telling me this"; 1 = "this is about a study or a service, not about anything in my life".
  High: it is about something people do, feel, fear or argue about (driving, sex, sleep, the comedown, mixing, memory,
  getting hooked, fake pills, how long it shows in tests, what a trip is like, what the law did); it surprises; it
  overturns something people believe. Low: it is about how a study or service was run, a narrow group, a count nobody
  asked for, a clinical or policy detail with no "so what" for the reader.
- `clear` 1 to 5: is it understood on first read by someone who did not finish school?
  5 = instantly; 3 = had to read twice; 1 = could not say what it claims. Marks against: a word most people do not use
  (benzodiazepine instead of benzos such as Xanax or Valium; "synthetic cathinones" instead of bath salts or mephedrone;
  "serotonergic"), a double negative, a "nobody who … expected …" construction, two claims in one, a number that cannot
  be pictured.
- `test_feel` true or false: does it read like an exam question about a study rather than a thing about a drug?
- `guessable` true or false: can the reader form a real guess (it is neither obvious nor a coin toss about an unknowable
  number)?
- `rewrite` (optional, at most 22 words): only when the fact is worth keeping (you would give the fact itself 4 or 5)
  but the wording loses people. Say **exactly the same fact** with the same truth value in everyday words, with common
  names where they exist. No new fact, no number changed, nothing dropped that the statement needs to stay true (a
  "lab study", "survey", "in rats", "people said" must stay). It will be checked blind against the evidence before use.
- `note` (optional, at most 12 words).

Use the whole scale. If fewer than half are 4 or 5, say so with your numbers: do not be kind to the cards.

## Output

`data/verification/quiz/interest-2026-11-15/ratings_<N>.json`, saved every 50 cards:
`{"rater": "AI rater <N> (card interest)", "date": "2026-11-15", "ratings": [{"n": 1, "key": "...", "interest": 4,
"clear": 5, "test_feel": false, "guessable": true, "rewrite": "", "note": ""}]}`

Commit and push after every 100 cards and at the end (add only your own file):
`cd /home/claude/pharmakon && git add data/verification/quiz/interest-2026-11-15/ratings_<N>.json && git -c user.name="Claude (Anthropic), AI co-editor" -c user.email="noreply@anthropic.com" commit -q -m "Card interest rater <N>" -m "Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>" -m "Claude-Session: https://claude.ai/code/session_018eyT8uK1o68qcrMFU7AWHn" && git push -q origin main`
(if refused: `git pull -q --rebase origin main`, then push again).

## Rules

- Blind: open no other rater's file and nothing else under `data/`. Change no file except your output and your scratch
  folder `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/interest/r<N>/`. `python3 -I`.
- Never write a rewrite about amounts, doses, timing of taking a drug, routes compared for strength, or reaching or
  strengthening effects. If an automatic filter stops a step, do not retry or reword it: save what you have and finish.
- Final message under 150 words: how many cards at each interest level, how many you would keep (interest ≥ 4 and
  clear ≥ 4), the three best and three worst (by `n`), and the most common reason cards fail.
