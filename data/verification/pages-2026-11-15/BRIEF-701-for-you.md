# "If it gets too much": what you can do yourself (first reader 701; second reader 702)

Read `BRIEF-common.md` in this folder first. Each drug page has a section "If it gets too much". Today every line in
it is about helping someone else ("If they're anxious or paranoid, talk calmly…"; see `data/site/stay-safer.json` →
`signs`, nine drug families). The senior author (15 November 2026): "we should not just write about what to do if it is
too much for another person but what to do yourself if it's too much for you. going or calling the hospital should be
the last on the list like a last resort everything else is things you can do to yourself when it's too much for you or
to others when it's too much for others ... we have to begin with what users find most useful ... we don't want to freak
people out ... we have to give objective knowledge".

## Reader 701

For each of the nine families (Opioids, Stimulants, Entactogens, Classic psychedelics, Dissociatives, Cannabinoids,
Depressants, Inhalants, Atypical psychedelics), write the lines for **"For you"**: what a person can do themselves when
the drug feels like too much (too high, anxious, panicky, a difficult trip, too hot, feeling sick, heart racing, too
sedated), as the allowed publishers say it to the person directly or about them. Start from the pages the family's
existing lines already cite (their URLs are in `signs.<family>.*[].anchors`), then look for more among the allowed
publishers (for example HSE "Coping with bad trips or challenging experiences", Zendo Project, Fireside Project,
PsyCare UK, The Loop, DanceSafe, ADF, FRANK, The Level).
- Address the reader as "you". Three to six lines per family, most useful first: what calms, what to do with your body
  and the place you are in, who to turn to (a friend you trust; the welfare or harm reduction tent at an event), and
  what to avoid. Calm and matter-of-fact: these are things that pass for most people; say so only if a source says so.
- One last line per family may say when it is time to get medical help, in the source's own terms; it goes last.
- Where a family's sources say nothing to the person themselves (it may be so for Opioids or Inhalants), write the
  lines you can support and say in `gaps` what you looked for and did not find. Never fill a gap from your own knowledge.

Output `data/verification/pages-2026-11-15/for_you_701.json`:
`{"reader": "AI reader 701", "date": "2026-11-15", "families": {"<family>": {"self": [{"line": "...", "anchors":
[...]}], "gaps": "..."}}}`. Final message under 150 words: lines per family, publishers used, gaps.

## Reader 702 (and reader 718: the nine families are shared between two second readers)

Your families and your output file's name are in your instructions; the shape of the file is the one below, with your
own reader name. An anchor whose page cannot be opened gets the verdict `not-checked` with the reason in `note`: do not
retry it and do not look for the passage on another address.

Check every anchor and line of `for_you_701.json` as `BRIEF-common.md` says. Output
`data/verification/pages-2026-11-15/for_you_check_702.json`: `{"reader": "AI reader 702 (second reader)", "date":
"2026-11-15", "families": {"<family>": [{"index": 0, "line_verdict": "ok", "line": "<corrected line if fix>",
"anchors": [{"index": 0, "verdict": "confirmed", "quote": "", "where": ""}], "note": ""}]}}`. Final message under 150
words: counts by verdict and every line you fixed or dropped.
