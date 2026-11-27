# Notes for the expansion plan (Fable 5.2, 27 November 2026), gathered by the editor overnight

Read with `docs/STATUS.md` (the entry of 26 November evening holds the senior author's words for this plan) and
`docs/OPENROUTER.md`. Everything here was measured or read on the night of 26 to 27 November.

## What he asked for, in his words

- 19:26: "our ai should create new pages on the website if there is not an already predicated page/section for what people
  search and it should automatically find pictures for them and in general enrichen the site perfectly and understand what is
  missing in the best token-saving manner possible while doing perefect work. our site should be endlessly expanding and we
  should be careful about token saving but also preserve perfect quality"
- 19:48: "it should enrichen every existing section too if it's relevant. Even myth and facts right? But it should be able to
  last the whole month with user questions always being answered the best way possible and many answers a month being
  answered and all that"
- 21:39: "Make the choice that absolutely has the best results"; "The best and fastest results"; "People don't like waiting
  at all and want outmost accuracy"
- 21:41: "the myth and fact questions have to be based on actual searches of what people really want to learn either in
  forums or in the site searches. But we still want the tokens to reach their limit when the month absolutely ends not
  before that"

## How he wants answers written (his comments of 12 and 13 November on his to-do page, kept in its database)

Any text the system writes by itself should meet these, not only the checked answers:

- "people live very fast paced nowadays i don't think nobody would read all this"; "all these numbers ... and details are too
  difficult for humans to absorb and it gets tiring and they could lose interest"; "nobody will read all this ... not even
  scientists so i wonder if we should keep a simpler format to convey info".
- "i want a human view of finding info significant written in a way that keeps only what's significant to know!"
- "so did take lutein or stopping them help? you didn't even say!" (answer the question asked, plainly).
- "what is the drug even! i never want you not to make clear what drug you are talking about!"
- On an answer about NAC for hangovers: "people don't know what N-acetylcysteine (NAC) pills are which is already confusing
  and the fact that they were not even helpful makes this unnecessary" (an answer nobody needs is not worth writing).
- The lines he accepted then ran to about 70 to 140 words for the short answer, its But and two to four points together.
  Last night's first lines for the section 7 answers ran to about 220 to 280: they were written again shorter
  (`data/verification/s7-simple-2026-11-27/`).

## The money (read at 00:11 Athens, 27 November)

- OpenRouter credit left: $9.61 of $10 bought; spent in November: $0.41 (exams $0.35, the lane's own list $0.05, visitors'
  questions $0). The workspace budget ($10 a month) resets on 1 December; the credit does not refill by itself (automatic
  top-up is off).
- Gemini (free tier): about 1,000 calls on 26 November, $0. OpenRouter calls on 26 November: about 1,050 (most of them the
  exams).
- Pacing now (`data/auto/lane/pay.json`): $9.50 a month for the lane, at most the month's pot divided by its days in one day
  (`even`), and never more than the credit left (`follow_credit`). His wish to spend exactly to the month's end needs one
  answer from him first: does he buy credit every month, or was the $10 once?

## The second reader

- Timed exams (exam-0026): GPT-6 Luna caught 32 of 35 wrong sentences (both sittings) and stopped 20 to 22 of 73 good ones,
  median 4.0 seconds a call; Claude Haiku 5.5 caught 22 and 24, stopped 9 and 11, 5.3 s; gpt-oss-120b caught 16 and 17,
  stopped 6 and 8, 4.6 s. Luna is asked first in every team since 00:40 (decision 46). It stops about 1 good sentence in 4,
  so more drafts are written again: count that in the token budget.

## Why the lane wrote no answer (answers made 24 to 26 November, 119 with none)

- 23: the second reader did not accept the answer.
- 35: no source that could be read gave a finding (23 of them with sources that could not be fetched at that moment).
- 8: not enough sources (one review read in full, or one official page, or two studies, is the floor).
- 10 more: drafts broken by the code's gates or not accepted by a further reader; 3: the stricter bar for dying, overdose
  or mixing not met.
- So the gaps are mostly sources, then drafts that the readers refuse; a better writer helps the second, the finders the
  first.

## What the editor found in the answers the system published (19 held on the night of 27 November)

Held, each with what to say for its next version (`data/auto/held.json`): copying a source's sentence as the site's own
(the lane now refuses more than 15 words in a row, `lane.copied_run`); ways of taking a drug compared; animal findings said
of people; a review's report of other researchers' proposal said as fact; an article proposing a therapy called a review
and its summary of other studies called its finding; an effect no source states; two settings (anaesthesia in hospital,
heavy daily use) set against each other as a disagreement; a comparison said without what it was compared with; a short
answer that does not answer plainly; empty How points. A design that writes more must keep this reading possible, or make
the gates catch these by themselves.

## Other facts for the plan

- The site's checked layer: 434 claims (46 in section 7, 8 approved), 433 sets of plain lines, 531 myth-or-fact items, 146
  quick questions, 742 study cards, 856 references. The machine lane: 321 answer records.
- Insight: 109 answers had no ways of asking written for them (58 of them checked answers); reader 809 writes them for the
  20 newest published ones tonight. New answers need them to be found by people's own words.
- GitHub's schedule starts the Auto run only every few hours (255 scheduled runs ever, some days none for hours); the site's
  server starts it when a question is sent, and a run that worked starts the next while work is left. At night, with no
  questions sent, nothing runs unless something starts it.
- The papers people would most need for the checked lane are listed for him on his to-do page (41, from the questions asked
  most); his computer was off overnight, so papers already in his folder could not be read (three section 7 answers wait
  for five of them: `data/verification/s7-restore/PLAN.md`).

## Seen after midnight (27 November, 02:00 to 03:00 Athens), with GPT-6 Luna asked first

- The lane, started after midnight UTC, found 199 listed questions due and chained its runs by itself (`tick.py again`).
  Of its first 14 tries, 2 were published (mescaline and tolerance: stands; barbiturates and tolerance: held), the rest
  gave no answer (sources, mostly).
- A pattern the gates do not catch: a writer says a review "found" something that the review says in passing, as
  background (the barbiturates answer rested on one background sentence in the abstract of a review of natural sleep
  aids). Luna accepted it. A gate could tell background from findings by where the passage stands (an abstract's opening,
  an introduction) and refuse "found" for those.
