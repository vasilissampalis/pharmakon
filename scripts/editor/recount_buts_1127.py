"""recount_buts_1127.py: the But the code writes ("This rests on ..."), counted again by the code of 27 November 2026.

Reader 816 found that the lane's own But called every paper Europe PMC tags with no type a "study in people" (a systematic review of studies
mostly in animals, two case reports). lane.py now counts such papers by their own words (lane.described). This writes the line again, with the
lane's own function, in the published answers that are not held, where the record's sources give another line than the one shown; the
answers held are written again by the lane itself. Nothing a model wrote is touched. Run from the repository root; --dry shows, writes nothing."""
import glob, importlib.util, json, sys

spec = importlib.util.spec_from_file_location("lane", "scripts/auto/lane.py"); L = importlib.util.module_from_spec(spec); spec.loader.exec_module(L)
dry = "--dry" in sys.argv
held = {(x["id"], str(x.get("run"))) for x in json.load(open("data/auto/held.json", encoding="utf-8"))["held"]}
NOTE = " (27 November 2026: counted again by the code, which had called a paper of no type a study in people)"
done = []
for f in sorted(glob.glob("data/auto/answers/au_*.json")):
    a = json.load(open(f, encoding="utf-8"))
    if a.get("status") != "published" or (a["id"], str(a["made"].get("run"))) in held: continue
    for p in a.get("parts") or []:
        if p.get("part") != "but" or not p.get("fixed") or not str(p.get("text", "")).startswith("This rests on"): continue
        used = {r["ref"] for r in p.get("rests_on") or [] if r.get("ref")}
        srcs = [dict(s, ref={"id": s["ref"]["id"] if isinstance(s.get("ref"), dict) else s.get("ref")}) for s in a["sources"]]
        rest = [s for s in srcs if s["ref"]["id"] in used] or srcs
        new = L.own_but(rest, True)
        if new == p["text"]: continue
        done.append((a["id"], p["text"], new))
        if dry: continue
        p["text"] = new
        cn = L.counts(rest)
        a["gates"]["sources"] = (f"{cn['reviews']} review(s) or meta-analyses, {cn['studies in people']} single studies in people, {cn['case reports']} case report(s) (which do not count), "
                                 f"{cn['other papers']} other paper(s), {cn['official']} official page(s), {cn['summaries']} paper(s) read in summary only (the ones the answer rests on)")
        if NOTE not in a["gates"].get("but", ""): a["gates"]["but"] = a["gates"].get("but", "") + NOTE
    if done and done[-1][0] == a["id"] and not dry:
        json.dump(a, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)   # as the lane writes its records
for d in done: print(*d, sep=" | ")
print(len(done), "written again" if not dry else "would be written again")
