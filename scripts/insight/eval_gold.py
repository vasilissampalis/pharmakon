"""eval_gold.py MODELS_DIR: Pharmakon Insight, phase 1 on the gold set (data/verification/insight/gold_reader693.json and
gold_reader694.json, two readers labelling the same 400 real forum questions blind). Reports the readers' agreement, then,
for each matcher, how often the top 3 hold a right answer:
- strict: an answer that a reader judged to answer the question as asked ("answers");
- lenient: also an answer judged to answer part of it ("partly");
and, for questions both readers judged unanswered, how often the matcher would show a confident match at each threshold.
Matchers: word search (TF-IDF), all-MiniLM-L6-v2 and potion-base-8M with the tuned scoring of tune.py (0.7 best question
wording + 0.3 short answer + 0.2 word overlap, drug names expanded). Wordings from variants_reader696.json are added when
that file exists (they were written without seeing these questions)."""
import sys, json, re, pathlib, importlib.util, io, contextlib
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[2]
M = pathlib.Path(sys.argv[1])
G = json.load(open(ROOT / "data/verification/insight/gold-sample.json", encoding="utf-8"))["questions"]
L = {}
for r in ("693", "694"):
    f = ROOT / f"data/verification/insight/gold_reader{r}.json"
    if f.exists(): L[r] = {x["n"]: x for x in json.load(open(f, encoding="utf-8"))["labels"]}
assert len(L) == 2, "both gold files needed"
a, b = L["693"], L["694"]
ns = [q["n"] for q in G if q["n"] in a and q["n"] in b]
def ans(x): return set(x.get("answers") or [])
def any_(x): return set(x.get("answers") or []) | set(x.get("partly") or [])
yes = lambda x: bool(any_(x)) and not x.get("none")
both_yes = sum(yes(a[n]) and yes(b[n]) for n in ns); both_no = sum((not yes(a[n])) and (not yes(b[n])) for n in ns)
po = (both_yes + both_no) / len(ns); pa = sum(yes(a[n]) for n in ns) / len(ns); pb = sum(yes(b[n]) for n in ns) / len(ns)
pe = pa * pb + (1 - pa) * (1 - pb); kappa = (po - pe) / (1 - pe) if pe < 1 else 1
full_overlap = sum(bool(ans(a[n]) & ans(b[n])) for n in ns if ans(a[n]) and ans(b[n]))
print(f"{len(ns)} questions labelled by both. Answerable (full or partly) by both: {both_yes}; unanswered by both: {both_no}; agreement {po:.2f}, kappa {kappa:.2f}")
print(f"questions with a full answer from both readers: {sum(1 for n in ns if ans(a[n]) and ans(b[n]))}, sharing at least one: {full_overlap}")
strict = {n: ans(a[n]) | ans(b[n]) for n in ns}
lenient = {n: any_(a[n]) | any_(b[n]) for n in ns}
none_both = [n for n in ns if not yes(a[n]) and not yes(b[n])]
spec = importlib.util.spec_from_file_location("tn", ROOT / "scripts/insight/tune.py")
argv0 = sys.argv; sys.argv = [argv0[0], str(M)]
with contextlib.redirect_stdout(io.StringIO()):
    em_spec = importlib.util.spec_from_file_location("em", ROOT / "scripts/insight/eval_match.py")
    em = importlib.util.module_from_spec(em_spec); em_spec.loader.exec_module(em)
sys.argv = argv0
ans_list = list(em.ans)
V = ROOT / "data/verification/insight/variants_reader696.json"
extra = json.load(open(V, encoding="utf-8"))["variants"] if V.exists() else {}
ids = [x[0] for x in ans_list]
flat = [(i, w) for i, x in enumerate(ans_list) for w in x[1] + [v for v in extra.get(x[0], [])]]
print(f"wordings indexed: {len(flat)} ({sum(len(v) for v in extra.values())} from the phrasings file)")
AL = json.load(open(ROOT / "data/site/aliases.json", encoding="utf-8")); SUB = json.load(open(ROOT / "data/site/substances.json", encoding="utf-8"))
names = {}
for s in SUB:
    ns_ = {s["slug"].replace("-", " ")} | {p.strip().lower() for p in re.split(r"[()/,;]| and ", s["name"]) if len(p.strip()) >= 3} | {x.lower() for x in AL.get(s["slug"], []) if len(x) >= 3}
    names[s["slug"]] = ns_
pat = {k: re.compile(r"\b(" + "|".join(re.escape(n) for n in sorted(v, key=len, reverse=True)) + r")\b") for k, v in names.items()}
canon = {s["slug"]: s["name"].split(" (")[0] for s in SUB}
def expand(t):
    d = {k for k, p in pat.items() if p.search(t.lower())}; extra_ = [canon[x] for x in sorted(d) if canon[x].lower() not in t.lower()]
    return t + (" (" + ", ".join(extra_) + ")" if extra_ else "")
qtext = {q["n"]: q["question"] for q in G}
T_raw = [qtext[n] for n in ns]; T_x = [expand(t) for t in T_raw]
docs = [" ".join(x[1]) + " " + x[2] for x in ans_list]
lex = em.Lexical(docs + T_raw); Lsim = lex.vec(T_raw) @ lex.vec(docs).T
def per_claim(T, W):
    sw = T @ W.T; out = np.full((T.shape[0], len(ans_list)), -1.0, np.float32)
    for col, (i, _) in enumerate(flat): out[:, i] = np.maximum(out[:, i], sw[:, col])
    return out
def report(name, sims):
    top = np.argsort(-sims, 1)[:, :3]; best = sims.max(1)
    rows = [k for k, n in enumerate(ns) if lenient[n]]; srows = [k for k, n in enumerate(ns) if strict[n]]
    s3 = sum(any(ids[j] in strict[ns[k]] for j in top[k]) for k in srows) / max(1, len(srows))
    s1 = sum(ids[top[k, 0]] in strict[ns[k]] for k in srows) / max(1, len(srows))
    l3 = sum(any(ids[j] in lenient[ns[k]] for j in top[k]) for k in rows) / max(1, len(rows))
    print(f"{name:<28} strict top1 {100*s1:5.1f} top3 {100*s3:5.1f} (n={len(srows)}) | lenient top3 {100*l3:5.1f} (n={len(rows)})")
    nb = [k for k, n in enumerate(ns) if n in none_both]
    for th in (0.35, 0.4, 0.45, 0.5, 0.55, 0.6):
        shown_ans = sum(best[k] >= th for k in rows) / max(1, len(rows)); right = sum(best[k] >= th and any(ids[j] in lenient[ns[k]] for j in top[k]) for k in rows) / max(1, len(rows))
        conf_none = sum(best[k] >= th for k in nb) / max(1, len(nb))
        print(f"    threshold {th:.2f}: answerable shown {100*shown_ans:5.1f}%, right in top 3 when shown {100*right:5.1f}% of answerable; unanswered given a confident match {100*conf_none:5.1f}%")
report("word search (TF-IDF)", Lsim)
for name, cls, sub in (("all-MiniLM-L6-v2", em.MiniLM, "_clay-design-system_embeddings/package/model"), ("potion-base-8M", em.Potion, "_yarflam_potion-base-8m/package/models")):
    enc = cls(M / sub); W = enc([w for _, w in flat]); As = enc([x[2] for x in ans_list])
    for lab, tx in (("plain", T_raw), ("tuned", T_x)):
        T = enc(tx); sims = 0.7 * per_claim(T, W) + 0.3 * (T @ As.T) + (0.2 * Lsim if lab == "tuned" else 0)
        report(f"{name} {lab}", sims)
