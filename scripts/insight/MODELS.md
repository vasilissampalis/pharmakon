# Pharmakon Insight: model files and where they came from

The two candidate models were obtained as npm packages (the workspace cannot reach Hugging Face) and accepted only
because every file is byte-identical to the official file on Hugging Face, whose SHA-256 (large files) or git blob
SHA-1 (small files) was read from the Hugging Face API through the browser on 14 November 2026. Nothing from the
packages' own code is used.

| Model | File | Bytes | Official hash | Official source | Taken from |
|---|---|---|---|---|---|
| all-MiniLM-L6-v2 (Apache-2.0) | all-MiniLM-L6-v2-q8.onnx (= onnx/model_quantized.onnx) | 22,972,370 | SHA-256 afdb6f1a0e45b715d0bb9b11772f032c399babd23bfc31fed1c170afc848bdb1 | huggingface.co/Xenova/all-MiniLM-L6-v2 (commit 751bff37) | npm @clay-design-system/embeddings 0.24.1 |
| all-MiniLM-L6-v2 | vocab.txt | 231,508 | git SHA-1 fb140275c155a9c7c5a3b3e0e77a9e839594a938 | same | same |
| potion-base-8M (MIT) | model.safetensors | 30,236,760 | SHA-256 f65d0f325faadc1e121c319e2faa41170d3fa07d8c89abd48ca5358d9a223de2 | huggingface.co/minishlab/potion-base-8M (commit bf8b0566) | npm @yarflam/potion-base-8m 1.0.4 |
| potion-base-8M | tokenizer.json | 683,666 | git SHA-1 3e511f68ccf95c33b9ffd214a94c6d25bdb3034f | same | same |

First evaluation (14 November 2026, `scripts/insight/eval_match.py`, provisional labels from the forum harvest's
coder, 356 answers, 278 answerable forum questions): word search (TF-IDF) top-3 42.8%; all-MiniLM-L6-v2 top-3 60.1%
(top-1 41.7%); potion-base-8M top-3 51.4% (top-1 37.8%). The gold set (two blind readers) and the ways people ask each
answer come next.

Gold-set evaluation (14 November 2026, evening, `scripts/insight/eval_gold.py`): 400 real forum questions labelled
blind by two readers (693 and 694; agreement 0.95, kappa 0.89 on answerable or not); 255 answerable by both, 126
unanswered by both. Right answer among the first 3 ("strict": an answer both readers judged to answer the question as
asked, n = 79; "lenient": also partial answers, n = 274):

| Matcher | Strict top-1 | Strict top-3 | Lenient top-3 |
|---|---|---|---|
| Word search (TF-IDF) | 43.0% | 51.9% | 46.0% |
| potion-base-8M, tuned | 50.6% | 68.4% | 62.8% |
| all-MiniLM-L6-v2, site questions only | 50.6% | 74.7% | 68.6% |
| all-MiniLM-L6-v2, tuned, with the 2,082 wordings of phrasings writer 696 | 54.4% | 79.7% | 70.4% |

(Tuned: 0.7 best question wording + 0.3 short answer + 0.2 word overlap, drug names expanded. Before the wordings the
tuned MiniLM scored 74.7% strict and 71.2% lenient top-3: the wordings, written without seeing these questions, add
about 5 points on questions with a full answer and change nothing measurable on partial ones.) No similarity threshold
separates questions the site cannot answer: at 0.60, 85% of answerable questions still get a match but so do 47% of
unanswerable ones. So the site never presents a match as "the answer": it shows the checked question it matched, in
full, beside its short answer, and always offers "Didn't find it? Ask us". Chosen for the site: all-MiniLM-L6-v2 (q8),
tuned, with the wordings.

## On the site (release 2.2.0, 14 November 2026)

Pharmakon Insight runs in the reader's browser with these files, published unmodified from `site/insight/vendor/` to
`insight/` next to the page and fetched only when someone uses the search box (never with a page; on a connection that
saves data, only when the reader taps the line that offers it). Nothing else is fetched, and nothing from outside the site.

| File | Bytes | SHA-256 | From |
|---|---|---|---|
| all-MiniLM-L6-v2-q8.onnx | 22,972,370 | afdb6f1a0e45b715d0bb9b11772f032c399babd23bfc31fed1c170afc848bdb1 | as above (official file) |
| vocab.txt | 231,508 | 07eced375cec144d27c900241f3e339478dec958f92fddbc551f295c992038a3 | as above (official file) |
| ort.wasm.min.js | 53,796 | b8a78c408c40da65fdc8ba0846f7b2948e92a4c6d6b23cc8e4165e428ad95443 | npm onnxruntime-web 1.31.1 (MIT), dist/ |
| ort-wasm-simd-threaded.mjs | 24,738 | 30ed0b5cd1182ede931fea448afb567d4dc705ec957af09f108a2be5f770dac3 | same |
| ort-wasm-simd-threaded.wasm | 14,848,852 | 4b884c203b0fa48d057be3332c65513ff85aa3c5bddd6946acc0fab7ecda001d | same |

Only the plain WebAssembly build of ONNX Runtime Web is used (one thread; no cross-origin isolation needed). Its WebGPU
build (29.5 MB) is never shipped: it is over Cloudflare Pages' limit of 25 MiB a file. The package's scripts were not run;
only these files were taken from it. The licences travel with them: `LICENSE-onnxruntime-web.txt` (MIT),
`NOTICE-all-MiniLM-L6-v2.txt` and `LICENSE-Apache-2.0.txt`. The page's security policy adds `'wasm-unsafe-eval'` to
`script-src` (it allows WebAssembly to compile, nothing else).

The index (`data/insight.json`) is made by `scripts/insight/build_index.py` on every `node site/build.js`, from the data
of the day: every answer with plain lines (data/site/simple.json), every wording of its question on the site
(data/site/questions.json and the plain lines' own question), the ways people ask it (variants_reader696.json; an answer
without them is found by its site questions and short answer alone), drug and street names (aliases.json,
substances.json). Tokens are made in Python by the tokenizers library; the vectors by the page's own runtime under Node
(`scripts/insight/embed.js`), one text at a time, so they are bit-identical to what the page computes. The Python
onnxruntime agrees to cosine 0.994 to 1 (median 1.000000) on a PC, as its int8 kernels round a little differently; a
batch padded to its longest text also shifts every vector in it slightly, so nothing is embedded in batches.
`scripts/insight/parity.js` checks all of this; `scripts/ux/insight_check.js` checks the search box and the answers in a
real browser. Threshold 0.65 (the editor's measure on the gold set: a match shown for 68.6% of answerable questions, a
right one among the three for 50.4%, and a match for 22.2% of questions the site cannot answer); so the page says
"Closest checked answers", and, under the threshold, "No checked answer fits this closely" with Ask us.
(That threshold and those two lines were release 2.2.0's; 2.3 replaced them: next section.)

## Release 2.3 (15 November 2026): two looks, and a judge for the best match

**One place for the numbers.** `site/insight/model.json` holds the model's file name, `weights`, `tiers` and `judge`;
`build_index.py` copies them into `data/insight.json`, the only place the page and the checks read them from (no number
is written in the page or in a check). A new model must take the same `vocab.txt` and inputs and give
`last_hidden_state`: add its file to `site/insight/vendor/`, change `file`, build. The vectors' cache
(`site/insight/.cache/vectors-<first 16 characters of the model file's SHA-256>.npz`, not committed) is kept by model, so
a new model embeds everything again. Then make the judge's numbers for it (below), put them in `model.json`, build again.

**Two looks at a question.** First look: 2.2.0's tuned score (0.7 x best wording + 0.3 x short answer + 0.2 x word
overlap, the drug's own name brought along). Topic: every wording is embedded a second time with the drug names
replaced by "it", and so is the question, because the drug's name carried so much of the meaning that any question about
kratom scored high against any answer about kratom. Which drug is meant is settled by the names themselves
(`data/insight.json`, `names`), not by the model: an answer can be the best match only when it is about every drug the
question names, or, when it names none, about the drug of the page the reader is on. Wordings indexed (3,339 for 372
answers on 15 November): the site's own questions, the six of phrasings writer 696, and the three hurried ones (`more`)
of the near-miss readers 707 and 708; those readers' `near` questions (which an answer does NOT answer) are never indexed.

**The judge** (the editor's rule; research and training in `judge2.py`). Two thresholds on the two looks (first look
>= 0.72 and topic >= 0.45) gave a best match that was wrong for 20 of 77 gold questions (26%). The judge replaced them.
The answers are put in order of `by` = first look + `weights.topic` x topic, those about the drugs named `weights.same`
ahead; c is the first. Six numbers of c (`judge.features`, in this order):

1. best wording: the similarity of its closest wording in the first look, before the weights;
2. second wording: its second-closest wording (0 if it has one wording);
3. short answer: the similarity of its short answer;
4. word overlap (TF-IDF);
5. topic: its closest wording with the drug names taken out;
6. lead over the next answer: `by` of c less the highest `by` among the other answers about every drug the question names
   (less 0 if there is no other).

p = 1 / (1 + exp(-(sum of w_i x (f_i - mu_i) / sd_i, + b))). c is the best match when it is about every drug named and
p >= `judge.best`; there is never a second best match. Related: the next answers in the same order, up to three, with a
first look of `tiers.related` or more and a topic of `tiers.near` or more, about at least one of the drugs named.

Trained only on our own examples, never on a gold question (`judge2.py --six`; scikit-learn logistic regression, C = 1,
on standardized numbers). Yes: a way of asking (writer 696; the near-miss readers' hurried wordings) against its own
answer, with that wording left out of the index first (2,957 pairs). No: a near-miss question against the answer it does
not get (1,585), and each way of asking against the three other answers that rank highest for it (8,871). On answers not
seen in training (5 folds by answer), wording against near-miss, area under the curve: judge 0.783, first look alone
0.772, topic alone 0.698. Weights on standardized numbers: lead over the next answer 1.36, best wording 0.54, word
overlap 0.41, second wording 0.38, short answer -0.28, topic 0.12; bias -2.14. So what makes a best match is mostly how
far the first answer stands from the next one about the same drug.

Measured on the gold set (400 real forum questions, two blind readers: 79 have a full answer, 126 none), base model
all-MiniLM-L6-v2 (q8), `judge2.py --six`; `build_index.py --eval` prints the same numbers from the page's own rule
(class Ranker), and `parity.js` holds the page to that rule (the judge's number to 1e-4; measured difference 3e-7).
Odd-numbered questions are for choosing the cut (dev), even-numbered ones for reporting it (test):

| Best match when | Questions | Best matches | Full answer | Partial | Wrong | Unanswerable given one | Full answers found |
|---|---|---|---|---|---|---|---|
| two thresholds (before) | all 400 | 77 | 26 | 31 | 20 (26%) | 2 of 126 | 26 of 79 |
| p >= 0.5 | dev 200 | 30 | 15 | 13 | 2 | 0 of 63 | 15 of 43 |
| p >= 0.5 | test 200 | 29 | 11 | 17 | 1 | 0 of 63 | 11 of 36 |
| p >= 0.5 | all 400 | 59 | 26 | 30 | 3 (5%) | 0 of 126 | 26 of 79 |
| **p >= 0.6 (model.json)** | dev 200 | 14 | 13 | 1 | 0 | 0 of 63 | 13 of 43 |
| **p >= 0.6 (model.json)** | test 200 | 14 | 8 | 5 | 1 | 0 of 63 | 8 of 36 |
| **p >= 0.6 (model.json)** | all 400 | 28 | 21 | 6 | 1 (4%) | 0 of 126 | 21 of 79 |
| p >= 0.7 | dev 200 | 10 | 10 | 0 | 0 | 0 of 63 | 10 of 43 |
| p >= 0.7 | test 200 | 10 | 6 | 3 | 1 | 0 of 63 | 6 of 36 |
| p >= 0.7 | all 400 | 20 | 16 | 3 | 1 (5%) | 0 of 126 | 16 of 79 |
| p >= 0.8 | dev 200 | 10 | 10 | 0 | 0 | 0 of 63 | 10 of 43 |
| p >= 0.8 | test 200 | 6 | 3 | 2 | 1 | 0 of 63 | 3 of 36 |
| p >= 0.8 | all 400 | 16 | 13 | 2 | 1 (6%) | 0 of 126 | 13 of 79 |

What the cut costs: at 0.6, 32 of the 79 questions with a full answer have it under Related instead (23 at 0.5), after
the line "We haven't checked exactly this yet"; related answers are shown for 209 of 400 questions (400 rows, 38% of
them a full or partial answer; 28 of the 126 unanswerable questions get some). For example "does ecstasy damage your
brain permanently" (the 2.3 brief's own example of a match) gets p 0.53: its answer is first under Related at 0.6, and
the best match at 0.5. Near-miss questions given the answer they do not get as best match: 13.9% at 0.5, 9.7% at 0.6,
6.9% at 0.7, 3.8% at 0.8 (of 1,585; these questions were training examples, so the true rate is higher).

For a new model: build; `python3 -I scripts/insight/judge2.py site/insight/.cache/index-input.json
site/dist/data/insight.json --six --save FILE`; copy `features`, `mu`, `sd`, `w`, `b` into `judge` in `model.json`, choose
`best`; build again; then `python3 -I scripts/insight/build_index.py site/insight/.cache/index-input.json OUT.json --eval`,
`node scripts/insight/parity.js`, `node scripts/ux/insight_check.js`. Probes for single questions: `ask.py` (the page's
rule, with the judge's number and its six numbers) and `ask2.py`. `sweep.py` belongs to the two thresholds the judge
replaced: it runs against `build_index.py` as it was before the judge (commit aba0173).

**Next questions** ("People also ask", "Read next"): at build, each answer's nearest answers by the meaning of their
site questions, never itself; the same drug first, then the nearest on each page the answer is told on; never an answer
that shares neither a drug nor a page with it. They travel in the page (`INS_NEXT`, about 24 KB), not in a fetched file.

**Size and speed.** `data/insight.json` 3.6 MB; with the model and the runtime about 42 MB, fetched once when the search
box is first used. A question takes two passes of the model (with and without the drug names) and one ranking: median
32 to 40 ms, slowest about 150 ms, in the checks' browser.
