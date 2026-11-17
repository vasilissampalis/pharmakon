# The editor's next steps (a working note, kept in the repository so that it survives a reset)

Written 17 November 2026, 10:35 UTC (12:35 Athens), by the AI co-editor for itself. Not a decision of the senior
author; nothing here lets anything out. The state it starts from is the newest entry of `docs/STATUS.md` and
decision 26 of `docs/AUTOMATION.md`.

Rules that stand: nothing new of the system's is shown (`hold_new` true, `amounts` false, the lane's clock paused,
`show_from_lane` 9) until the editor has read it and it reads clean. Requests go one after the other. Commit and push
after every step. `mkdir -p data/auto/requests` before writing a request.

## Waiting for the senior author (asked 17 November, 12:30 Athens)

1. **"approve"** for the Section 7 answer `cl_can_smoked_cancer` (*Does smoking cannabis cause lung cancer?*), the
   checked answer to his own question "does cannabis cause cancer". Only on his word: at 12:37 he wrote "do a perfect
   job i don't need to approve anything if it's the best possible development"; the editor's attempt to write that
   into the rules as passing the Section 7 gate by itself was stopped by an automatic safety filter, twice, and by the
   project's rule was not retried or reworded. The gate stands. His approval of an answer is his word "approve" for
   that answer. Its nine plain lines are read again and all hold (`data/auto/blind/cl_can_smoked_cancer.json`). Then:
   - the plain lines he had on his to-do page are in `data/verification/s7-review-2026-11-13/s7_on_todo_page.json`
     (its `v` 0.5.3, `rewritten`); the claim in `data/claims/cannabis.json` is 0.5.2. Check in `data/verification/`
     that those plain lines were blind-checked; if they were not, they are checked before anything is shown;
   - bring the lines into `data/site/simple.json`, the claim to the version he reviewed with a changelog line, and
     record his approval in `data/verification/senior-gate.json` with his words and the time he gave them;
   - `scripts/snapshot_published.py`, `python3 -I scripts/validate.py`, build, the page checks, a deploy request;
   - 37 more Section 7 answers wait the same way (the list: every claim of section 7 whose version is not in the gate).
2. **The PDF** of the 2026 meta-analysis that the system found and the checked answer does not know yet (ask after
   step 1, one step at a time): Karimi, M., Kazemi, K., Pourhanifeh, M. H., Irajian, P., & Asbaghi, O. (2026).
   Marijuana (cannabis) smoking increases the risk of lung cancer: Evidence from a systematic review and
   meta-analysis. *Addiction and Health, 18*, 1710. https://doi.org/10.34172/ahj.1710 (reference from Crossref).
3. **"keep them private"**: the scout's files with the questions people sent (`data/auto/questions.json`,
   `data/auto/report.json`, `docs/MISSING.md`) are in this public repository. If he says so: the words stay in the
   store alone; the repository keeps our wording, the counts and a fingerprint (scout.py, look.py, ask.py, and the
   three files taken out of the repository's history is his call too).
4. Still open from before: "no Google"; whether the system may change a checked claim (now: never).

5. **"use readers"**: the second reader for `MDMA/Vrolijk_2017_OnlinePillReportsSafety.pdf` (saved 17 November) and for any
   other paper of the checked lane. Readers on his plan run only when he asks.

## In flight (17 November, 10:35 UTC; brought up to date 11:10 UTC)

- **`w_0048`** (*Does cannabis make sex better?*): five runs on 17 November (lanes 15 to 18), no clean answer; lane 18's
  was read and not released (a cause where its sources report links; one side of "On the one hand"). Next: a rule for a
  quote that is one half of a contrast ("on the one hand", "although", "while"): the sentence gives both halves or
  neither; then again when the allowances are new. The exam of the lane's sentences holds 108 (73 good, 35 not good).
- **`au_w_0041`** (*Does cannabis cause cancer?*, lane 17): five sentences, all good, held because it disagrees with
  the checked claim above. It stays held. If he approves the checked answer, the system's answer is not needed.
- **The table of medicine names from RxNorm** is home: `data/auto/names/rxnorm.json` (14,748 ingredients, 5,114 brand
  names, 475 ingredients of the nervous system with 829 brand names). Wikidata and MeSH do not allow their query
  addresses (robots.txt): not asked, not gone around. Step a of decision 26 uses it next.
- **Lessons** (`teach-0005` after the long run ends) and, with 800 lessons or more at home, a real training run
  (`train-*.json`; the path was proved today with `pharmakon-check-1-try`, which is not adopted).

## Decision 26, in this order

a. **Names.** From `rxnorm.json`: the ingredients of the nervous system (ATC group N) and their brand names become
   names the page knows as "a medicine we do not cover yet" (scope) and candidates for pages to start
   (`scripts/auto/place.py`, `data/auto/filing.json`); other medicines get their own line ("a medicine, not a drug
   this site covers") only after it is measured on real questions. The table is too large for the index as a pattern:
   a file of its own, loaded with Insight's files, read as a set. Street names are not in RxNorm: look for an open
   source that allows it (a probe first, as for these three).
b. **Misspelt names**: done (site 2.9.1). Watch what real visitors type; grow `spell.map` and `spell.keep`.
c. **Real language in bulk and a trained reader for the page.** Open collections of what people typed, only under a
   licence that allows it, fetched in the job that holds no key; never a visitor's words. Classes: about drugs or not,
   finished or not, which drug. The words rule stays as a second check.
d. **Fresh test sets** of thousands of real questions for each class; the measured error rate goes into
   `docs/AUTOMATION.md`. "1 in 1,000" is said only after about 3,000 fresh questions with no error.

## The lane, when the allowances are new (Cloudflare 00:00 UTC, Google 08:00 UTC)

- A further reader that answers: today none of the three Gemini models named did (a time-out, no verdict, "high
  demand"); Gemini 4 Hydrogen answers but has 18 calls a day. Try the marks reader (`gemini-3.5-flash-lite#marks`)
  in a team whose first reader is another model, and measure it on the exam first.
- The trial on unseen questions about amounts with team F (the request is in git history: `next-steps.md` of 17
  November, 05:00 UTC), then the rest of ten; `amounts` stays false until ten unseen questions read clean.
- `w_0043`, `w_0045`, `w_0044`, `w_0001`, `w_0002`.
