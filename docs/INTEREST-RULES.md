# Interest rules: quiz items, myth-or-fact cards and "why this rating" lines

Rewritten on 13 November 2026 after the workspace reset (the first version, of 12 November, was lost); same rules.

The senior author's standard: every item must be useful in life and interesting, the kind of research fact a person
would repeat to a friend ("actual research facts", playful, never a school test). People like talking to humans, not
textbooks: plain words, a little wit where the evidence allows, never mockery and never judgment of people who use drugs.
On 14 November 2026 he put it in one line: users should find it interesting "as if a super educated joe rogan answered
their reddit questions", and "we should not discard everything if people in forums would find it useful". So the test for
every item is a person on a drug forum: would they find it useful or surprising, and would they repeat it? Since 14
November the site asks one format only, Myth or fact? (true-or-false statements); the Quick questions are kept on file,
and the useful ones are rewritten as myth-or-fact statements.

## Every item

- One fact, from the answer's own plain lines (`short`, `but`, `how`) at the version it was written for (`v`). A checker
  rejects any item, option or `why` that says more than those lines.
- Worth telling a friend: surprising, myth-busting, or practical for safety. Not trivia: no dates, author names, journal
  names or sample sizes unless they are the point.
- True-or-false (`tf`): a statement people might believe; `answer` true or false; `why` in one or two plain sentences
  that give the research reason, with its limits when they matter ("in one small study").
- Quick question (`quiz`): three options, all plausible, one right; no trick wording; `why` starts with the right answer.
- Plain sentence case, at most about 20 words for statements, person-first language.

## Never

- Amounts, doses, timing, routes compared for speed or strength, or anything about reaching or strengthening effects.
- Mixing drugs except as risk facts ("what happens when X and Y are combined, and what are the risks").
- Getting or selling drugs, hiding use, or anything that reads as instructions.
- Certainty beyond the evidence: an association is not a cause, a self-report stays a report, an animal finding stays
  an animal finding.

Weak items (true but dull, or only half supported) stay off the site.

## "Why this rating" (`rate` in `data/site/simple.json`)

One or two plain sentences, at most about 40 words, that say what limits how sure we can be (for example "one small
study, and nothing else that changed was taken into account"). No research jargon: not GRADE, bias, confounding,
heterogeneity, imprecision, indirectness or power. The full reasoning stays one tap further, for researchers.
