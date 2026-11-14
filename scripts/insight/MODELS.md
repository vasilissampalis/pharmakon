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
