"""voice_check.py prep N DIR | sync DIR N [N ...] [--dry]: the question headings and How-point sources in the blind check of the
plain-voice pass (Rule 0c, 13 November 2026).

prep: after make_check.py N DIR …, adds to each plain-line task of data/verification/DIR/tasks_check<N>.json the heading to
check (the writer's proposed question from q_proposed.json, else the heading on the site now), the How points' source lists
(how_src) and the sources' short names, so the checker judges them too.
sync: after apply_check.py for checkers N …, puts each checked heading on the site: the checker's corrected q if given, else the
writer's proposed q (when the checker passed it), into every drug-page heading of that answer (data/site/questions.json) and
into the general-page question of the plain layer where it has one; a q apply_check copied into an entry that had none is
removed again (drug pages take their headings from questions.json). Writes DIR/q_applied.json."""
import json, sys, glob, os, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import sj
ROOT = pathlib.Path(__file__).resolve().parents[2]; os.chdir(ROOT)
cmd = sys.argv[1]; dry = "--dry" in sys.argv; args = [a for a in sys.argv[2:] if not a.startswith("--")]
R = {}
for f in glob.glob("data/references/*.json"):
    for r in json.load(open(f, encoding="utf-8")): R[r["id"]] = r
def short(rid):
    r = R.get(rid); a = (r or {}).get("author") or []
    if not r: return rid
    fam = lambda x: x.get("family") or x.get("literal") or "?"
    who = fam(a[0]) if len(a) == 1 else fam(a[0]) + " & " + fam(a[1]) if len(a) == 2 else (fam(a[0]) + " et al." if a else (r.get("publisher") or "?"))
    return f"{who}, {((r.get('issued') or {}).get('date-parts') or [[None]])[0][0]}"
QF = pathlib.Path("data/site/questions.json"); Q = json.load(open(QF, encoding="utf-8"))
def headings(cid): return [q for slug, gs in Q.items() if slug != "_note" for g in gs for c2, q in g["items"] if c2 == cid]
if cmd == "prep":
    n, d = args[0], args[1]; D = pathlib.Path(f"data/verification/{d}"); TF = D / f"tasks_check{n}.json"
    T = json.load(open(TF, encoding="utf-8")); S = json.load(open("data/site/simple.json", encoding="utf-8"))["claims"]
    QP = json.load(open(D / "q_proposed.json", encoding="utf-8")) if (D / "q_proposed.json").exists() else {}
    for x in T["lines"]:
        cid = x["id"]; e = S[cid]; now = headings(cid) or ([e["q"]] if e.get("q") else [])
        x["lines"]["q"] = QP[cid]["q"] if cid in QP else (now[0] if now else None)
        x["lines"]["q_on_site_now"] = now[0] if now else None
        x["lines"]["how_src"] = e.get("how_src")
        x["sources"] = [{"ref": r, "name": short(r)} for r in sorted({r for l in (e.get("how_src") or []) for r in l})]
    with open(TF, "w", encoding="utf-8") as f: json.dump(T, f, ensure_ascii=False, indent=1)
    print("prepared", len(T["lines"]), "plain-line tasks with headings and sources;", sum(1 for x in T["lines"] if x["id"] in QP), "proposed headings")
elif cmd == "sync":
    d, ns = args[0], args[1:]; D = pathlib.Path(f"data/verification/{d}")
    QP = json.load(open(D / "q_proposed.json", encoding="utf-8")) if (D / "q_proposed.json").exists() else {}
    B = json.load(open(D / "before.json", encoding="utf-8"))["claims"]; S = sj.load(); out = {}
    for n in ns:
        o = json.load(open(D / f"check_out{n}.json", encoding="utf-8"))
        for r in o.get("lines", []):
            cid = r["id"]; fixed = (r.get("fields") or {}).get("q") if r.get("verdict") == "fix" else None
            final = fixed or (QP[cid]["q"] if cid in QP else None)
            had = bool(B.get(cid, {}).get("q"))
            if final:
                for slug, gs in Q.items():
                    if slug == "_note": continue
                    for g in gs:
                        g["items"] = [[c2, final if c2 == cid else q] for c2, q in g["items"]]
                out[cid] = {"q": final, "from": "checker" if fixed else "writer", "was": headings(cid) or [B.get(cid, {}).get("q")]}
            if cid in S["claims"]:
                if had and final: S["claims"][cid]["q"] = final
                elif not had: S["claims"][cid].pop("q", None)
    print("headings changed:", len(out))
    for cid, v in out.items(): print(" ", cid, "|", v["q"], "(" + v["from"] + ")")
    if not dry:
        sj.save(S)
        with open(QF, "w", encoding="utf-8") as f: json.dump(Q, f, ensure_ascii=False, indent=1); f.write("\n")
        with open(D / "q_applied.json", "w", encoding="utf-8") as f: json.dump(out, f, ensure_ascii=False, indent=1); f.write("\n")
