#!/usr/bin/env python3
"""encoders.py: open text encoders tried on our own gold set, on GitHub's machines (docs/AUTOMATION.md, decision 37, stage one).

The senior author, 19 November 2026: "our search engine has to understand human language like an LLM" (17:57); "it should not be
limited" (18:10); "our ai is FUCKING STUPID it does not understand human language well" (20:52). Insight reads a question on the
reader's own device with a small open encoder (all-MiniLM-L6-v2, trained further on our wordings: pharmakon-insight-1). Newer small
encoders of the same size class read far better on public benchmarks. This measures them on OUR task, before any is shipped:

    python3 -I scripts/insight/encoders.py [--request FILE]      (needs site/insight/.cache/index-input.json: node site/build.js first)

For each candidate (MODELS below: Hugging Face repositories with an ONNX file made for browsers, and a licence that allows any use):
the files are fetched (and their sizes and SHA-256 kept), the answers' wordings and short answers and the 400 forum questions of the
gold set are embedded as the page would (at most 128 tokens; the candidate's own pooling), and each question is matched as the
page's first look does (0.7 x the nearest wording + 0.3 x the short answer). Reported, as in scripts/insight/MODELS.md: strict top-1
and top-3 (an answer both blind readers judged to answer the question as asked), lenient top-3 (also partial answers), and how well
the nearest score tells questions we can answer from questions nobody can (AUC; 0.5 is chance). Also: whether the candidate reads
words with the page's own vocabulary (a drop-in model must: site/insight/vendor/vocab.txt) and how long it takes. Nothing is shipped
by this: data/verification/insight/encoders.json is the record; a candidate goes to the page only with its own build and checks.
"""
import sys, os, json, time, math, hashlib, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "verification" / "insight" / "encoders.json"
INPUT = ROOT / "site" / "insight" / ".cache" / "index-input.json"
VENDOR = ROOT / "site" / "insight" / "vendor"

# name: repo, onnx file, pooling ("mean" or "cls"), query prefix, text prefix, licence. Only models whose licence allows any use.
MODELS = {
    "Pharmakon's own model (on the site)": {"local": json.load(open(ROOT / "site" / "insight" / "model.json", encoding="utf-8"))["file"], "pool": "mean", "licence": "Apache-2.0"},
    "all-MiniLM-L6-v2": {"repo": "Xenova/all-MiniLM-L6-v2", "file": "onnx/model_quantized.onnx", "pool": "mean", "licence": "Apache-2.0"},
    "multi-qa-MiniLM-L6-cos-v1": {"repo": "Xenova/multi-qa-MiniLM-L6-cos-v1", "file": "onnx/model_quantized.onnx", "pool": "mean", "licence": "Apache-2.0"},
    "gte-small": {"repo": "Xenova/gte-small", "file": "onnx/model_quantized.onnx", "pool": "mean", "licence": "MIT"},
    "bge-small-en-v1.5": {"repo": "Xenova/bge-small-en-v1.5", "file": "onnx/model_quantized.onnx", "pool": "cls", "licence": "MIT"},
    "e5-small-v2": {"repo": "Xenova/e5-small-v2", "file": "onnx/model_quantized.onnx", "pool": "mean", "q": "query: ", "t": "query: ", "licence": "MIT"},
    "snowflake-arctic-embed-xs": {"repo": "Snowflake/snowflake-arctic-embed-xs", "file": "onnx/model_quantized.onnx", "pool": "cls", "q": "Represent this sentence for searching relevant passages: ", "licence": "Apache-2.0"},
    "snowflake-arctic-embed-s": {"repo": "Snowflake/snowflake-arctic-embed-s", "file": "onnx/model_quantized.onnx", "pool": "cls", "q": "Represent this sentence for searching relevant passages: ", "licence": "Apache-2.0"},
    "mxbai-embed-xsmall-v1": {"repo": "mixedbread-ai/mxbai-embed-xsmall-v1", "file": "onnx/model_quantized.onnx", "pool": "mean", "licence": "Apache-2.0"},
}


def log(*a): print("encoders:", *a, flush=True)


def fetch(name):
    m = MODELS[name]
    if m.get("local"):
        p = VENDOR / m["local"]; return {"onnx": str(p), "tokenizer": None, "vocab": str(VENDOR / "vocab.txt"), "source": "site/insight/vendor"}
    from huggingface_hub import HfApi, hf_hub_download
    info = HfApi().model_info(m["repo"]); files = {s.rfilename for s in info.siblings or []}
    if m["file"] not in files: raise RuntimeError(f"{m['repo']} has no {m['file']}")
    onnx = hf_hub_download(m["repo"], m["file"], revision=info.sha)
    tok = hf_hub_download(m["repo"], "tokenizer.json", revision=info.sha) if "tokenizer.json" in files else None
    vocab = hf_hub_download(m["repo"], "vocab.txt", revision=info.sha) if "vocab.txt" in files else None
    return {"onnx": onnx, "tokenizer": tok, "vocab": vocab, "source": f"huggingface.co/{m['repo']} (commit {info.sha[:8]})"}


class Encoder:
    def __init__(self, name, got):
        import onnxruntime as ort
        from tokenizers import Tokenizer, BertWordPieceTokenizer
        self.m = MODELS[name]; so = ort.SessionOptions(); so.intra_op_num_threads = os.cpu_count() or 4
        self.s = ort.InferenceSession(got["onnx"], so, providers=["CPUExecutionProvider"]); self.inputs = {i.name for i in self.s.get_inputs()}
        if got.get("tokenizer"):
            self.tok = Tokenizer.from_file(got["tokenizer"]); self.tok.no_padding(); self.tok.enable_truncation(128)
        else:
            self.tok = BertWordPieceTokenizer(got["vocab"], lowercase=True); self.tok.enable_truncation(128)

    def __call__(self, texts, prefix=""):
        import numpy as np
        out = []
        for t in texts:
            e = self.tok.encode(prefix + t); ids = np.array([e.ids], dtype=np.int64); mask = np.ones_like(ids)
            feeds = {"input_ids": ids, "attention_mask": mask}
            if "token_type_ids" in self.inputs: feeds["token_type_ids"] = np.zeros_like(ids)
            h = self.s.run(None, feeds)[0][0]
            v = h[0] if self.m["pool"] == "cls" else h.mean(axis=0)
            out.append(v / max(float(np.linalg.norm(v)), 1e-9))
        return np.stack(out).astype("float32")


def gold():
    G = json.load(open(ROOT / "data/verification/insight/gold-sample.json", encoding="utf-8"))["questions"]
    L = [{x["n"]: x for x in json.load(open(ROOT / f"data/verification/insight/gold_reader{r}.json", encoding="utf-8"))["labels"]} for r in ("693", "694")]
    ans = lambda x: set(x.get("answers") or []); part = lambda x: set(x.get("answers") or []) | set(x.get("partly") or [])
    yes = lambda x: bool(part(x)) and not x.get("none")
    rows = []
    for q in G:
        n = q["n"]
        if n not in L[0] or n not in L[1]: continue
        a, b = L[0][n], L[1][n]
        rows.append({"q": q["question"], "strict": ans(a) | ans(b), "lenient": part(a) | part(b), "none": not yes(a) and not yes(b)})
    return rows


def auc(pos, neg):
    if not pos or not neg: return None
    allv = sorted([(v, 1) for v in pos] + [(v, 0) for v in neg]); r = 0.0; rank = 0; i = 0
    while i < len(allv):
        j = i
        while j < len(allv) and allv[j][0] == allv[i][0]: j += 1
        avg = (i + j + 1) / 2.0; r += avg * sum(1 for k in range(i, j) if allv[k][1] == 1); i = j
    return (r - len(pos) * (len(pos) + 1) / 2.0) / (len(pos) * len(neg))


def evaluate(name, enc, A, G):
    import numpy as np
    m = MODELS[name]; t0 = time.time()
    rows, W = [], []
    for i, a in enumerate(A):
        for w in a["wordings"]: rows.append(i); W.append(w)
    Wv = enc(W, m.get("t", "")); Sv = enc([a["short"] for a in A], m.get("t", "")); Qv = enc([g["q"] for g in G], m.get("q", "") if m.get("q") and m.get("t") else "")
    rows = np.array(rows); best_w = np.full((len(G), len(A)), -1.0, dtype=np.float32)
    sims = Qv @ Wv.T
    for i in range(len(A)):
        k = np.where(rows == i)[0]
        if len(k): best_w[:, i] = sims[:, k].max(axis=1)
    score = 0.7 * best_w + 0.3 * (Qv @ Sv.T); ids = [a["id"] for a in A]
    s1 = s3 = l3 = ns = nl = 0; top = []
    for qi, g in enumerate(G):
        order = np.argsort(-score[qi])[:3]; got = [ids[k] for k in order]; top.append(float(score[qi][order[0]]))
        if g["strict"]: ns += 1; s1 += got[0] in g["strict"]; s3 += bool(set(got) & g["strict"])
        if g["lenient"]: nl += 1; l3 += bool(set(got) & g["lenient"])
    can = [top[i] for i, g in enumerate(G) if g["lenient"] and not g["none"]]; cannot = [top[i] for i, g in enumerate(G) if g["none"]]
    return {"strict_top1": round(s1 / max(ns, 1), 3), "strict_top3": round(s3 / max(ns, 1), 3), "lenient_top3": round(l3 / max(nl, 1), 3), "n_strict": ns, "n_lenient": nl,
            "answerable_vs_not_auc": round(auc(can, cannot) or 0, 3), "texts": len(W) + len(A) + len(G), "seconds": round(time.time() - t0, 1)}


def main():
    a = sys.argv[1:]
    req = json.load(open(a[a.index("--request") + 1], encoding="utf-8")) if "--request" in a else {}
    names = [n for n in (req.get("models") or list(MODELS)) if n in MODELS]
    if not INPUT.exists(): sys.exit("encoders: no site/insight/.cache/index-input.json: run node site/build.js first")
    A = [x for x in json.load(open(INPUT, encoding="utf-8"))["answers"] if x.get("wordings") and x.get("short")]
    var = {}
    try: var = json.load(open(ROOT / "data/verification/insight/variants_reader696.json", encoding="utf-8")).get("variants") or {}
    except (OSError, ValueError): pass
    for x in A: x["wordings"] = list(dict.fromkeys(list(x["wordings"]) + [w for w in var.get(x["id"], []) if isinstance(w, str) and w.strip()]))
    G = gold(); ours = (VENDOR / "vocab.txt").read_text(encoding="utf-8").split("\n")
    out = {"_note": "scripts/insight/encoders.py: open text encoders on our own gold set (400 forum questions, two blind readers), matched as the page's first look does (0.7 nearest wording + 0.3 short answer; no judge, no word overlap). Nothing here is shipped.",
           "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "answers": len(A), "gold": len(G), "models": {}}
    for n in names:
        row = out["models"][n] = {"licence": MODELS[n]["licence"]}
        try:
            got = fetch(n); row["source"] = got["source"]; row["bytes"] = os.path.getsize(got["onnx"])
            h = hashlib.sha256(open(got["onnx"], "rb").read()).hexdigest(); row["sha256"] = h
            if got.get("vocab"): row["same_vocab_as_the_page"] = pathlib.Path(got["vocab"]).read_text(encoding="utf-8").split("\n") == ours
            elif got.get("tokenizer"):
                v = json.load(open(got["tokenizer"], encoding="utf-8")).get("model", {}).get("vocab") or {}
                row["same_vocab_as_the_page"] = bool(v) and [k for k, _ in sorted(v.items(), key=lambda kv: kv[1])] == [x for x in ours if x != ""][:len(v)] and len(v) == len([x for x in ours if x != ""])
            row.update(evaluate(n, Encoder(n, got), A, G)); log(n, json.dumps({k: row[k] for k in ("strict_top1", "strict_top3", "lenient_top3", "answerable_vs_not_auc", "seconds")}))
        except Exception as e: row["failed"] = (type(e).__name__ + ": " + str(e))[:300]; log(n, "failed:", row["failed"])
        OUT.parent.mkdir(parents=True, exist_ok=True); json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    log("done: data/verification/insight/encoders.json")


if __name__ == "__main__":
    main()
