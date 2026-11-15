# The nightly run: how Pharmakon grows by itself (design, 15 November 2026)

The senior author, 15 November 2026: "i wonder if insight should understand itself what's missing from the website ...
and can update the site itself and also find the questions that people interested in drugs search for itself. like making
the website expand by itself and prioritize what users really want to read"; "it should be interesting if pharmakon
insight could read on the papers we already have understand the gaps based on what users want to know and fill in those
gaps itself. i wonder if we can get pharmakon automated and perfect"; "i wonder if insight can do it itself as an
autonomous ai".

Insight has two halves. The half on the reader's own device finds checked answers and writes nothing, which is why it
cannot make things up. The half that reads, writes and checks is the editorial pipeline of `CLAUDE.md` (first readers,
writers, second readers who wrote none of it, blind checkers, the editor). The nightly run is that pipeline started by a
schedule instead of by a message. It is **not switched on until the senior author says so**.

## What one night does, in order (each step only with the tools and rules already in this repository)

1. **Take stock.** `git pull`; read `CLAUDE.md` and `docs/STATUS.md`; `python3 -I scripts/editor/gaps.py --write` (what
   the site is missing); read the to-do page's ticks; if the senior author's computer is linked, stage the PDFs he has
   saved since last night and check each is the right paper (`scripts/editor/verify_pdfs.py`).
2. **Answer what people ask from what is on file.** The library gap finder
   (`data/verification/gapfill-*/BRIEF-finder.md`) lists the most-asked questions that cards on file can answer; claim
   writers write up to ten new answers a night from those cards; round-2 readers check every new anchor at the PDF;
   the editor adjudicates; plain lines and Myth or fact? cards are blind-checked, and cards are scored for interest.
3. **Fill what needs no paper.** Lines from official and non-profit pages (what each drug is, "for you" lines, a
   country's line on test kits, seller pages), each read by one reader and checked at its source by another.
4. **Teach Insight the new answers.** Wordings and near-miss questions for each new answer; `scripts/insight/finetune.py`;
   the new model is kept only if the gold-set measures (`scripts/insight/eval_model.py`) are no worse.
5. **Build and check.** `scripts/snapshot_published.py`; validator (0 hard failures); `node site/build.js`;
   `python3 -I site/build_public.py`; every check in `scripts/ux/` and `scripts/insight/parity.js`. If anything fails,
   nothing is released: the failure goes into `docs/STATUS.md`.
6. **Hand over.** Commit and push; update `docs/STATUS.md` and the to-do page (papers and photos needed, most-asked
   first); send the zip with a five-line summary: what is new, what was dropped and why, what is needed from him.

## What a night never does

- Deploy, or record an approval the senior author did not give (section 7, doses, emergency guidance stay his).
- Publish anything unchecked, or read a paper that is not on file; no dosing, administration or potentiation guidance.
- Retry or reword a step an automatic filter stopped; go around a site that refuses; download files; sign in anywhere.
- Spend without limit: ten new answers, one training run and one release candidate a night.

## What still needs him

Papers behind paywalls and photos (his folder), the deploy click, and his review.
