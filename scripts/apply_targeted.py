#!/usr/bin/env python3
"""Turn a targeted-check result file into a claim patch (METHODS §5.5; WORKFLOW step 9a), then apply it with claim_patch.py.

Usage: apply_targeted.py TASKS.json OUT.json PATCH_OUT.json [--apply]

TASKS.json: [{n, claim_id, claim_file, anchor_index, reference, extracted, current_status, ...}] (what the checker was given)
OUT.json:   {"reader": "...", "date": "YYYY-MM-DD", "results": [{n, claim_id, anchor_index, verdict, corrected_extracted?,
             corrected_page?, corrected_locator?, note}]}

- confirmed → the anchor becomes ai-checked, check_mode 'targeted', checked_by the reader, checked_on the date.
- corrected / wrong-location → the corrected text, page or locator is written and the anchor becomes ai-checked
  (the reader checked the corrected version at the source); a correction that changes a number is a minor version.
- not-found → nothing changes but a check_note; the editor decides (listed at the end).
- A metadata-verified claim whose anchors are then all checked moves up to ai-anchored (METHODS §12). Draft claims are
  never moved by this script (draft can also mean narrative-only).
The checker must not have written the anchor; the validator refuses a check by the reader who located it.
"""
import json, re, sys, pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
_t = json.load(open(sys.argv[1], encoding="utf-8")); _t = _t["tasks"] if isinstance(_t, dict) else _t  # a task list, or {"_note", "tasks": [...]}
tasks = {t["n"]: t for t in _t}
out = json.load(open(sys.argv[2], encoding="utf-8"))
reader, date = out["reader"], out["date"]
nums = lambda s: sorted(re.findall(r"\d+(?:\.\d+)?", s or ""))
claims = {}
for f in sorted((ROOT / "data" / "claims").glob("*.json")) + sorted(x for x in (ROOT / "data" / "claims" / "_incoming").glob("*.json") if not x.name.startswith("patch_")):
    for c in json.load(open(f, encoding="utf-8")): claims.setdefault(c["id"], c)  # the main claim files come first and win over staged copies
patches, notes, problems = {}, [], []
for r in out["results"]:
    for k in ("extracted", "page", "locator"):  # results may give corrections as {"corrected": {"page": ...}}
        if (r.get("corrected") or {}).get(k) and not r.get("corrected_" + k): r["corrected_" + k] = r["corrected"][k]
    t = tasks.get(r["n"])
    if not t or t["claim_id"] != r["claim_id"] or t["anchor_index"] != r["anchor_index"]:
        problems.append(f"result {r.get('n')}: does not match its task"); continue
    c = claims[t["claim_id"]]; i = t["anchor_index"]; e = c["evidence"][i]
    if e["extracted"] != t["extracted"]:
        problems.append(f"{c['id']} anchor {i}: changed since the task was written; skipped"); continue
    p = patches.setdefault(c["id"], {"claim": c["id"], "evidence_set": [], "bump": "patch", "_n": {}})
    v = r["verdict"]
    p["_n"][v] = p["_n"].get(v, 0) + 1
    if v == "not-found":
        p["evidence_set"].append([i, "check_note", f"Targeted check {date} ({reader}): not found at the stated place. {r.get('note', '')}".strip()])
        notes.append(f"NOT FOUND {c['id']} anchor {i} ({t['reference']}): {r.get('note', '')}"); continue
    if v in ("corrected", "wrong-location"):
        if r.get("corrected_extracted"):
            if nums(r["corrected_extracted"]) != nums(e["extracted"]): p["bump"] = "minor"
            p["evidence_set"].append([i, "extracted", r["corrected_extracted"]])
        if r.get("corrected_page"): p["evidence_set"].append([i, "page", r["corrected_page"]])
        if r.get("corrected_locator"): p["evidence_set"].append([i, "locator", r["corrected_locator"]])
        notes.append(f"{v.upper()} {c['id']} anchor {i} ({t['reference']}): {r.get('note', '')}")
    elif v != "confirmed":
        problems.append(f"{c['id']} anchor {i}: unknown verdict {v!r}"); continue
    p["evidence_set"] += [[i, "anchor_status", "ai-checked"], [i, "check_mode", "targeted"], [i, "checked_by", reader], [i, "checked_on", date]]
# compose change lines and the ladder step
final = []
for cid, p in patches.items():
    c = claims[cid]; st = [e["anchor_status"] for e in c["evidence"]]
    for i, f, val in p["evidence_set"]:
        if f == "anchor_status": st[i] = val
    n = p.pop("_n")
    parts = [f"{k} {n[k]}" for k in ("confirmed", "corrected", "wrong-location", "not-found") if n.get(k)]
    p["change"] = f"Targeted check of anchors at the stated place by an independent reader ({reader}, {date}): " + ", ".join(parts) + "."
    if c["verification"]["status"] == "metadata-verified" and all(s in ("ai-checked", "senior-verified") for s in st):
        p["set"] = {"verification.status": "ai-anchored"}
        p["change"] += " Every anchor is now checked by a second reader: status ai-anchored (METHODS §12)."
    final.append(p)
json.dump(final, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(final)} claim patches written to {sys.argv[3]}")
for x in problems: print("PROBLEM", x)
for x in notes: print(x)
if "--apply" in sys.argv:
    if problems: sys.exit("not applied: fix the problems first")
    print(subprocess.run([sys.executable, "-I", str(ROOT / "scripts" / "claim_patch.py"), sys.argv[3]], capture_output=True, text=True).stdout.strip())
