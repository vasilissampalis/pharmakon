"""ask.py [--drug SLUG] [--index FILE] QUESTION...: how Insight reads each question (site 2.3), with the page's own rule
(class Ranker in build_index.py) on the index of the last build: the drugs it names, what is embedded for each of the two
looks, and the candidates with their first-look and topic scores and the tier each falls in. For the editor, when tuning
TIERS in build_index.py. --drug: as if asked on that drug's page. Build first (node site/build.js).
Usage: python3 -I scripts/insight/ask.py "how can i die from ketamine" "is it addictive" --drug cannabis"""
import importlib.util, json, pathlib, sys
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("bi", ROOT / "scripts/insight/build_index.py"); bi = importlib.util.module_from_spec(spec); spec.loader.exec_module(bi)
args = sys.argv[1:]; drug = None; index = ROOT / "site/dist/data/insight.json"
while args and args[0] in ("--drug", "--index"):
    if args[0] == "--drug": drug = args[1]
    else: index = pathlib.Path(args[1])
    args = args[2:]
D = json.load(open(index, encoding="utf-8")); R = bi.Ranker(D)
A = {a["id"]: a for a in json.load(open(ROOT / "site/insight/.cache/index-input.json", encoding="utf-8"))["answers"]}
for q in args:
    full, masked, groups = R.texts(q, drug)
    v, mv = bi.embed_all([full, masked], quiet=True)
    r = R.rank_vectors(q, v, mv, groups)
    print(f"\n{q}\n  first look: {full}\n  topic:      {masked}\n  about:      {[g if len(g) < 4 else g[:3] + ['…'] for g in groups] or 'no drug named'}")
    tier = {x["id"]: "BEST   " for x in r["best"]}; tier.update({x["id"]: "related" for x in r["related"]})
    key = r["plain"] + R.wt["topic"] * r["topic"] + R.wt["same"] * r["ok"]
    for i in np.argsort(-key, kind="stable")[:7]:
        a = A.get(R.ids[i], {})
        print(f"  {tier.get(R.ids[i], '       ')} first {r['plain'][i]:.3f} topic {r['topic'][i]:.3f} {'  ' if r['ok'][i] else 'x '}{R.ids[i]} [{', '.join(a.get('about') or a.get('pages') or [])[:40]}] {(a.get('wordings') or [''])[0][:70]}")
    if not r["best"]: print("  -> We haven't checked exactly this yet." + ("" if r["related"] else " (nothing related)"))
