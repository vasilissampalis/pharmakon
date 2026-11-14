"""eval_match.py MODELS_DIR [--out FILE]: Pharmakon Insight, phase 1 (docs: the concept "Pharmakon Insight: the site that
thinks with you"). How well do two small open models, run as they would run on a reader's phone, find the checked answer
for real questions people asked on drug forums?

Answers indexed: every answer with plain lines on the site (data/site/simple.json -> claims), with every wording of its
question on the site's pages (data/site/questions.json, and the plain lines' own q) and its short answer.
Questions: the forum harvest (data/verification/questions-*/forums.json), each with `covered_by` = the answers the harvest
coder judged to cover it (fully or partly). These labels are provisional (one coder); the gold set (two blind readers)
comes next. A question counts as answerable if at least one of its covering answers is indexed.

Models (files byte-identical to the official ones; SHA-256 recorded in scripts/insight/MODELS.md):
- minilm: all-MiniLM-L6-v2, quantized ONNX (Xenova), mean pooling, normalized (as sentence-transformers does).
- potion: Model2Vec potion-base-8M, static embeddings, mean of token vectors (no special tokens), normalized.
- lexical: a TF-IDF baseline, standing in for today's word search.
Index variants: q only; q + short answer; max of the two.
Reports: top-1 and top-3 hit rates on answerable questions; for each threshold on the best score, the share of
answerable questions answered right in the top 3 and the share of unanswerable ones given a confident (wrong) match."""
import json, glob, sys, os, re, math, pathlib
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[2]
M = pathlib.Path(sys.argv[1])
S = json.load(open(ROOT / "data/site/simple.json", encoding="utf-8"))["claims"]
QS = json.load(open(ROOT / "data/site/questions.json", encoding="utf-8")); QS.pop("_note", None)
wordings = {}
for slug, groups in QS.items():
    for g in groups:
        for it in g["items"]:
            if len(it) > 1 and it[1]: wordings.setdefault(it[0], []).append(it[1])
ans = []
for k, v in S.items():
    ws = list(dict.fromkeys(([v["q"]] if v.get("q") else []) + wordings.get(k, [])))
    if ws: ans.append((k, ws, v.get("short", "")))
ids = [a[0] for a in ans]; idset = set(ids)
Q = [q for f in sorted(glob.glob(str(ROOT / "data/verification/questions-*/forums.json"))) for q in json.load(open(f, encoding="utf-8"))["questions"]]
def cov(q):
    out = []
    for c in q.get("covered_by") or []:
        cid = c["id"] if isinstance(c, dict) else c
        if cid in idset: out.append(cid)
    return out
tests = [(q["question"], cov(q)) for q in Q if q.get("question")]
answerable = [t for t in tests if t[1]]; unanswerable = [t for t in tests if not t[1]]
print(f"{len(ans)} answers indexed; {len(tests)} forum questions: {len(answerable)} answerable (provisional labels), {len(unanswerable)} not")

from tokenizers import Tokenizer, BertWordPieceTokenizer
import onnxruntime as ort
from safetensors.numpy import load_file

def norm(x): return x / np.maximum(np.linalg.norm(x, axis=-1, keepdims=True), 1e-9)

class MiniLM:
    def __init__(self, d):
        self.tok = BertWordPieceTokenizer(str(d / "vocab.txt"), lowercase=True)
        self.tok.enable_truncation(256); self.tok.enable_padding()
        self.s = ort.InferenceSession(str(d / "all-MiniLM-L6-v2-q8.onnx"), providers=["CPUExecutionProvider"])
        self.inputs = [i.name for i in self.s.get_inputs()]
    def __call__(self, texts):
        out = []
        for i in range(0, len(texts), 64):
            enc = self.tok.encode_batch(texts[i:i + 64])
            ii = np.array([e.ids for e in enc], dtype=np.int64); am = np.array([e.attention_mask for e in enc], dtype=np.int64)
            feed = {"input_ids": ii, "attention_mask": am}
            if "token_type_ids" in self.inputs: feed["token_type_ids"] = np.zeros_like(ii)
            h = self.s.run(None, feed)[0]
            m = am[..., None].astype(np.float32)
            out.append(norm((h * m).sum(1) / np.maximum(m.sum(1), 1e-9)))
        return np.vstack(out)

class Potion:
    def __init__(self, d):
        self.tok = Tokenizer.from_file(str(d / "tokenizer.json"))
        self.E = load_file(str(d / "model.safetensors"))["embeddings"].astype(np.float32)
    def __call__(self, texts):
        out = []
        for t in texts:
            ii = [i for i in self.tok.encode(t, add_special_tokens=False).ids if i < len(self.E)]
            out.append(self.E[ii].mean(0) if ii else np.zeros(self.E.shape[1], np.float32))
        return norm(np.vstack(out))

class Lexical:
    def __init__(self, docs):
        self.tokz = lambda s: re.findall(r"[a-z0-9]+", s.lower())
        self.df = {}
        for d in docs:
            for w in set(self.tokz(d)): self.df[w] = self.df.get(w, 0) + 1
        self.N = len(docs)
    def vec(self, texts):
        vocab = {w: i for i, w in enumerate(self.df)}
        X = np.zeros((len(texts), len(vocab)), np.float32)
        for r, t in enumerate(texts):
            for w in self.tokz(t):
                if w in vocab: X[r, vocab[w]] += math.log(1 + self.N / self.df[w])
        return norm(X)

def evaluate(name, A, T, sims=None):
    sims = T @ A.T if sims is None else sims
    res = {}
    top = np.argsort(-sims, 1)[:, :3]; best = sims.max(1)
    n_ans = len(answerable)
    hit1 = sum(ids[top[i, 0]] in answerable[i][1] for i in range(n_ans)) / n_ans
    hit3 = sum(any(ids[j] in answerable[i][1] for j in top[i]) for i in range(n_ans)) / n_ans
    res = {"top1": round(hit1 * 100, 1), "top3": round(hit3 * 100, 1), "thresholds": []}
    for th in np.round(np.arange(0.2, 0.95, 0.05), 2):
        keep_ans = [i for i in range(n_ans) if best[i] >= th]
        right3 = sum(any(ids[j] in answerable[i][1] for j in top[i]) for i in keep_ans)
        wrong_conf_unans = sum(best[n_ans + k] >= th for k in range(len(unanswerable)))
        wrong_top1_ans = sum(ids[top[i, 0]] not in answerable[i][1] for i in keep_ans)
        res["thresholds"].append({"t": float(th), "answerable_right_top3": round(right3 / n_ans * 100, 1), "answerable_shown": round(len(keep_ans) / n_ans * 100, 1),
                                  "answerable_top1_wrong_when_shown": round(wrong_top1_ans / max(1, len(keep_ans)) * 100, 1),
                                  "unanswerable_confident_match": round(wrong_conf_unans / max(1, len(unanswerable)) * 100, 1)})
    print(f"{name:<22} top1 {res['top1']:5.1f}  top3 {res['top3']:5.1f}")
    return res

texts_T = [t[0] for t in answerable] + [t[0] for t in unanswerable]
report = {"answers": len(ans), "answerable": len(answerable), "unanswerable": len(unanswerable), "models": {}}
flat = [(i, w) for i, a in enumerate(ans) for w in a[1]]   # every wording, with its answer's row
docs_q = [a[1][0] for a in ans]; docs_qs = [" ".join(a[1]) + " " + a[2] for a in ans]
def per_claim(Tv, Wv):
    simw = Tv @ Wv.T
    out = np.full((Tv.shape[0], len(ans)), -1.0, np.float32)
    for col, (i, _) in enumerate(flat): out[:, i] = np.maximum(out[:, i], simw[:, col])
    return out
lex = Lexical(docs_qs + texts_T)
report["models"]["lexical q+short"] = evaluate("lexical q+short", lex.vec(docs_qs), lex.vec(texts_T))
for name, cls, sub in (("minilm", MiniLM, "_clay-design-system_embeddings/package/model"), ("potion", Potion, "_yarflam_potion-base-8m/package/models")):
    enc = cls(M / sub)
    T = enc(texts_T); Wv = enc([w for _, w in flat]); As = enc([a[2] for a in ans])
    simq = per_claim(T, Wv)
    report["models"][name + " questions"] = evaluate(name + " questions", None, T, simq)
    report["models"][name + " questions+short"] = evaluate(name + " questions+short", None, T, np.maximum(simq, T @ As.T))
    sims_max = 0.7 * simq + 0.3 * (T @ As.T)
    # max of q and short: evaluate through a pseudo-index (reuse evaluate by passing precomputed similarities)
    class P: pass
    def ev_sims(nm, sims):
        global evaluate
        A_fake = None
        top = np.argsort(-sims, 1)[:, :3]; best = sims.max(1); n_ans = len(answerable)
        hit1 = sum(ids[top[i, 0]] in answerable[i][1] for i in range(n_ans)) / n_ans
        hit3 = sum(any(ids[j] in answerable[i][1] for j in top[i]) for i in range(n_ans)) / n_ans
        print(f"{nm:<22} top1 {hit1*100:5.1f}  top3 {hit3*100:5.1f}")
        return {"top1": round(hit1 * 100, 1), "top3": round(hit3 * 100, 1)}
    report["models"][name + " 0.7q+0.3short"] = evaluate(name + " 0.7q+0.3short", None, T, sims_max)
out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
if out: json.dump(report, open(out, "w", encoding="utf-8"), indent=1)
