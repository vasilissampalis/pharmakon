# Pharmakon's own AI: the route (decided with the senior author, 15 November 2026)

The senior author: "apis are costly everything we make has to be ours if we make an ai it has to be ours"; "we have to
automate it otherwise the encyclopedia will never get finished"; "no i don't want my claude plan to use tokens! we have to
automate the ai! and make it perfect and completely individualized on perfect drug specialization"; "i want it to be
free". Nothing is scheduled on his Claude plan.

## What is ours already

- **Insight on the site**: all-MiniLM-L6-v2 (Apache-2.0) fine-tuned on this site's own questions (the wordings of every
  answer and the near-miss questions written for it), 23 MB, run on the reader's own device (`scripts/insight/`). It finds
  checked answers and writes nothing. Measured on 400 real forum questions that it never trained on.

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

## What stays true whatever runs

Nothing unverified: a line is shown only after a reader who did not write it has checked it at its source. No AI is
perfect, ours included; the checks are what keep the site right.
