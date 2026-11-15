# Pharmakon's own AI: the route (decided with the senior author, 15 November 2026)

The senior author: "apis are costly everything we make has to be ours if we make an ai it has to be ours"; "we have to
automate it otherwise the encyclopedia will never get finished"; "no i don't want my claude plan to use tokens! we have to
automate the ai! and make it perfect and completely individualized on perfect drug specialization"; "i want it to be
free". Nothing is scheduled on his Claude plan.

## What is ours already

- **Insight on the site** (from site 2.3.0): `pharmakon-insight-1`, the open model all-MiniLM-L6-v2 (Apache-2.0) trained
  further on this site's own questions (the wordings of every answer and the near-miss questions written for it) and
  averaged half and half with the original; 23 MB, run on the reader's own device (`scripts/insight/`, how it was made
  and measured: `scripts/insight/MODELS.md`). It finds checked answers and writes nothing. Measured on 400 real forum
  questions that it never trained on: with its judge, a wrong "Best match" for 1 question in 36 (2.2.0's way: 20 in 77),
  and none for the 126 questions the site cannot answer. The judge does most of that; the model itself is ahead of the open
  one on those questions by 2 to 6 points (too few questions to prove it) and clearly better on our own held-out wordings
  (85.5% find their answer, against 77.4%). Training took about twenty minutes on two processor cores
  and no graphics card; it is repeated at each release with the new answers' wordings (`finetune.py`, `export_mix.py`,
  `judge2.py`, `sweep_related.py`), so Insight learns every answer the site gains.

## What has to be built for the rest (reading, writing, checking)

Reading a paper, judging the evidence, writing an answer and checking it at the source need a language model. Ours will
be an open-weights model, trained on our own checked work and run on free graphics hours. Steps:

1. **The training set** (`data/own-ai/`, made by scripts from the repository, no paper text committed): one file per job,
   each line an instruction, its input and the checked output:
   - plain lines from an answer's precise statement (the lines on the site, after their blind check);
   - Myth or fact? cards from plain lines, with the raters' interest and clarity scores;
   - the second reader's job: an anchor's wording against the page of the PDF it cites (text taken from the senior
     author's PDFs at training time, never stored in the repository), with the second reader's verdict and correction;
   - study cards from papers (first reader's job), with the second reader's corrections.
2. **Training**: a notebook the senior author runs on a free graphics card (Kaggle's weekly hours): low-rank fine-tuning
   of an open model small enough for that card, licence Apache-2.0 or MIT.
3. **The test, per job**: examples held out from training, with the checked output as the key. A job moves to our model
   only when it does as well as the readers did on those examples (for the second reader's job: catches the errors the
   second readers caught, and invents none). Jobs it fails stay with the present readers.
4. **Running it**: the same free hours, started by a schedule; results arrive as files in the repository and go through
   the same checks as today.

## What is free already and needs no model

Finding what is missing (`scripts/editor/gaps.py`), ranking what people ask, retraining Insight
(`scripts/insight/finetune.py`), building, checking and deploying can run on GitHub's free build machines. Deploying
needs the senior author to store a Cloudflare key in GitHub once.

## The next three steps (proposed on 15 November 2026)

The senior author answered the same evening ("whatever you think is objectively optimal"; then, on what the machine may
publish: "it should be claims"). Step 1 is built in site 2.4.0. Step 2 is wanted more often than nightly. Step 3 was
changed by his decision: machine-written claims are to be published with a small label once they pass five hard-coded
gates and an exam on our own records. The plan, his words and what is built are in `docs/AUTOMATION.md`; the three steps
below are kept as they were proposed.

What limits the site now is how many answers exist, not how they are found: of 400 real forum questions it answers 79
in full, 195 in part and 126 not at all.

1. **Hear what visitors miss.** Where Insight has no answer, a button "Send this question to Pharmakon" (the question
   only, no name, no address, nothing else; kept in a free Cloudflare store). This changes the promise "Nothing you
   type leaves it" for a question a person chooses to send, so it needs the senior author's decision and one honest
   line beside the button.
2. **A nightly scout on GitHub's free machines** (no Claude plan, no paid service): ranks the questions people sent and
   the forum questions on file, runs `gaps.py`, searches Crossref, PubMed and OpenAlex for the papers that could answer
   the top ones, writes the senior author's to-do list with full APA 7 references from Crossref, retrains Insight when
   answers were added, builds, checks and deploys. It writes no answer.
3. **Writing and double-checking** stay with the present readers, inside the hours of the senior author's plan, until
   our own checker (steps 1 to 4 above) passes its test. Its training set exists already in the repository's records:
   4,778 checked passages and the second readers' corrections.

## What stays true whatever runs

Nothing unverified: a line is shown only after a reader who did not write it has checked it at its source. No AI is
perfect, ours included; the checks are what keep the site right.

One exception has been decided and is not yet in force: the machine lane of `docs/AUTOMATION.md` (decision 4, the senior
author, 15 November 2026), whose answers will be shown with the line "Written by our system from N papers. Not yet checked
by a person." until a reader has checked them. Until the day that lane opens, and the protocol and `CLAUDE.md` are amended
in his words, the rule above holds without exception.
