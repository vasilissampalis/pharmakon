"""judge.py MODELS_DIR [--model FILE --name LABEL] [--no-bge] [--no-cross] [--cache DIR] [--out FILE]: Pharmakon Insight 2.3, research harness (15 November 2026).

Question: how do we make Insight tell "this answers what was asked" from "this is only near it", with models that run
on the reader's own device and with examples that are ours? Measured on the gold set (400 real forum questions, two
blind readers; never used for training). Candidates on the gold set are the 356 answers the readers labelled against.

What is tried:
  A. the 2.2.0 scoring (0.7 best wording + 0.3 short answer + 0.2 word overlap, drug names expanded);
  B. A with the hurried wordings of the near-miss round (`more`) added;
  C. a second encoder (bge-small-en-v1.5, int8) in place of MiniLM;
  D. a cross-encoder (ms-marco-MiniLM-L-6-v2) re-ordering A's first 10;
  E. a judge trained on our own examples (leave-one-out features from the wordings and the near-miss questions):
     logistic regression and gradient boosting, used to re-order A's first 10 and to say "best match" or "related".
For each: strict and lenient top-1 and top-3, and how well the first answer's score separates questions the site
answers from questions it does not (area under the curve, and best-match precision at several cut-offs)."""
import sys, json, re, math, pathlib, hashlib, pickle, itertools
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[2]
M = pathlib.Path(sys.argv[1])
arg = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
CACHE = pathlib.Path(arg("--cache", "/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/insight/judge-cache")); CACHE.mkdir(parents=True, exist_ok=True)
V = ROOT / "data/verification/insight"
from tokenizers import Tokenizer, BertWordPieceTokenizer
import onnxruntime as ort
def norm(x): return x / np.maximum(np.linalg.norm(x, axis=-1, keepdims=True), 1e-9)

# ---------- data ----------
A = json.load(open(V / "answers-2026-11-15.json", encoding="utf-8"))
SKIP = set(A.get("skip") or []); A = A["answers"]
ids = [a["id"] for a in A]; ix = {a: i for i, a in enumerate(ids)}
OLD = {a["id"] for a in json.load(open(V / "answers.json", encoding="utf-8"))["answers"]}
var = json.load(open(V / "variants_reader696.json", encoding="utf-8"))["variants"]
near, more = {}, {}
for r in ("707", "708"):
    f = V / f"nearmiss_{r}.json"
    if f.exists():
        for k, v in json.load(open(f, encoding="utf-8"))["items"].items(): near[k] = v.get("near") or []; more[k] = v.get("more") or []
print(f"{len(A)} answers ({len(OLD & set(ids))} in the gold catalogue); variants for {len(var)}; near-miss for {len(near)} answers")
G = json.load(open(V / "gold-sample.json", encoding="utf-8"))["questions"]
La = {x["n"]: x for x in json.load(open(V / "gold_reader693.json", encoding="utf-8"))["labels"]}
Lb = {x["n"]: x for x in json.load(open(V / "gold_reader694.json", encoding="utf-8"))["labels"]}
ns = [q["n"] for q in G if q["n"] in La and q["n"] in Lb]; qtext = {q["n"]: q["question"] for q in G}
full = lambda x: set(x.get("answers") or []); part = lambda x: full(x) | set(x.get("partly") or [])
strict = {n: full(La[n]) | full(Lb[n]) for n in ns}; lenient = {n: part(La[n]) | part(Lb[n]) for n in ns}
yes = lambda x: bool(part(x)) and not x.get("none")
none_both = {n for n in ns if not yes(La[n]) and not yes(Lb[n])}; yes_both = {n for n in ns if yes(La[n]) and yes(Lb[n])}
AL = json.load(open(ROOT / "data/site/aliases.json", encoding="utf-8")); SUB = json.load(open(ROOT / "data/site/substances.json", encoding="utf-8"))
names = {s["slug"]: ({s["slug"].replace("-", " ")} | {p.strip().lower() for p in re.split(r"[()/,;]| and ", s["name"]) if len(p.strip()) >= 3} | {x.lower() for x in AL.get(s["slug"], []) if len(x) >= 3}) for s in SUB}
pat = {k: re.compile(r"\b(" + "|".join(re.escape(n) for n in sorted(v, key=len, reverse=True)) + r")\b") for k, v in names.items()}
canon = {s["slug"]: s["name"].split(" (")[0] for s in SUB}
def drugs_in(t): return {k for k, p in pat.items() if p.search(t.lower())}
def expand(t):
    d = drugs_in(t); ex = [canon[x] for x in sorted(d) if canon[x].lower() not in t.lower()]
    return t + (" (" + ", ".join(ex) + ")" if ex else "")
pages = [set(a["pages"]) & set(names) for a in A]
TYPES = [("count", r"^(how (many|much|common|often|likely)|what (percent|share|are the (odds|chances)))"), ("long", r"^how long|how soon|when (does|do|will)"),
         ("how", r"^how (do|does|can|could|did|is|are|would|to)\b"), ("why", r"^why"), ("yesno", r"^(can|could|does|do|did|is|are|was|were|will|would|should|has|have|am)\b"),
         ("what", r"^(what|which|who|where)")]
def qtype(t):
    t = t.strip().lower()
    for k, p in TYPES:
        if re.search(p, t): return k
    return "other"

# ---------- encoders (with a disk cache per model) ----------
class Enc:
    def __init__(self, name, model, tok, pool, vocab=False, prefix=""):
        self.name, self.pool, self.prefix = name, pool, prefix
        self.tok = BertWordPieceTokenizer(str(tok), lowercase=True) if vocab else Tokenizer.from_file(str(tok))
        self.tok.enable_truncation(256); self.tok.enable_padding()
        so = ort.SessionOptions(); so.intra_op_num_threads = 2
        self.s = ort.InferenceSession(str(model), so, providers=["CPUExecutionProvider"]); self.inputs = [i.name for i in self.s.get_inputs()]
        self.f = CACHE / f"{name}.pkl"; self.c = pickle.load(open(self.f, "rb")) if self.f.exists() else {}
    def __call__(self, texts, query=False):
        key = lambda t: (self.prefix + t) if query else t
        todo = [t for t in dict.fromkeys(key(t) for t in texts) if t not in self.c]
        for i in range(0, len(todo), 32):
            b = todo[i:i + 32]; e = self.tok.encode_batch(b)
            ii = np.array([x.ids for x in e], np.int64); am = np.array([x.attention_mask for x in e], np.int64)
            feed = {"input_ids": ii, "attention_mask": am}
            if "token_type_ids" in self.inputs: feed["token_type_ids"] = np.zeros_like(ii)
            h = self.s.run(None, feed)[0]
            if self.pool == "cls": v = h[:, 0]
            else: m = am[..., None].astype(np.float32); v = (h * m).sum(1) / np.maximum(m.sum(1), 1e-9)
            for t, x in zip(b, norm(v)): self.c[t] = x.astype(np.float32)
        if todo: pickle.dump(self.c, open(self.f, "wb"))
        return np.vstack([self.c[key(t)] for t in texts])
class Cross:
    def __init__(self, model, tok):
        self.tok = Tokenizer.from_file(str(tok)); self.tok.enable_truncation(256); self.tok.enable_padding()
        so = ort.SessionOptions(); so.intra_op_num_threads = 2
        self.s = ort.InferenceSession(str(model), so, providers=["CPUExecutionProvider"]); self.inputs = [i.name for i in self.s.get_inputs()]
        self.f = CACHE / "cross.pkl"; self.c = pickle.load(open(self.f, "rb")) if self.f.exists() else {}
    def __call__(self, pairs):
        todo = [p for p in dict.fromkeys(pairs) if p not in self.c]
        for i in range(0, len(todo), 32):
            b = todo[i:i + 32]; e = self.tok.encode_batch(b)
            feed = {"input_ids": np.array([x.ids for x in e], np.int64), "attention_mask": np.array([x.attention_mask for x in e], np.int64)}
            if "token_type_ids" in self.inputs: feed["token_type_ids"] = np.array([x.type_ids for x in e], np.int64)
            for p, x in zip(b, self.s.run(None, feed)[0][:, 0]): self.c[p] = float(x)
        if todo: pickle.dump(self.c, open(self.f, "wb"))
        return np.array([self.c[p] for p in pairs], np.float32)
class Lexical:
    def __init__(self, docs):
        self.tokz = lambda s: re.findall(r"[a-z0-9]+", s.lower()); self.df = {}
        for d in docs:
            for w in set(self.tokz(d)): self.df[w] = self.df.get(w, 0) + 1
        self.N = len(docs); self.vocab = {w: i for i, w in enumerate(self.df)}
    def vec(self, texts):
        X = np.zeros((len(texts), len(self.vocab)), np.float32)
        for r, t in enumerate(texts):
            for w in self.tokz(t):
                if w in self.vocab: X[r, self.vocab[w]] += math.log(1 + self.N / self.df[w])
        return norm(X)

# ---------- index ----------
def build(use_more):
    P = [list(dict.fromkeys(a["questions"] + var.get(a["id"], []) + (more.get(a["id"], []) if use_more else []))) for a in A]
    N = [list(dict.fromkeys(near.get(a["id"], []))) for a in A]
    return P, N
docs = [" ".join(a["questions"]) + " " + a["short"] for a in A]
lex = Lexical(docs); Ldoc = lex.vec(docs)
def seg_max(S, owner, n, k=1):
    """per answer, the k-th largest similarity over its texts (S: queries x texts; owner: text -> answer row)"""
    out = np.full((S.shape[0], n), -1.0, np.float32); out2 = np.full((S.shape[0], n), -1.0, np.float32)
    order = np.argsort(owner, kind="stable"); owner_s = owner[order]; starts = np.r_[0, np.flatnonzero(np.diff(owner_s)) + 1]
    for s, e in zip(starts, np.r_[starts[1:], len(owner_s)]):
        blk = S[:, order[s:e]]; a = owner_s[s]
        if blk.shape[1] == 1: out[:, a] = blk[:, 0]
        else:
            srt = np.sort(blk, 1); out[:, a] = srt[:, -1]; out2[:, a] = srt[:, -2]
    return out, out2

def features(enc, queries, P, N, self_of=None):
    """Feature tensor [q, a, f] and the base score. self_of[q] = (kind, answer row, text) removes the query's own text
    from that answer's examples (leave-one-out) when the query is one of our own examples."""
    Ptxt = [w for ws in P for w in ws]; Pown = np.array([i for i, ws in enumerate(P) for _ in ws])
    Ntxt = [w for ws in N for w in ws]; Nown = np.array([i for i, ws in enumerate(N) for _ in ws])
    Q = enc([expand(q) for q in queries], query=True); W = enc(Ptxt); Sh = enc([a["short"] for a in A])
    SP = Q @ W.T
    if self_of:
        pos = {}
        for j, w in enumerate(Ptxt): pos.setdefault((int(Pown[j]), w), j)
        for qi, so in enumerate(self_of):
            if so and so[0] == "P" and (so[1], so[2]) in pos: SP[qi, pos[(so[1], so[2])]] = -1.0
    p1, p2 = seg_max(SP, Pown, len(A))
    if len(Ntxt):
        NW = enc(Ntxt); SN = Q @ NW.T
        if self_of:
            posn = {}
            for j, w in enumerate(Ntxt): posn.setdefault((int(Nown[j]), w), j)
            for qi, so in enumerate(self_of):
                if so and so[0] == "N" and (so[1], so[2]) in posn: SN[qi, posn[(so[1], so[2])]] = -1.0
        n1, _ = seg_max(SN, Nown, len(A)); n1 = np.maximum(n1, 0)
    else: n1 = np.zeros_like(p1)
    sh = Q @ Sh.T; lx = lex.vec(queries) @ Ldoc.T
    base = 0.7 * p1 + 0.3 * sh + 0.2 * lx
    qd = [drugs_in(q) for q in queries]
    dr = np.zeros_like(p1)
    for qi, d in enumerate(qd):
        if d:
            for ai, pg in enumerate(pages): dr[qi, ai] = 1.0 if (pg & d) else (-1.0 if pg else 0.0)
    # the type of the nearest positive wording against the type of the question
    arg = np.zeros(SP.shape[0], int); ty = np.zeros_like(p1); qt = [qtype(q) for q in queries]; wt = [qtype(w) for w in Ptxt]
    order = np.argsort(Pown, kind="stable"); owner_s = Pown[order]; starts = np.r_[0, np.flatnonzero(np.diff(owner_s)) + 1]
    for s, e in zip(starts, np.r_[starts[1:], len(owner_s)]):
        cols = order[s:e]; best = cols[np.argmax(SP[:, cols], 1)]
        ty[:, owner_s[s]] = np.array([1.0 if wt[b] == qt[qi] else 0.0 for qi, b in enumerate(best)])
    top = base.max(1, keepdims=True); srt = np.sort(base, 1); margin = (srt[:, -1] - srt[:, -2])[:, None]
    ql = np.array([min(len(q.split()), 20) / 20 for q in queries], np.float32)[:, None]
    F = np.stack([p1, np.maximum(p2, 0), sh, lx, dr, n1, p1 - n1, ty, base - top, np.where(base >= top - 1e-9, margin, 0), np.broadcast_to(ql, p1.shape), base], -1)
    return F, base
FN = ["best wording", "2nd wording", "short answer", "word overlap", "drug named", "nearest near-miss", "wording minus near-miss", "same kind of question", "behind the first", "lead if first", "question length", "base score"]

# ---------- measures on the gold set ----------
gq = [qtext[n] for n in ns]; oldmask = np.array([a in OLD for a in ids])
SPLIT = {"dev": lambda n: n % 2 == 1, "test": lambda n: n % 2 == 0, "all": lambda n: True}   # odd-numbered gold questions choose a setting, even-numbered ones report it
def gold_report(name, score, verdict=None, cuts=(0.5, 0.6, 0.7, 0.8, 0.9), split="all", quiet=False):
    """score: [gold question, answer] for ordering; verdict: [gold question, answer] confidence that it answers (default: score)."""
    s = np.where(oldmask[None, :], score, -9.0); v = s if verdict is None else np.where(oldmask[None, :], verdict, -9.0)
    top = np.argsort(-s, 1)[:, :3]; first = top[:, 0]; use = SPLIT[split]
    S_ = [k for k, n in enumerate(ns) if strict[n] and use(n)]; L_ = [k for k, n in enumerate(ns) if lenient[n] and use(n)]; NB = [k for k, n in enumerate(ns) if n in none_both and use(n)]
    ALLK = np.array([k for k, n in enumerate(ns) if use(n)])
    s1 = np.mean([ids[first[k]] in strict[ns[k]] for k in S_]); s3 = np.mean([any(ids[j] in strict[ns[k]] for j in top[k]) for k in S_])
    l1 = np.mean([ids[first[k]] in lenient[ns[k]] for k in L_]); l3 = np.mean([any(ids[j] in lenient[ns[k]] for j in top[k]) for k in L_])
    conf = v[np.arange(len(ns)), first]
    # does the first answer's confidence separate "the first answer fully answers" from everything else?
    y = np.array([ids[first[k]] in strict[ns[k]] for k in range(len(ns))]); auc = auc_of(conf[ALLK], y[ALLK])
    y2 = np.array([ids[first[k]] in lenient[ns[k]] for k in range(len(ns))]); auc2 = auc_of(conf[ALLK], y2[ALLK])
    line = f"{name:<44} [{split}] strict top1 {100*s1:5.1f} top3 {100*s3:5.1f} (n={len(S_)}) | lenient top1 {100*l1:5.1f} top3 {100*l3:5.1f} (n={len(L_)}) | AUC full {auc:.3f} any {auc2:.3f}"
    print(line); rows = []
    if not quiet:
        for q in (0.2, 0.3, 0.4, 0.5):   # cut-offs set by the share of the questions that get a "best match"
            t = np.quantile(conf[ALLK], 1 - q); shown = conf >= t
            rows.append((q, t, y[ALLK][shown[ALLK]].mean(), y2[ALLK][shown[ALLK]].mean(), np.mean([shown[k] for k in NB]), np.mean([shown[k] and y[k] for k in S_])))
        print("    best match shown for | cut | first answer answers in full | in full or part | shown on unanswerable | strict questions answered as best")
        for q, t, a_, b_, c_, d_ in rows: print(f"      {100*q:3.0f}% of questions | {t:6.3f} | {100*a_:5.1f}% | {100*b_:5.1f}% | {100*c_:5.1f}% | {100*d_:5.1f}%")
    return {"name": name, "split": split, "s1": s1, "s3": s3, "l1": l1, "l3": l3, "auc": auc, "auc_any": auc2}
def auc_of(score, y):
    y = np.asarray(y, bool); pos, neg = score[y], score[~y]
    if not len(pos) or not len(neg): return float("nan")
    r = np.argsort(np.argsort(np.r_[pos, neg])) + 1
    return (r[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))

if __name__ == "__main__":
    res = []
    mini = Enc(arg("--name", "minilm"), arg("--model", str(M / "_clay-design-system_embeddings/package/model/all-MiniLM-L6-v2-q8.onnx")), M / "_clay-design-system_embeddings/package/model/vocab.txt", "mean", vocab=True)   # --model FILE --name LABEL: another encoder file with the same tokenizer
    P0, N0 = build(False); P1, N1 = build(True)
    F0, b0 = features(mini, gq, P0, [[] for _ in A]); res.append(gold_report("A. 2.2.0 scoring (MiniLM)", b0))
    if more:
        F1, b1 = features(mini, gq, P1, [[] for _ in A]); res.append(gold_report("B. A + hurried wordings", b1))
    else: F1, b1 = F0, b0
    Puse = P1 if more else P0
    bge_dir = M / "_impro-plugin-semantic-mute-model/package"
    if (bge_dir / "bge-small-en-v1.5-q8.onnx").exists() and "--no-bge" not in sys.argv:
        for label, pre in (("no prefix", ""), ("query prefix", "Represent this sentence for searching relevant passages: ")):
            bge = Enc("bge-" + ("p" if pre else "n"), bge_dir / "bge-small-en-v1.5-q8.onnx", bge_dir / "bge-small-en-v1.5-tokenizer.json", "cls", prefix=pre)
            bge.c.update(pickle.load(open(CACHE / "bge-docs.pkl", "rb")) if (CACHE / "bge-docs.pkl").exists() else {})
            Fb, bb = features(bge, gq, Puse, [[] for _ in A]); res.append(gold_report(f"C. bge-small-en-v1.5 ({label})", bb))
            res.append(gold_report(f"C2. MiniLM + bge ({label}), mean", (b1 + bb) / 2))
    ce_dir = M / "_kontexta-reranker-model/package/models/Xenova/ms-marco-MiniLM-L-6-v2"
    if (ce_dir / "onnx/model.onnx").exists() and "--no-cross" not in sys.argv:
        ce = Cross(ce_dir / "onnx/model.onnx", ce_dir / "tokenizer.json")
        K = 10; s = np.where(oldmask[None, :], b1, -9.0); cand = np.argsort(-s, 1)[:, :K]
        for label, ptxt in (("question + short answer", lambda a: a["questions"][0] + " " + a["short"]), ("short answer + but", lambda a: a["short"] + " " + a["but"])):
            pairs = [(gq[k], ptxt(A[j])) for k in range(len(gq)) for j in cand[k]]
            sc = ce(pairs).reshape(len(gq), K); full_ = np.full_like(b1, -30.0)
            for k in range(len(gq)): full_[k, cand[k]] = sc[k]
            res.append(gold_report(f"D. cross-encoder re-orders 10 ({label})", full_))
            z = 1 / (1 + np.exp(-full_)); res.append(gold_report(f"D2. base + 0.3 x cross-encoder ({label})", b1 + 0.3 * z * (full_ > -29), verdict=z))
            if label.startswith("question"): CEg = full_
    # ----- E. a judge trained on our own examples -----
    if near:
        from sklearn.linear_model import LogisticRegression
        from sklearn.ensemble import HistGradientBoostingClassifier
        qs, self_of, lab = [], [], []      # our own examples as questions: positives (label by their answer) and near-misses
        # --judge-on-val: only the answers a fine-tuned encoder never trained on (the same 15% finetune.py holds out), so the
        # judge learns from scores as they look for questions the encoder has not seen
        only_val = "--judge-on-val" in sys.argv; held = lambda a: int(hashlib.sha1(a["id"].encode()).hexdigest(), 16) % 100 < 15
        for ai, a in enumerate(A):
            if only_val and not held(a): continue
            for w in Puse[ai]:
                if w in a["questions"]: continue   # site questions stay in the index always
                qs.append(w); self_of.append(("P", ai, w)); lab.append((ai, 1))
            for w in N1[ai]: qs.append(w); self_of.append(("N", ai, w)); lab.append((ai, 0))
        print(f"training questions: {len(qs)} ({sum(1 for _, y in lab if y)} wordings, {sum(1 for _, y in lab if not y)} near-misses)")
        Ft, bt = features(mini, qs, Puse, N1, self_of=self_of)
        X, y, grp = [], [], []
        rng = np.random.default_rng(7)
        for qi, (ai, yy) in enumerate(lab):
            X.append(Ft[qi, ai]); y.append(yy); grp.append(ai)          # the pair itself
            if yy == 1:                                                   # a wording against the wrong answers that rank highest for it
                for j in np.argsort(-bt[qi])[:4]:
                    if j != ai: X.append(Ft[qi, j]); y.append(0); grp.append(ai)
        X = np.array(X, np.float32); y = np.array(y); grp = np.array(grp)
        print(f"training pairs: {len(y)} ({int(y.sum())} answer, {int((1 - y).sum())} do not)")
        Fg, bg = features(mini, gq, Puse, N1)
        res.append(gold_report("E0. base with near-miss examples in view (wording - 0.5 x excess near-miss)", bg - 0.5 * np.maximum(Fg[..., 5] - Fg[..., 0] + 0.02, 0)))
        mu, sd = X.mean(0), X.std(0) + 1e-6
        lr = LogisticRegression(C=1.0, max_iter=2000).fit((X - mu) / sd, y)
        print("logistic weights:", {n: round(float(w), 2) for n, w in zip(FN, lr.coef_[0])}, "bias", round(float(lr.intercept_[0]), 2))
        pg = lr.predict_proba(((Fg - mu) / sd).reshape(-1, Fg.shape[-1]))[:, 1].reshape(Fg.shape[:2])
        res.append(gold_report("E1. logistic judge orders and judges", pg))
        res.append(gold_report("E2. base orders, logistic judge judges", bg, verdict=pg))
        res.append(gold_report("E3. base + 0.3 x judge orders, judge judges", bg + 0.3 * pg, verdict=pg))
        gb = HistGradientBoostingClassifier(max_depth=3, max_iter=200, learning_rate=0.06, random_state=7).fit(X, y)
        pb = gb.predict_proba(Fg.reshape(-1, Fg.shape[-1]))[:, 1].reshape(Fg.shape[:2])
        res.append(gold_report("E4. boosted judge orders and judges", pb))
        res.append(gold_report("E5. base + 0.3 x boosted judge", bg + 0.3 * pb, verdict=pb))
        if "CEg" in dir():
            z = 1 / (1 + np.exp(-CEg)); res.append(gold_report("F. base + 0.3 judge + 0.3 cross-encoder", bg + 0.3 * pg + 0.3 * z * (CEg > -29), verdict=(pg + z) / 2))
        json.dump({"features": FN, "mu": mu.tolist(), "sd": sd.tolist(), "w": lr.coef_[0].tolist(), "b": float(lr.intercept_[0])}, open(CACHE / "judge-lr.json", "w"))
    out = arg("--out")
    if out: json.dump(res, open(out, "w"), indent=1)
