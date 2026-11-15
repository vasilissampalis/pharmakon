"""ask2.py IN.json INDEX.json JUDGE.json "question" ["question" ...] [--drug SLUG]: how Insight reads a question, with the
judge (scripts/insight/judge2.py): the first three candidates in the page's order, each with the page's two looks, its lead
over the next answer, its second-best wording, and the judge's confidence that it answers what was asked."""
import sys, json, pathlib, re
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_index as bi
args = [a for a in sys.argv[1:] if not a.startswith("--")]
drug = sys.argv[sys.argv.index("--drug") + 1] if "--drug" in sys.argv else None
if drug in args: args.remove(drug)
A = json.load(open(args[0], encoding="utf-8"))["answers"]; D = json.load(open(args[1], encoding="utf-8")); J = json.load(open(args[2], encoding="utf-8"))
R = bi.Ranker(D); n = R.n; rows = np.array(D["rows"]); qtext = {a["id"]: (a["wordings"] or ["?"])[0] for a in A}
mu, sd, w, b = np.array(J["mu"]), np.array(J["sd"]), np.array(J["w"]), J["b"]
for q in args[3:]:
    full, masked, groups = R.texts(q, drug); v, mv = bi.embed_all([full, masked], quiet=True)
    sw, sm = R.W @ v, R.M @ mv
    bw = np.full(n, -1.0, np.float32); bw2 = np.full(n, -1.0, np.float32); bm = np.full(n, -1.0, np.float32); seen = np.zeros(n, bool)
    for k in np.argsort(-sw, kind="stable"):
        r = rows[k]
        if not seen[r]: seen[r] = True; bw[r] = sw[k]
        elif bw2[r] < 0: bw2[r] = sw[k]
    np.maximum.at(bm, rows, sm)
    sh = R.S @ v; lx = R.lex.sims(q); plain = R.wt["q"] * bw + R.wt["short"] * sh + R.wt["words"] * lx
    ok = np.array([all(any(s in R.about[i] for s in g) for g in groups) for i in range(n)])
    by = plain + R.wt["topic"] * bm; key = by + R.wt["same"] * ok
    print(f"\nQ: {q}   [drugs named: {groups or '-'}]")
    for c in [int(c) for c in np.argsort(-key, kind="stable")[:3]]:
        lead = float(by[c] - np.delete(by, c).max())
        f = np.array([bw[c], max(bw2[c], 0), sh[c], lx[c], bm[c], lead, 0.0, min(len(q.split()), 20) / 20, min(len(groups), 2)])
        f[6] = 0.5   # the kind-of-question number is not recomputed here (small weight)
        f = f[:len(mu)]
        p = 1 / (1 + np.exp(-(((f - mu) / sd) @ w + b)))
        print(f"   p {p:.2f} | plain {plain[c]:.2f} topic {bm[c]:.2f} lead {lead:+.3f} second {max(bw2[c],0):.2f} {'' if ok[c] else '[other drug] '}| {qtext[R.ids[c]]}")
