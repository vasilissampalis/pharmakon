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
