"""judge2.py IN.json INDEX.json [--save FILE] [--cv 5]: does a judge trained on our own examples say "this answers what was
asked" better than two thresholds? (Pharmakon Insight 2.3, 15 November 2026)

The page's rule (scripts/insight/build_index.py, class Ranker) calls an answer a best match when its first look and its
topic score both pass a threshold. Measured on the gold set, that best match is wrong for about one question in four.
Here the same numbers the page already computes for the first candidate, and a few more it can compute for free, go into
a small logistic regression trained ONLY on our own examples:
  yes: a way of asking (phrasings writer 696, the near-miss readers' hurried wordings) against its own answer, with that
       wording taken out of the index first (leave-one-out);
  no:  a near-miss question (readers 707 and 708: "sounds close, is not answered by this answer") against that answer;
       and a way of asking against the other answers that rank highest for it.
No gold question is used for training. The gold set then answers two questions, with its odd-numbered questions choosing
the cut (dev) and its even-numbered ones reporting it (test):
  - at the same number of best matches, is the judge's best match wrong less often than the thresholds'?
  - how often does a question nobody can answer get a best match?
IN.json is the build's input (site/insight/.cache/index-input.json), INDEX.json the index made from it with the model
under test. Everything is embedded by the page's own runtime (build_index.embed_all), so the numbers are the page's."""
import sys, json, glob, pathlib, re, hashlib
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_index as bi
ROOT = bi.ROOT
args = [a for a in sys.argv[1:] if not a.startswith("--")]
opt = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
A = json.load(open(args[0], encoding="utf-8"))["answers"]; D = json.load(open(args[1], encoding="utf-8"))
R = bi.Ranker(D); n = R.n; idx = {a: i for i, a in enumerate(R.ids)}
var, more, near = bi.people_wordings()
# the index's wordings, in the index's order (as build_index.main lists them)
W_txt, rows = [], []
for i, a in enumerate(A):
    for w in dict.fromkeys([w for w in a["wordings"] if w] + [w for w in var.get(a["id"], []) if isinstance(w, str) and w.strip()] + more.get(a["id"], [])):
        rows.append(i); W_txt.append(w)
rows = np.array(rows); assert len(rows) == len(R.rows) and (rows == R.rows).all(), "index and input disagree"
site = [set(a["wordings"]) for a in A]
TYPES = [("count", r"^(how (many|much|common|often|likely)|what (percent|share|are the (odds|chances)))"), ("long", r"^how long|how soon|when (does|do|will)"),
         ("how", r"^how (do|does|can|could|did|is|are|would|to)\b"), ("why", r"^why"), ("yesno", r"^(can|could|does|do|did|is|are|was|were|will|would|should|has|have|am)\b"),
         ("what", r"^(what|which|who|where)")]
def qtype(t):
    t = t.strip().lower()
    for k, p in TYPES:
        if re.search(p, t): return k
    return "other"
W_type = [qtype(w) for w in W_txt]
FEATS = ["best wording", "second wording", "short answer", "word overlap", "topic", "lead over the next answer", "same kind of question", "question length", "drugs named"]
LEAD_ALL = "--lead-all" in sys.argv
NF = 6 if "--six" in sys.argv else len(FEATS)   # --six: only the six numbers the page has at hand for its first candidate
FEATS = FEATS[:NF]

VEC = {}
def learn(questions):
    """One pass through the page's runtime for every text these questions need (the cache file is read once, not per question)."""
    need = []
    for q in questions:
        f, m, _ = R.texts(q); need += [f, m]
    need = [x for x in dict.fromkeys(need) if x not in VEC]
    if need:
        for x, v in zip(need, bi.embed_all(need)): VEC[x] = v
def look(q, drug=None, drop=None):
    """Everything the page computes for a question, per answer. drop: a row of the index to leave out (the question is
    that wording itself)."""
    full, masked, groups = R.texts(q, drug)
    v, mv = VEC[full], VEC[masked]
    sw, sm = R.W @ v, R.M @ mv
    if drop is not None: sw[drop] = -1.0; sm[drop] = -1.0
    bw = np.full(n, -1.0, np.float32); bm = np.full(n, -1.0, np.float32); arg = np.zeros(n, int)
    order = np.argsort(-sw, kind="stable"); seen = np.zeros(n, bool); bw2 = np.full(n, -1.0, np.float32)
    for k in order:                      # best and second-best wording of each answer
        r = rows[k]
        if not seen[r]: seen[r] = True; bw[r] = sw[k]; arg[r] = k
        elif bw2[r] < 0: bw2[r] = sw[k]
    np.maximum.at(bm, rows, sm)
    sh = R.S @ v; lx = R.lex.sims(q)
    plain = R.wt["q"] * bw + R.wt["short"] * sh + R.wt["words"] * lx
    ok = np.array([all(any(s in R.about[i] for s in g) for g in groups) for i in range(n)])
    by = plain + R.wt["topic"] * bm; key = by + R.wt["same"] * ok
    qt = qtype(q); ql = min(len(q.split()), 20) / 20.0
    def feats(c):
        # the next answer: among the answers about every drug the question names (the others cannot be a best match
        # anyway); --lead-all: among all answers
        el = np.ones(n, bool) if LEAD_ALL else ok.copy(); el[c] = False
        lead = float(by[c] - (by[el].max() if el.any() else 0.0))
        return [float(bw[c]), float(max(bw2[c], 0.0)), float(sh[c]), float(lx[c]), float(bm[c]), lead, 1.0 if W_type[arg[c]] == qt else 0.0, ql, float(min(len(groups), 2))][:NF]
    return {"plain": plain, "topic": bm, "ok": ok, "key": key, "by": by, "feats": feats, "groups": groups}

# ---------- our own examples ----------
texts = []
people = [(k, int(rows[k]), w) for k, w in enumerate(W_txt) if w not in site[rows[k]]]
nm = [(q, idx[a]) for a, qs in sorted(near.items()) if a in idx for q in qs]
# --teachers (19 November 2026, decision 41): the teachers' ways of asking that are NOT in the index, as more examples of a question and the answer
# it asks for. The encoder never learned them and the index does not hold them, so the judge sees the numbers a new way of asking really gets (our
# own wordings, which the encoder learned, look easier than a stranger's question does); and their near-miss questions, as more of those.
extra, extra_nm = [], []
if "--teachers" in sys.argv:
    have = set(W_txt)
    for f in (ROOT / "data/verification/insight/variants_teacher.json", ROOT / "data/auto/insight/teachers.json"):
        try: d = json.load(open(f, encoding="utf-8"))
        except (OSError, ValueError): continue
        for a, ws in (d.get("variants") or {}).items():
            if a in idx: extra += [(idx[a], w) for w in ((x.get("w") if isinstance(x, dict) else x) for x in ws) if isinstance(w, str) and w.strip() and w not in have]
        for a, ws in (d.get("near") or {}).items():
            if a in idx: extra_nm += [(w, idx[a]) for w in ((x.get("w") if isinstance(x, dict) else x) for x in ws) if isinstance(w, str) and w.strip()]
    extra = list(dict.fromkeys(extra)); nm = nm + [x for x in dict.fromkeys(extra_nm) if x not in set(nm)]
learn([w for _, _, w in people] + [q for q, _ in nm] + [w for _, w in extra])
X, y, grp, kind = [], [], [], []
for k, i, w in people:
    L = look(w, drop=k)
    X.append(L["feats"](i)); y.append(1); grp.append(i); kind.append("wording")
    for j in [int(j) for j in np.argsort(-L["key"], kind="stable") if j != i][:3]:
        X.append(L["feats"](j)); y.append(0); grp.append(i); kind.append("other answer")
for i, w in extra:
    L = look(w)
    X.append(L["feats"](i)); y.append(1); grp.append(i); kind.append("wording")
    for j in [int(j) for j in np.argsort(-L["key"], kind="stable") if j != i][:3]:
        X.append(L["feats"](j)); y.append(0); grp.append(i); kind.append("other answer")
for q, i in nm:
    L = look(q); X.append(L["feats"](i)); y.append(0); grp.append(i); kind.append("near-miss")
X = np.array(X, np.float32); y = np.array(y); grp = np.array(grp); kind = np.array(kind)
print(f"model {D['model']}: training pairs {len(y)}: {int(y.sum())} wordings against their own answer, {int((kind == 'near-miss').sum())} near-miss questions, {int((kind == 'other answer').sum())} wordings against other answers")
from sklearn.linear_model import LogisticRegression
mu, sd = X.mean(0), X.std(0) + 1e-6
def fit(Xa, ya): return LogisticRegression(C=1.0, max_iter=3000).fit((Xa - mu) / sd, ya)
def prob(m, Xa): return m.predict_proba((np.asarray(Xa, np.float32).reshape(-1, X.shape[1]) - mu) / sd)[:, 1]
# out-of-fold on our own examples (folds by answer): how well does it separate a wording from a near-miss it never saw?
K = int(opt("--cv", "5")); fold = np.array([int(hashlib.sha1(R.ids[g].encode()).hexdigest(), 16) % K for g in grp]); oof = np.zeros(len(y))
for f in range(K):
    m = fit(X[fold != f], y[fold != f]); oof[fold == f] = prob(m, X[fold == f])
def auc(score, lab):
    lab = np.asarray(lab, bool); pos, neg = score[lab], score[~lab]
    r = np.argsort(np.argsort(np.r_[pos, neg])) + 1
    return (r[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))
wn = (kind == "wording") | (kind == "near-miss")
print(f"our own examples, answers not seen in training ({K} folds): wording against near-miss, area under the curve: judge {auc(oof[wn], y[wn]):.3f}; first look alone {auc((R.wt['q'] * X[wn, 0] + R.wt['short'] * X[wn, 2] + R.wt['words'] * X[wn, 3]), y[wn]):.3f}; topic alone {auc(X[wn, 4], y[wn]):.3f}")
J = fit(X, y)
print("judge weights (on standardized numbers):", {f: round(float(w), 2) for f, w in zip(FEATS, J.coef_[0])}, "bias", round(float(J.intercept_[0]), 2))

# ---------- the gold set ----------
G = json.load(open(ROOT / "data/verification/insight/gold-sample.json", encoding="utf-8"))["questions"]
readers = [json.load(open(f, encoding="utf-8"))["labels"] for f in sorted(glob.glob(str(ROOT / "data/verification/insight/gold_reader*.json")))]
lab = {}
for Rd in readers:
    for x in Rd: lab.setdefault(x["n"], []).append(x)
tests = []
for g in G:
    ls = lab.get(g["n"], [])
    if len(ls) < len(readers): continue
    full = {a for x in ls for a in x.get("answers", []) if a in idx}; part = {a for x in ls for a in x.get("partly", []) if a in idx} - full
    tests.append((g["n"], g["question"], full, part, all(x.get("none") for x in ls)))
learn([q for _, q, _, _, _ in tests])
rowsG = []
for nq, q, full, part, un in tests:
    L = look(q); c = int(np.argsort(-L["key"], kind="stable")[0]); a = R.ids[c]
    best, related, _ = R.tiers(L["plain"], L["topic"], L["groups"], L["feats"])   # 2.3: the page's rule is now the judge of model.json, given these six numbers
    rowsG.append({"n": nq, "cand": a, "ok": bool(L["ok"][c]), "p": float(prob(J, [L["feats"](c)])[0]), "plain": float(L["plain"][c]), "topic": float(L["topic"][c]),
                  "full": a in full, "part": a in part, "un": un, "has_full": bool(full), "rule": bool(best) and R.ids[best[0]] == a, "rule_any": bool(best)})
def report(label, pick, rs):
    b = [r for r in rs if pick(r)]; nb = len(b); f = sum(r["full"] for r in b); p = sum(r["part"] for r in b); w = nb - f - p
    nun = sum(r["un"] for r in rs); nfull = sum(r["has_full"] for r in rs)
    print(f"  {label:<46} best match for {nb:3d} of {len(rs)}: full {f:3d} ({100*f/max(1,nb):3.0f}%), partial {p:3d} ({100*p/max(1,nb):3.0f}%), wrong {w:3d} ({100*w/max(1,nb):3.0f}%); "
          f"unanswerable given one {sum(r['un'] for r in b)} of {nun}; questions with a full answer that get it as best match {f} of {nfull}")
    return nb, w
for split, use in (("dev (odd-numbered)", lambda r: r["n"] % 2 == 1), ("test (even-numbered)", lambda r: r["n"] % 2 == 0), ("all", lambda r: True)):
    rs = [r for r in rowsG if use(r)]; print(f"gold, {split}: {len(rs)} questions")
    report("the page's rule now (the judge in model.json)", lambda r: r["rule"], rs)
    for th in (0.5, 0.6, 0.7, 0.8, 0.9): report(f"judge >= {th:.1f} (and about the drugs named)", lambda r: r["ok"] and r["p"] >= th, rs)
    # the judge at the same number of best matches as the thresholds
    k = sum(r["rule"] for r in rs); ps = sorted((r["p"] for r in rs if r["ok"]), reverse=True)
    if k and len(ps) >= k: report(f"judge, as many best matches as the page now", lambda r, t=ps[k - 1]: r["ok"] and r["p"] >= t, rs)
out = opt("--save")
if out:
    json.dump({"_note": "Insight's judge: a logistic regression on numbers the page computes for its first candidate; trained on our own wordings and near-miss questions only (scripts/insight/judge2.py).",
               "features": FEATS, "mu": [float(x) for x in mu], "sd": [float(x) for x in sd], "w": [float(x) for x in J.coef_[0]], "b": float(J.intercept_[0])}, open(out, "w"), indent=1)
    print("saved", out)
