"""sweep_related.py IN.json INDEX.json [--show REL NEAR]: where should "Related" begin for this model? (15 November 2026)

With the best match decided by the judge (site/insight/model.json, judge.best), the other answers Insight lists are the
related ones: the next answers in the page's order, up to three, whose first look is tiers.related or more and whose
topic score is tiers.near or more (build_index.Ranker.tiers). A fine-tuned encoder spreads its scores, so the open
model's thresholds are too strict for it. For a grid of the two, on the gold set (400 forum questions, two blind
readers; odd-numbered questions are the dev half, even-numbered the test half), per question, what Insight shows is

  help : a full or partial answer is among the best match and the related rows;
  junk : rows are shown and none of them answers the question, in full or in part;
  miss : nothing is shown although the site has a full or partial answer;
  ok   : nothing is shown and the site has nothing (rightly empty);

and also: seen (of the questions with a full answer, how many see it), the number of related rows, the share of them
that are a full or partial answer, and how many of the questions nobody can answer get rows anyway.
--show REL NEAR prints every third junk block at that setting, to read what such rows look like.
IN.json is the build's input (site/insight/.cache/index-input.json), INDEX.json the index built with the model."""
import sys, json, glob, pathlib
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_index as bi
ROOT = bi.ROOT
args = [a for a in sys.argv[1:] if not a.startswith("--")]
show = [float(x) for x in sys.argv[sys.argv.index("--show") + 1:sys.argv.index("--show") + 3]] if "--show" in sys.argv else None
if show: args = args[:2]
A = json.load(open(args[0], encoding="utf-8"))["answers"]; qtext = {a["id"]: (a["wordings"] or ["?"])[0] for a in A}
D = json.load(open(args[1], encoding="utf-8")); R = bi.Ranker(D); idset = set(R.ids)
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
tx = [R.texts(t[1]) for t in tests]; V = bi.embed_all([t[0] for t in tx] + [t[1] for t in tx], quiet=True)
LG = [R.look(V[i], V[len(tx) + i], tests[i][1], tx[i][2]) for i in range(len(tx))]
keep = dict(R.t)
def shown(L, rel, near):
    R.t = dict(keep, related=rel, near=near)
    best, related, _ = R.tiers(L["plain"], L["topic"], L["groups"], lambda c: R.six(L, c))
    return list(best), list(related)
def run(rel, near, use=lambda n: True):
    o = dict(help=0, junk=0, miss=0, ok=0, seen=0, nfull=0, rows=0, good=0, unrows=0, nun=0, n=0)
    for (n, q, full, part, un), L in zip(tests, LG):
        if not use(n): continue
        best, related = shown(L, rel, near); ids = [R.ids[j] for j in best + related]
        o["n"] += 1; o["nfull"] += bool(full); o["nun"] += un; o["rows"] += len(related)
        o["good"] += sum(R.ids[j] in full or R.ids[j] in part for j in related); o["unrows"] += bool(un and related)
        o["seen"] += bool(full) and any(a in full for a in ids)
        o["help" if any(a in full or a in part for a in ids) else "junk" if ids else "miss" if (full or part) else "ok"] += 1
    return o
fmt = lambda o: (f"help {o['help']:3d} junk {o['junk']:3d} miss {o['miss']:3d} ok {o['ok']:3d} | seen {o['seen']:2d} of {o['nfull']} | "
                 f"{o['rows']:3d} rows, {100 * o['good'] / max(1, o['rows']):2.0f}% answers | unanswerable with rows {o['unrows']:2d} of {o['nun']}")
dev = lambda n: n % 2 == 1; test = lambda n: n % 2 == 0
if show:
    k = 0; print(f"junk blocks at related {show[0]:.2f}, near {show[1]:.2f} (every third): the question, then each row's first look / topic")
    for (n, q, full, part, un), L in zip(tests, LG):
        best, related = shown(L, *show); ids = [R.ids[j] for j in best + related]
        if ids and not any(a in full or a in part for a in ids):
            k += 1
            if k % 3: continue
            print(f"Q{n} [{'nothing on the site' if un else 'answerable' if (full or part) else 'readers differ'}] {q[:110]}")
            for j in related: print(f"      {float(L['plain'][j]):.2f} / {float(L['topic'][j]):.2f}  {qtext[R.ids[j]][:95]}")
    R.t = keep; sys.exit(0)
print(f"model {D['model']}; best match from judge {R.J['best']}; tiers now {json.dumps(keep)}")
print(f"  now | dev  {fmt(run(keep['related'], keep['near'], dev))}\n      | test {fmt(run(keep['related'], keep['near'], test))}\n      | all  {fmt(run(keep['related'], keep['near']))}")
for rel in (0.44, 0.46, 0.48, 0.50, 0.52, 0.54, 0.56, 0.58):
    for near in (0.0, 0.30, 0.36, 0.38, 0.40, 0.42, 0.45, 0.50):
        print(f"related {rel:.2f} near {near:.2f} | dev {fmt(run(rel, near, dev))}\n{'':<23} | test {fmt(run(rel, near, test))}\n{'':<23} | all  {fmt(run(rel, near))}")
R.t = keep
