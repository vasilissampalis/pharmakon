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

## Our own model: pharmakon-insight-1 (site 2.3.0, 15 November 2026)

The senior author: "our own ai"; "we have to automate the ai"; "i want it to be free". From 2.3.0 the encoder on the site
is Pharmakon's own: all-MiniLM-L6-v2 taught this site's questions with this site's own examples, then averaged half and
half with the original so that it keeps what the original knew about ordinary language. It has the same vocabulary,
inputs, output, size and speed, so the page's code did not change: `site/insight/model.json` names the file, and holds
the judge's numbers and the tiers made for it. It still writes nothing: it only finds checked answers.

| File | Bytes | SHA-256 | What it is |
|---|---|---|---|
| pharmakon-insight-1-q8.onnx | 22,911,759 | 4f5059c16139f1d93e5b78df2a4ee7c5728452e46d93d663cca31e23d1c2c2f5 | the model on the site (`site/insight/vendor/`, published as `insight/`); int8 |
| NOTICE-pharmakon-insight-1.txt | 1,137 | (text) | what was changed and by whom, as Apache-2.0 (section 4b) asks; published beside the model with `NOTICE-all-MiniLM-L6-v2.txt` and `LICENSE-Apache-2.0.txt` |
| model.onnx (the float original it was trained from; not in the repository, 90 MB) | 90,387,606 | 759c3cd2b7fe7e93933ad23c4c9181b7396442a2ed746ec7c1d46192c469c46e | npm @maycombhq/embed-model 2.0.0-beta.1, whose `pins.json` names huggingface.co/Xenova/all-MiniLM-L6-v2 (commit 751bff37), `onnx/model.onnx`, with this hash |

The float original: only its weights are read, as numbers; none of the package's code is run. Its hash has not yet been
read from Hugging Face by us (the workspace cannot reach it; to do through the browser, as for the files above). Until
then, what is checked is that it computes what the verified official int8 file computes: on 200 site questions the two
give vectors with a cosine of 0.993 (median; lowest 0.987), the difference int8 rounding makes. `all-MiniLM-L6-v2-q8.onnx`
stays in `site/insight/vendor/` for comparison and as the way back (change `file` in `model.json`, put the base model's
judge numbers back from `model.json` as it was at commit 2dd1c04, build); it is no longer published.

**Training** (`finetune.py`; PyTorch on two processor cores, no graphics card, about 20 minutes). Examples, all ours:
each answer's ways of being asked (its questions on the site, the six of phrasings writer 696, the hurried ones of the
near-miss readers 707, 708 and 725): 3,186 wordings; and 1,810 near-miss questions for 362 answers (questions that sound
close to an answer and are not answered by it). A wording is pulled towards another wording of the same answer and pushed
away from the other answers' wordings in its batch and from its own answer's near-miss questions (multiple-negatives
ranking loss on cosine x 20; batches of 32; learning rate 2e-5; at most 48 tokens; seed 7). No forum question and no gold
label is used, so the gold set stays a fair test.
- Step 1, how long to train: with the examples of 15% of the answers held out (55 answers, chosen by a hash of their id),
  a held-out wording found its own answer among all answers 77.4% of the time before training and 85.1%, 85.5% and 85.3%
  after 3, 5 and 6 passes; held-out wording against held-out near-miss, area under the curve 0.806 before, 0.930 after 5.
  The curve is flat from the third pass.
- Step 2, the model: every answer's examples, 6 passes (`--all --epochs 6`).
- Step 3, mixing (`export_mix.py … 0.5`): every weight is half the trained one and half the original; then ONNX (opset
  14) and int8 (onnxruntime's dynamic quantization, QUInt8).

**Why half and half.** The model trained on our examples alone (step 1's, from 85% of the answers) found full answers
more often than the open model and partial ones less often: it had learned our wordings so well that it grew stricter
about everything near them. Averaging its weights with the original's keeps most of what it learned and gives back what
it lost. In the Python harness (`judge.py`, `compare.py`: 2.2.0's scoring and no judge; 400 gold questions, 79 with a
full answer, 274 with a full or partial one; int8 files):

| Encoder | Full answer first (n = 79) | within the first 3 | Full or partial first (n = 274) | within the first 3 |
|---|---|---|---|---|
| open model | 55.7% | 79.7% | 53.3% | 70.1% |
| trained alone (85% of the answers) | 60.8% (+5.1; -5.1 to +15.2) | 84.8% (+5.1; -1.3 to +11.4) | 49.6% (-3.6; -8.8 to +1.5) | 73.4% (+3.3; -1.5 to +8.0) |
| that one, half and half | 63.3% (+7.6; +1.3 to +15.2) | 79.7% (0.0; -3.8 to +3.8) | 57.7% (+4.4; +0.7 to +8.0) | 73.0% (+2.9; -0.4 to +6.2) |
| **pharmakon-insight-1** (trained on all, half and half) | 62.0% (+6.3; -1.3 to +15.2) | 82.3% (+2.5; -2.5 to +7.6) | 56.2% (+2.9; -0.4 to +6.6) | 72.3% (+2.2; -1.1 to +5.5) |

In brackets: the difference from the open model in points, question by question, and its 95% interval from 4,000
resamples of the questions (`compare.py`; the logs of this section are in `data/verification/insight/own-model-2026-11-15/`).
Read plainly: our model is ahead of the open one on every count, by 2 to 6 points, and for the model on the site no
interval excludes zero. With 79 and 274 questions a gain of this size cannot be proved. What is proved is on our own
examples (held-out wordings find their answer 85.5% of the time against 77.4%), and what the release gains on forum
questions comes mostly from the judge (table below). The model is published because it is ours, costs nothing, learns
every answer the site gains, and is not worse than the one it replaces on any count that matters here.

On the page's own rule a quarter and a half of the trained weights did the same (35 best matches each at 0.6: 23 full,
11 partial, 1 wrong; and 22, 12, 1); a half was kept because it tells a wording from a near-miss better on our own
examples (area under the curve 0.856 against 0.818; open model 0.783; trained alone 0.910).

**On the page's own rule** (`build_index.py --eval`; the judge made for each model by `judge2.py --six --save`; a best
match from 0.6; the same 400 gold questions):

| | Best matches | Full answer | Partial | Wrong | Unanswerable given one | Near-miss given the answer it does not get |
|---|---|---|---|---|---|---|
| 2.2.0's kind of rule (two thresholds), open model | 77 | 26 | 31 | 20 (26%) | 2 of 126 | 20.9% |
| the judge, open model | 28 | 21 | 6 | 1 (4%) | 0 of 126 | 9.7% of 1,585 |
| **the judge, pharmakon-insight-1 (site 2.3.0)** | **36** | **24** | **11** | **1 (3%)** | **0 of 126** | **8.3% of 1,810** |
| the same, dev half (odd-numbered) | 20 | 14 | 6 | 0 | 0 of 63 | |
| the same, test half (even-numbered) | 16 | 10 | 5 | 1 | 0 of 63 | |

Candidates in the page's order: a full answer comes first for 63.3% of the 79 questions that have one (open model
58.2%) and within the first three for 74.7% (open model 77.2%; the difference is two questions). The judge for this
model was trained on 14,558 pairs (3,187 wordings against their own answer with that wording left out of the index,
1,810 near-miss questions, 9,561 wordings against the other answers that rank highest for them). Weights on standardized
numbers: lead over the next answer 1.58, best wording 0.92, second wording 0.80, word overlap 0.05, short answer 0.00,
topic -0.04; bias -2.68. Its area under the curve on our own examples (0.876; first look alone 0.869) is not a fair
figure for this model, because the encoder was trained on those same examples; the gold set is the fair one. The same
holds for the near-miss column above.

**Where Related begins for this model** (`sweep_related.py`). The open model's thresholds (first look 0.58, topic 0.45)
are too strict for a model whose scores spread wider: with them the full answer was seen for only 42 of the 79
questions that have one, and "how can you die from alcohol" showed nothing under Related. Per question, what Insight
shows (the best match and the related rows) was counted as help (a full or partial answer is among them), junk (rows,
none an answer), miss (nothing, although the site has a full or partial answer) or rightly empty:

| First look, topic | Help | Junk | Miss | Rightly empty | Full answer seen | Related rows | of them answers | Unanswerable with rows |
|---|---|---|---|---|---|---|---|---|
| 0.58, 0.45 (the open model's) | 95 | 34 | 155 | 116 | 42 of 79 | 142 | 53% | 10 of 126 |
| 0.50, 0.38 | 147 | 88 | 73 | 92 | 52 of 79 | 401 | 37% | 34 of 126 |
| 0.48, 0.45 | 142 | 71 | 90 | 97 | 54 of 79 | 338 | 43% | 29 of 126 |
| 0.48, 0.40 | 154 | 79 | 74 | 93 | 55 of 79 | 416 | 39% | 33 of 126 |
| **0.48, 0.38 (model.json)** | **160** | **90** | **61** | **89** | **55 of 79** | **465** | **37%** | **37 of 126** |
| the same, dev half | 78 | 46 | 30 | 46 | 32 of 43 | 215 | 34% | 17 of 63 |
| the same, test half | 82 | 44 | 31 | 43 | 23 of 36 | 250 | 39% | 20 of 63 |
| 0.46, 0.38 | 167 | 98 | 55 | 80 | 55 of 79 | 529 | 35% | 46 of 126 |

No setting stands out: help and junk rise together, and the dev and test halves agree on that. Four ways of deciding
(the two thresholds; first look + 0.5 x topic; both; a free sum) gave the same within two or three questions at equal
numbers of rows, so the rule stayed as it was. The setting was taken by two plain reasons, and is the editor's
judgement, not a measured optimum: (1) the first look at 0.48, because the step from 0.50 adds 13 helpful sets of rows
and 2 unhelpful ones, and the next step, to 0.46, adds 7 and 8; (2) the topic at 0.38, one step past where the same
count turns (0.40 to 0.38 adds 6 and 11), because the nearest answers for the senior author's two test questions have
topic scores of 0.41 ("How many deaths does alcohol cause worldwide?") and 0.40 ("How many UK deaths were linked to
ketamine, and what were they?"), and a reader who asks how one can die from a drug is better served by that answer under
Related, below "We haven't checked exactly this yet", than by nothing. For comparison, the open model with its own
thresholds showed the full answer for 53 of 79 with 400 related rows, 38% of them answers, and rows for 28 of the 126
unanswerable questions. A "junk" set of rows is still about the drug that was asked about and is labelled Related; read
some with `sweep_related.py IN INDEX --show 0.48 0.38`.

**The questions the senior author asked** (the judge's number; a best match from 0.6): "how can you die from alcohol"
0.11 and "give me the full evidence about how can i die from ketamine" 0.42: no best match, the line "We haven't
checked exactly this yet" with "Ask us to check it", and the nearest answer under Related. "is ketamine bad for your
bladder" 0.96, "does alcohol cause cancer" 0.96, "is weed addictive" 0.93, "what happens if i mix alcohol and cocaine"
0.74, "does molly mess up your memory" 0.70: each a best match. "does ecstasy damage your brain permanently" 0.58: its
answer is first under Related. Known weakness: where the site has no near answer, the rows under Related can be
only loosely related ("can you overdose on lsd" shows the answers on LSD with MDMA and on chromosomes, and not the one
on emergency treatment after LSD): the model tells "answers this" from "does not" far better than it ranks what is
merely near. They are still better rows than the word search shows under them. To do: a second small judge for
Related, trained on the near-miss questions as examples of "near, not the answer".

**What limits Insight now is the number of answers, not the search.** Of the 400 forum questions the site answers 79 in
full, 195 in part and 126 not at all. Every new answer needs its wordings and near-miss questions (briefs
`data/verification/insight/BRIEF-phrasings-*.md`), and then:

**At each release that adds answers** (free; about half an hour of two processor cores): `node site/build.js` (makes
`site/insight/.cache/index-input.json`); `python3 scripts/insight/finetune.py MODELS_DIR --out DIR --all --epochs 6`;
`python3 scripts/insight/export_mix.py MODELS_DIR DIR/best.pt 0.5 site/insight/vendor/pharmakon-insight-N-q8.onnx`
(MODELS_DIR holds the two npm packages unpacked: `_maycombhq_embed-model/package/model.onnx`, the float original, and
`_clay-design-system_embeddings/package/model/vocab.txt`); name the file in `model.json`, write its NOTICE with its SHA-256;
build; `python3 -I scripts/insight/judge2.py site/insight/.cache/index-input.json site/dist/data/insight.json --six
--save FILE` and copy its numbers into `model.json`; `python3 -I scripts/insight/sweep_related.py
site/insight/.cache/index-input.json site/dist/data/insight.json` and check the tiers still sit where the counts turn;
build; `build_index.py --eval`, `node scripts/insight/parity.js`, `node scripts/ux/insight_check.js`. A new model is
published only if its best match on the gold set is wrong no more often than the one it replaces.

## Teachers and a pupil: the model learns by itself (decision 41, 19 November 2026)

The senior author, 21:44: "we have to teach our ai to work like an llm and do what you do as perfect as possible it has to
work by itself perfectly all the time autonomously". A small encoder learns a language from examples, so the examples are
made every day and the model is taught again every week, by itself, and measured each time against the model on the site.

**The teachers** (`teachers.py`). Round 0 is the editor's: up to eight ways a person might type each answer's question,
for all 391 answers (`data/verification/insight/variants_teacher.json`, 3,001 kept), written from the answers' own
questions without the gold set or any visitor's words in view; a wording that shares 70% of its words with a gold question
was left out (11), and so was a wording the answer already had (116). From then on, in every Auto run, a free model
(Gemma 4 31B at Google's free tier first) writes ten more for the answers that have the fewest (a new answer first),
shown the answer's question, the ways it is already asked and three answers' worth of the editor's examples; a model of
another family (gpt-oss-120b on Groq first) keeps only those that ask exactly the same question; code keeps the drug,
drops copies of any answer's wordings and anything near a gold question; sixteen per answer at most
(`data/auto/insight/teachers.json`, each with its writer, its checker and its day).

**The pupil** (`train.py`, `.github/workflows/insight.yml`). As `finetune.py`, with the answers as the site has them now
(the machine lane's included), the teachers' wordings added (`--teacher`), and a choice of base among the open encoders
that read with the page's own vocabulary and pooling (all-MiniLM-L6-v2; gte-small, MIT). Each pass is checked on the
readers' wordings of the 15% of the answers it never saw (never the teachers': every model is tested on the same
questions); `--all` trains on every answer. Each share of the trained weights asked for (`--mix 0.5,1.0`) is written as
the page's ONNX file and as int8 (checked against the trained model: cosine 0.98 or more), and measured on the gold set as
`encoders.py` measures (the page's first look), with the index as it is and with the teachers' wordings added to it.
The GitHub workflow runs up to eight such trainings at once, one machine each, every Sunday and on request; its records
are in `data/verification/insight/train/`, its models among the release files (`own-models`), each with its SHA-256.

**The measured path in one go** (`candidate.py MODEL.onnx`): the candidate's index (every text embedded again by the
page's own runtime), its own judge (`judge2.py --six --save`), and the gold set ranked with the page's rule for the
candidate and for the model on the site, side by side; "better" only where its best match is wrong no more often, a
question nobody can answer gets one no more often, and more questions get their full answer as best match (or as many,
with fewer wrong). The real `model.json` is not touched (`PK_INSIGHT_MODEL_JSON`). A model that is better is shipped by
the editor with its NOTICE, the tiers swept for it (`sweep_related.py`), a build and every check.

**First results (19 November 2026, evening).** Held out (the readers' wordings of the 57 answers a training never saw), all-MiniLM-L6-v2,
six passes: without the teachers' wordings it finds the answer for 85.3% of them (wording against near-miss, area under the curve 0.917);
with them, 86.8% (0.933). On the gold set with the page's own rule (`candidate.py`; each model with the judge made for it):

| | Best matches | Full | Partial | Wrong | Nobody can answer, given one | Full answer first | in the first three | Shown: helps | junk | misses |
|---|---|---|---|---|---|---|---|---|---|---|
| pharmakon-insight-1 (site 2.3 to 2.26) | 40 | 24 | 10 | 6 (15.0%) | 2 of 126 | 60.8% | 73.4% | 133 | 60 | 106 |
| **pharmakon-insight-2** (every answer, the teachers' wordings, half and half) | **41** | **23** | **12** | **6 (14.6%)** | **2 of 126** | **62.0%** | **77.2%** | **138** | **58** | **102** |
| insight-1 with 8 teachers' wordings per answer in its index | 45 | 24 | 13 | 8 (17.8%) | 1 | 63.3% | 81.0% | | | |
| insight-1 with its judge taught the teachers' wordings too | 51 | 24 | 18 | 9 (17.6%) | 2 | 60.8% | 73.4% | | | |

"Shown" is what Insight puts before the reader for each of the 400 questions (the best match and the related rows, at the tiers of
model.json): helps (a full or partial answer is among them), junk (rows, none an answer), misses (nothing, though the site has an answer).
pharmakon-insight-2 is wrong no more often (MODELS.md's rule), gives a question nobody can answer a best match no more often, and what it
shows helps five questions more and misleads two fewer; it gives one full answer fewer as best match and two partial ones more, a difference
of one question in 400. It also knows every answer the site has now (the machine lane's among them), which insight-1 never saw. So it is the
site's model from 2.27.0 (`ship.py`; NOTICE-pharmakon-insight-2.txt). The two other rows are not shipped: more wrong best matches at the
judge's cut (the index would also grow by 2.8 MB). The free models' wordings (`teachers.py`) and gte-small (`insight.yml`) come next.

## The short answer read after its question; the judge's cut at 0.7; a research chemical by its own name (site 2.28.6, 20 November 2026)

Found by asking Insight thirty-five more everyday questions: "does ketamine help depression" (also gold question 119) got no answer, though
the answer on ketamine drips ("Can a ketamine drip lift depression within hours, and for how long?") had a wording at 0.97 from it. Its short
answer leans on its question ("It can, within hours. A day after one drip, 64 in 100 were much better ..."): alone, its meaning stood at -0.03
from the question, so the answer on side effects of ketamine treatment came first and the judge, rightly, did not take it. Now each short answer
is embedded after its own question (`model.json`, `short_with_question`; `build_index.py`). On the gold set (`build_index.py --eval`; near-miss:
of 1,810 questions written as ones an answer does NOT answer, how many get it as best match; "now" is the site before this change, with the
answers the machine lane has published since 2.28.0, which the gold readers never saw: of the "wrong" below, four go to such answers and answer
the question, among them "Does LSD stay in the body forever?"):

| | Best matches | Full | Partial | Wrong | Nobody can answer, given one | Near-miss given | Full answer first | in the first three |
|---|---|---|---|---|---|---|---|---|
| now (judge's cut 0.6) | 43 | 23 | 12 | 8 | 4 of 126 | 122 | 60.8% | 77.2% |
| short after its question, cut 0.6 | 47 | 25 | 13 | 9 | 5 | 142 | 63.3% | 78.5% |
| the same, with a judge taught for it (`judge2.py --six`), cut 0.6 | 42 | 22 | 10 | 10 | 5 | | | |
| short after its question, cut 0.64 | 41 | 24 | 10 | 7 | 3 | 126 | | |
| short after its question, cut 0.66 | 38 | 23 | 8 | 7 | 3 | 115 | | |
| **short after its question, cut 0.7 (shipped)** | **35** | **23** | **7** | **5** | **2** | **101** | **63.3%** | **78.5%** |

The cut was chosen on the odd-numbered gold questions (dev: 14 full, 3 partial, 4 wrong at 0.7, against 13, 5, 6 now) and reported on the even
ones (test: 9, 4, 1 against 10, 7, 2). At 0.7 the best match is wrong less often, a question nobody can answer gets one half as often and a
near-miss question gets the answer it does not get 21 times fewer, for as many full answers; five partial answers go from best match to the
related answers. tiers.related moves from 0.48 to 0.50 (`sweep_related.py`: the related answers as many as before, as often right, and fewer
for questions nobody can answer). The cost, measured on the editor's 198 probe questions: "can weed make you go crazy" and "does lsd make you
insane" now get their answers (psychosis; psychedelics and mental health) first among the related answers rather than as the best match: the
three answers on psychosis stand close to each other, so the lead over the next one is small and the judge is less sure. The partly right
"is ecstasy the same as mdma" (pill contents) and the wrong "is molly the same as mdma" (MDMA and MDA) went the same way.

A research chemical named by the shape of its name (`scope.json`, "chem": 3-MeO-PCE, 5-MeO-DALT, 1P-LSD) is never answered by an answer that
names none of those the question names (`build_index.py`, the index's "chem"; `Ranker.speaks` and the page's `insSpeaks`; `parity.js` asks
three such questions): "What is 3-MeO-PCE like, and how risky is it?" had the answer on 5-MeO-DALT, another drug, as its best match at the cut
of 0.6.

Measured and not kept (20 November 2026): the judge's lead measured over the next answer of ANOTHER topic of the page (the three answers on
psychosis would no longer stand in each other's way for "can weed make you go crazy"). With the judge as it is, at the cut of 0.7: best
matches 39 (full 24, partial 8, wrong 7), near-miss questions given the answer they do not get 138 of 1,810 against 101: a near-miss
question is most often one of the same topic, and the lead is what kept it from the answer.

Measured and not kept (20 November 2026): a related answer whose first look is very near whatever its topic score ("is it bad to smoke weed
while pregnant": the answer on cannabis in pregnancy stood first at 0.68, its topic at 0.49, and was not listed). On the gold set, from a first
look of 0.65: 12 questions more see an answer among what is shown, and 11 more are shown rows none of which answers them (and 5 more questions
nobody can answer get rows); from 0.60, 25 and 20. As many rows mislead as help: tiers stay as they are.

**Three more aspects (site 2.28.8, 20 November 2026).** "kill" said of brain cells, the high, pain or time is no question about dying ("does weed kill brain cells" asked every answer on cannabis to speak of dying); an answer that never speaks of vaping never answers a question about vaping ("how bad is vaping for your lungs" got the answer on smoking cannabis, judge 0.85); a question about damage or harm is answered only by an answer that speaks of harm ("does ketamine damage your brain" got the answer on brain scans during ketamine, judge 0.72, whose near-miss readers had written "Do brain scans show damage in people who use ketamine a lot?"). On the gold set nothing changes (35 best matches: 23 full, 7 partial, 5 wrong; 2 of 126 unanswerable); near-miss questions given the answer they do not get 100 of 1,810 (101); of the editor's 198 probe questions only the ketamine one changes.

**A drug the site has no page on (site 2.28.9, 20 November 2026).** A question that names one (scope.json's names and the names the system
learned) and no drug the site covers is shown only the answers that name it, as best match or related (`build_index.py`, the index's "unc";
`Ranker.tiers` and the page's `insTiers`). "can you get high from nutmeg" was shown the answers on kratom and ibogaine. On the gold set (21
such questions): best matches as before (35: 23 full, 7 partial, 5 wrong); related rows 299 (317), 49% of them a full or partial answer (47%);
questions nobody can answer that are shown rows 20 of 126 (25); near-miss 100 of 1,810 as before. One question helped before is not: "Does CBN
help sleep?" was helped by the answers on cannabis and sleep, which do not name CBN.

And (2.28.9): a question about dying or overdose that names no drug is never answered by an answer about one drug (`Ranker.speaks`, the page's `insSpeaks`): "overdose symptoms" got the answer on meth's acute toxicity as its best match. Nothing changes on the gold set or the near-miss questions. The same rule for every question that names no drug was measured too and not kept: three full answers fewer on the gold set (best matches 32, full 20), though near-miss 90.
