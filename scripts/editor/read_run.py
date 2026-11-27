"""read_run.py [RUN ...]: the answers the machine lane published in the given GitHub runs (default: the newest run that wrote an answer),
each with its parts and the words they rest on, for the editor's reading (27 November 2026). Prints; writes nothing.
Whether a version is held is said beside it (lane.is_held, the newest hold of an answer, as the site decides)."""
import glob, importlib.util, json, sys

spec = importlib.util.spec_from_file_location("lane", "scripts/auto/lane.py"); L = importlib.util.module_from_spec(spec); spec.loader.exec_module(L)
recs = [json.load(open(f, encoding="utf-8")) for f in sorted(glob.glob("data/auto/answers/au_*.json"))]
runs = set(sys.argv[1:]) or {max((str(a.get("made", {}).get("run") or "") for a in recs), key=lambda r: int(r) if r.isdigit() else 0)}
held = json.load(open("data/auto/held.json", encoding="utf-8"))["held"]
for a in recs:
    if str(a.get("made", {}).get("run") or "") not in runs: continue
    print("=" * 100)
    print(f"{a['id']}  {a['status']}  run {a['made'].get('run')}  team {a['made'].get('models', {}).get('team')}  held: {L.is_held(a, held)}  | {a['question']}")
    if a["status"] != "published": print("   why:", (a.get("why") or "")[:400]); continue
    for p in a.get("parts") or []:
        print(f"  -- {p['part']}{' (the code)' if p.get('fixed') else ''}: {p['text']}")
        for r in p.get("rests_on") or []: print(f"        [{r.get('ref')} | {(r.get('where') or '')[:60]}] {(r.get('quote') or '')[:300]}")
