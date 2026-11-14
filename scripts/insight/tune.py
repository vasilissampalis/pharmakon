"""tune.py MODELS_DIR: Pharmakon Insight, phase 1 tuning. On top of the meaning match (eval_match.py), try two signals
the site already has: the drug a question names (street names from data/site/aliases.json and the drug names in
data/site/substances.json) and plain word overlap (TF-IDF). Grid over the drug boost b and the word weight w; reports
top-1 and top-3 on the answerable forum questions (provisional labels) for each model. Run eval_match.py's loaders."""
import sys, json, re, pathlib, importlib.util
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("em", ROOT / "scripts/insight/eval_match.py")
sys.argv = [sys.argv[0], sys.argv[1]]
em = importlib.util.module_from_spec(spec); spec.loader.exec_module(em)
ans, answerable, unanswerable, ids = em.ans, em.answerable, em.unanswerable, em.ids
AL = json.load(open(ROOT / "data/site/aliases.json", encoding="utf-8"))
SUB = json.load(open(ROOT / "data/site/substances.json", encoding="utf-8"))
names = {}
for s in SUB:
    slug = s["slug"]; ns = {slug.replace("-", " ")}
    for part in re.split(r"[()/,;]| and ", s["name"]): 
        p = part.strip().lower()
        if len(p) >= 3: ns.add(p)
    for a in AL.get(slug, []):
        if len(a) >= 3: ns.add(a.lower())
    names[slug] = ns
pat = {slug: re.compile(r"\b(" + "|".join(re.escape(n) for n in sorted(ns, key=len, reverse=True)) + r")\b") for slug, ns in names.items()}
def drugs_in(text):
    t = text.lower(); return {slug for slug, p in pat.items() if p.search(t)}
S = json.load(open(ROOT / "data/verification/insight/answers.json", encoding="utf-8"))["answers"]
pages = {a["id"]: set(a["pages"]) & set(names) for a in S}
texts_T = [t[0] for t in answerable] + [t[0] for t in unanswerable]
qd = [drugs_in(t) for t in texts_T]
canon = {s["slug"]: s["name"].split(" (")[0] for s in SUB}
def expand(t):   # add the drug's own name for each street or brand name found ("valium" -> Benzodiazepines)
    d = drugs_in(t); extra = [canon[x] for x in sorted(d) if canon[x].lower() not in t.lower()]
    return t + (" (" + ", ".join(extra) + ")" if extra else "")
texts_X = [expand(t) for t in texts_T]
print("expanded examples:", [x for x, t in zip(texts_X, texts_T) if x != t][:4])
B = np.zeros((len(texts_T), len(ans)), np.float32)
for i, d in enumerate(qd):
    if not d: continue
    for j, a in enumerate(ans):
        ad = pages.get(a[0], set())
        if ad & d: B[i, j] = 1
        elif ad: B[i, j] = -1
docs = [" ".join(a[1]) + " " + a[2] for a in ans]
lex = em.Lexical(docs + texts_T); L = lex.vec(texts_T) @ lex.vec(docs).T
n = len(answerable)
def score(sims):
    top = np.argsort(-sims, 1)[:, :3]
    return (round(100 * sum(ids[top[i, 0]] in answerable[i][1] for i in range(n)) / n, 1), round(100 * sum(any(ids[j] in answerable[i][1] for j in top[i]) for i in range(n)) / n, 1))
print("questions naming a drug:", sum(1 for d in qd[:n] if d), "of", n, "answerable")
for name, cls, sub in (("minilm", em.MiniLM, "_clay-design-system_embeddings/package/model"), ("potion", em.Potion, "_yarflam_potion-base-8m/package/models")):
    enc = cls(em.M / sub); Wv = enc([w for _, w in em.flat]); As = enc([a[2] for a in ans])
    for label, tx in (("plain", texts_T), ("expanded", texts_X)):
        T = enc(tx); base = 0.7 * em.per_claim(T, Wv) + 0.3 * (T @ As.T)
        print(name, label, "b=0 w=0", score(base), "| b=0.03 w=0.1", score(base + 0.03 * B + 0.1 * L), "| b=0.05 w=0.2", score(base + 0.05 * B + 0.2 * L))
    T = enc(texts_X); base = 0.7 * em.per_claim(T, Wv) + 0.3 * (T @ As.T)
    best = None
    for b in (0, 0.03, 0.05, 0.08, 0.12):
        for w in (0, 0.1, 0.2, 0.3):
            r = score(base + b * B + w * L)
            if best is None or r[1] > best[0][1] or (r[1] == best[0][1] and r[0] > best[0][0]): best = (r, b, w)
    print("BEST", name, best)
