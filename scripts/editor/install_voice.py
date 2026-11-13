"""install_voice.py DIR N [N ...] [--dry]: install the plain-voice writers' lines (data/verification/DIR/<N>_voice.json) into
data/site/simple.json, for the blind check that follows (Rule 0c, 13 November 2026).

For each answer: short, but, how, how_src and rate replace the current ones (freq only if the writer gave it; pages and the
general-page question stay); v stays the claim's version, and an answer whose claim changed since the tasks were made is
skipped. A proposed question heading (q) is not installed here: it is kept in data/verification/DIR/q_proposed.json and goes
into the check tasks (add_q_to_check), then onto the site after the check (sync_q). Problems are listed and the answer skipped:
How points and their source lists of different lengths, a source that is not among the claim's own references, an empty line."""
import json, sys, glob, os, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import sj
ROOT = pathlib.Path(__file__).resolve().parents[2]; os.chdir(ROOT)
args = [a for a in sys.argv[1:] if not a.startswith("--")]; dry = "--dry" in sys.argv
d, ns = args[0], args[1:]
D = pathlib.Path(f"data/verification/{d}")
C = {}
for f in glob.glob("data/claims/*.json"):
    for c in json.load(open(f, encoding="utf-8")): C[c["id"]] = c
S = sj.load()
B = json.load(open(D / "before.json", encoding="utf-8"))["claims"]
QP = json.load(open(D / "q_proposed.json", encoding="utf-8")) if (D / "q_proposed.json").exists() else {}
done, skipped, changed = [], [], {"short": 0, "but": 0, "how": 0, "rate": 0, "q": 0}
for n in ns:
    W = json.load(open(D / f"{n}_voice.json", encoding="utf-8"))["answers"]
    for cid, e in W.items():
        c, cur, old = C.get(cid), S["claims"].get(cid), B.get(cid)
        why = []
        if not c or not cur or not old: why.append("not on the site or not in this pass")
        elif cur.get("v") != c["version"] or old.get("v") != c["version"]: why.append(f"claim changed since the tasks (lines v{cur.get('v')}, claim v{c['version']})")
        else:
            refs = {a["reference"] for a in c["evidence"]}
            if not all(isinstance(e.get(k), str) and e[k].strip() for k in ("short", "but", "rate")): why.append("an empty short, but or rate")
            if not isinstance(e.get("how"), list) or not 2 <= len(e["how"]) <= 4 or not all(isinstance(x, str) and x.strip() for x in e["how"]): why.append("how needs 2 to 4 points")
            elif not isinstance(e.get("how_src"), list) or len(e["how_src"]) != len(e["how"]): why.append("how_src does not match the points")
            elif any(not isinstance(l, list) or not l or any(r not in refs for r in l) for l in e["how_src"]): why.append("a source that is not the claim's own, or a point without a source")
        if why: skipped.append(cid + ": " + "; ".join(why)); continue
        new = dict(cur)
        for k in ("short", "but", "how", "rate"):
            if new.get(k) != e[k]: changed[k] += 1
        for k in ("short", "but", "how", "how_src", "rate"): new[k] = e[k]
        if e.get("freq"): new["freq"] = e["freq"]
        S["claims"][cid] = new; done.append(cid)
        if e.get("q") and str(e["q"]).strip():
            QP[cid] = {"q": str(e["q"]).strip(), "writer": n, "note": e.get("note", "")}; changed["q"] += 1
        else: QP.pop(cid, None)
print("installed", len(done), "answers; fields changed:", changed)
for s in skipped: print("!! skipped", s)
if not dry:
    sj.save(S)
    with open(D / "q_proposed.json", "w", encoding="utf-8") as f: json.dump(QP, f, ensure_ascii=False, indent=1); f.write("\n")
