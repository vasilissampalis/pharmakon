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
