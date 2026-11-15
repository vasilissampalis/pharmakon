"""sweep.py IN.json INDEX.json [--out FILE]: where should Insight's tiers begin for this model? (15 November 2026)

For a grid of the two thresholds of a best match (first look `best`, topic score `topic`; site/insight/model.json), the
page's own rule (build_index.Ranker.tiers) is run on:
  - the gold set (400 forum questions, two blind readers): how many questions get a best match, and whether it is a full
    answer, a partial one or wrong; how many unanswerable questions get one; in how many questions with a full answer that
    answer is shown at all (as best match or under Related);
  - the near-miss questions of the answers the fine-tuned encoder never trained on (the 15% finetune.py holds out, by the
    same hash) and of all answers: how often the answer a question does NOT get is given as its best match.
Odd-numbered gold questions choose (dev), even-numbered ones report (test). Printed: the grid on dev, then the settings
that keep wrong best matches on dev at or under 5% and 10% with the most full answers, each with its test numbers."""
import sys, json, glob, pathlib, hashlib
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_index as bi
ROOT = bi.ROOT
args = [a for a in sys.argv[1:] if not a.startswith("--")]
opt = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
D = json.load(open(args[1], encoding="utf-8")); R = bi.Ranker(D); idset = set(R.ids)
_, _, near = bi.people_wordings()
G = json.load(open(ROOT / "data/verification/insight/gold-sample.json", encoding="utf-8"))["questions"]
readers = [json.load(open(f, encoding="utf-8"))["labels"] for f in sorted(glob.glob(str(ROOT / "data/verification/insight/gold_reader*.json")))]
lab = {}
for Rd in readers:
    for x in Rd: lab.setdefault(x["n"], []).append(x)
tests = []
for g in G:
    ls = lab.get(g["n"], [])
    if len(ls) < len(readers): continue
    full = {a for x in ls for a in x.get("answers", []) if a in idset}; part = {a for x in ls for a in x.get("partly", []) if a in idset} - full
    tests.append((g["n"], g["question"], full, part, all(x.get("none") for x in ls)))
held = lambda a: int(hashlib.sha1(a.encode()).hexdigest(), 16) % 100 < 15
nm = [(q, a) for a, qs in sorted(near.items()) if a in idset for q in qs]
def scored(questions):
    tx = [R.texts(q) for q in questions]; V = bi.embed_all([t[0] for t in tx] + [t[1] for t in tx])
    return [(R.score(V[i], V[len(tx) + i], questions[i]), tx[i][2]) for i in range(len(tx))]
SG = scored([t[1] for t in tests]); SN = scored([q for q, _ in nm])
keep = dict(R.t)
def run(best, topic, sure=None, use=lambda n: True):
    R.t = dict(keep, best=best, topic=topic, sure=keep["sure"] if sure is None else sure)
    o = {"n": 0, "best": 0, "full": 0, "part": 0, "wrong": 0, "un": 0, "nun": 0, "nfull": 0, "seen": 0}
    for (nq, q, full, part, un), ((plain, tp), groups) in zip(tests, SG):
        if not use(nq): continue
        o["n"] += 1; o["nun"] += un; o["nfull"] += bool(full)
        b, rel, _ = R.tiers(plain, tp, groups)
        if b:
            a = R.ids[b[0]]; o["best"] += 1; o["full"] += a in full; o["part"] += a in part; o["wrong"] += (a not in full and a not in part); o["un"] += un
        if full and any(R.ids[j] in full for j in list(b) + list(rel)): o["seen"] += 1
    return o
def nearmiss(best, topic, only_held):
    R.t = dict(keep, best=best, topic=topic); hit = tot = 0
    for (q, a), ((plain, tp), groups) in zip(nm, SN):
        if only_held and not held(a): continue
        b, _, _ = R.tiers(plain, tp, groups); tot += 1; hit += any(R.ids[j] == a for j in b)
    return hit, tot
dev = lambda n: n % 2 == 1; test = lambda n: n % 2 == 0
fmt = lambda o: f"best {o['best']:3d} of {o['n']}: full {o['full']:2d}, partial {o['part']:2d}, wrong {o['wrong']:2d} ({100*o['wrong']/max(1,o['best']):3.0f}%); unanswerable given one {o['un']} of {o['nun']}; full answer shown at all {o['seen']} of {o['nfull']}"
print(f"model {D['model']}; thresholds now {json.dumps(keep)}")
grid = [(round(b, 2), round(t, 2)) for b in np.arange(0.50, 0.801, 0.02) for t in (0.0, 0.30, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65)]
rows = []
for b, t in grid:
    d = run(b, t, use=dev); rows.append((b, t, d))
print("dev half (odd-numbered gold questions), by threshold of the first look (rows) with the topic threshold that gives the most full answers at each level of wrong best matches:")
for limit in (0.0, 0.05, 0.10, 0.15):
    ok = [(b, t, d) for b, t, d in rows if d["best"] and d["wrong"] / d["best"] <= limit]
    if not ok: print(f"  wrong at most {100*limit:.0f}%: none"); continue
    b, t, d = max(ok, key=lambda x: (x[2]["full"], x[2]["full"] + x[2]["part"], -x[2]["wrong"], x[0]))
    te = run(b, t, use=test); al = run(b, t); h, n_ = nearmiss(b, t, True); h2, n2 = nearmiss(b, t, False)
    print(f"  wrong at most {100*limit:.0f}% on dev -> best {b:.2f}, topic {t:.2f}\n      dev : {fmt(d)}\n      test: {fmt(te)}\n      all : {fmt(al)}\n      near-miss questions given the answer they do not get: answers not trained on {h} of {n_} ({100*h/max(1,n_):.1f}%), all {h2} of {n2} ({100*h2/max(1,n2):.1f}%)")
print("the whole grid on all 400 gold questions (first look threshold, topic threshold: best matches, full, partial, wrong; full answer shown at all):")
for b in sorted({b for b, _ in grid}):
    cells = []
    for t in (0.0, 0.45, 0.55, 0.65):
        o = run(b, t); cells.append(f"t{t:.2f}: {o['best']:3d} / {o['full']:2d} {o['part']:2d} {o['wrong']:2d} / {o['seen']:2d}")
    print(f"  best {b:.2f} | " + " | ".join(cells))
R.t = keep
out = opt("--out")
if out: json.dump([{"best": b, "topic": t, **d} for b, t, d in rows], open(out, "w"))
