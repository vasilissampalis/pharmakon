#!/usr/bin/env python3
"""Apply an editor's patch file to claims, safely and with a changelog entry (METHODS §13).

Patch file: a JSON list of
  {"claim": "cl_meth_x",
   "expect": {"grade.certainty": "moderate"},          # optional: refuse unless these fields currently hold these values
   "set": {"plain": "...", "grade.domains.large_effect.levels": 0, "grade.certainty": "low"},
   "replace": [["statement", "old text", "new text"]], # optional: exact substring replacements; the old text must occur once
   "evidence_set": [[3, "extracted", "..."]],          # optional: set a field of evidence[i]
   "evidence_add": [{"reference": "...", "page": "...", "locator": "...", "extracted": "...", "role": "qualifies"}],
                                                       # optional: new anchors, status ai-located unless given
   "bump": "patch" | "minor",                          # minor when a rating, a number or the meaning changes; patch for wording
   "change": "what changed and why (goes into the claim's changelog)"}

Usage: claim_patch.py PATCH.json [--dry-run]
Every patch is checked before anything is written; one failure aborts the whole file.
"""
import json, sys, pathlib, datetime, copy

ROOT = pathlib.Path(__file__).resolve().parents[1]
TODAY = datetime.date.today().isoformat()


def get(obj, path):
    for k in path.split("."):
        obj = obj[int(k)] if isinstance(obj, list) else obj[k]
    return obj


def put(obj, path, value):
    keys = path.split(".")
    for k in keys[:-1]:
        obj = obj[int(k)] if isinstance(obj, list) else obj.setdefault(k, {})
    last = keys[-1]
    if isinstance(obj, list):
        obj[int(last)] = value
    else:
        obj[last] = value


def bump(v, how):
    major, minor, patch = (int(x) for x in v.split("."))
    return f"{major}.{minor + 1}.0" if how == "minor" else f"{major}.{minor}.{patch + 1}"


def main():
    patches = json.load(open(sys.argv[1], encoding="utf-8"))
    dry = "--dry-run" in sys.argv
    files = {}
    for f in sorted((ROOT / "data" / "claims").glob("*.json")):
        files[f] = json.load(open(f, encoding="utf-8"))
    for f in sorted((ROOT / "data" / "claims" / "_incoming").glob("*.json")):
        if f.name.startswith("patch_"): continue  # readers' patch files sit here too; they are not claims
        files[f] = json.load(open(f, encoding="utf-8"))
    where = {}
    for f, cs in files.items():  # the main claim files come first and win over staged copies in _incoming/
        for i, c in enumerate(cs): where.setdefault(c["id"], (f, i))
    work = copy.deepcopy(files)
    errors = []
    for n, p in enumerate(patches):
        cid = p["claim"]
        if cid not in where:
            errors.append(f"#{n} {cid}: unknown claim"); continue
        f, i = where[cid]; c = work[f][i]
        for path, val in (p.get("expect") or {}).items():
            try:
                cur = get(c, path)
            except (KeyError, IndexError):
                cur = None
            if cur != val:
                errors.append(f"#{n} {cid}: expected {path} = {val!r}, found {cur!r}")
        for path, val in (p.get("set") or {}).items():
            put(c, path, val)
        for field, old, new in p.get("replace", []):
            cur = get(c, field)
            if cur.count(old) != 1:
                errors.append(f"#{n} {cid}: '{old[:60]}' occurs {cur.count(old)} times in {field}"); continue
            put(c, field, cur.replace(old, new))
        for idx, field, val in p.get("evidence_set", []):
            c["evidence"][idx][field] = val
        for a in p.get("evidence_add", []):
            a = dict(a)
            a.setdefault("anchor_status", "ai-located"); a.setdefault("located_on", TODAY)
            a.setdefault("located_by", "editor, from the study card or the source text")
            a.setdefault("study_card", "sc_" + a["reference"].replace("-", "_"))
            for k in ("reference", "page", "locator", "extracted", "role"):
                if not a.get(k):
                    errors.append(f"#{n} {cid}: added anchor lacks '{k}'")
            c["evidence"].append(a)
        # a claim the senior author has approved, edited afterwards, returns to the rung its anchors support and its review
        # becomes pending (METHODS §5.5): the decision was made on the earlier version
        before = files[f][i]
        content_changed = any(before.get(k) != c.get(k) for k in ("statement", "plain", "magnitude", "grade", "evidence", "relation", "status"))
        if content_changed and c.get("verification", {}).get("status") in ("appraised", "senior-reviewed", "published"):
            st = [e["anchor_status"] for e in c["evidence"]]
            c["verification"]["status"] = "anchor-verified" if all(x == "senior-verified" for x in st) else \
                "ai-anchored" if all(x in ("ai-checked", "senior-verified") for x in st) else "metadata-verified"
            c.setdefault("senior_review", {})["decision"] = "pending"
            p["change"] = p["change"] + " Changed after the senior author's decision: review pending again."
        # a new or reopened anchor that is not yet checked moves an ai-anchored claim back down the ladder (METHODS §12)
        if c.get("verification", {}).get("status") in ("ai-anchored", "anchor-verified") and \
                any(e["anchor_status"] not in ("ai-checked", "senior-verified") for e in c["evidence"]):
            c["verification"]["status"] = "metadata-verified"
            p["change"] = p["change"] + " Verification status back to metadata-verified until the new anchors are checked."
        if p.get("bump") not in ("patch", "minor"):
            errors.append(f"#{n} {cid}: bump must be 'patch' or 'minor'"); continue
        c["version"] = bump(c.get("version", "0.1.0"), p["bump"])
        c.setdefault("changelog", []).append({"version": c["version"], "date": TODAY, "change": p["change"]})
    if errors:
        print("NOT APPLIED:"); [print("  " + e) for e in errors]; sys.exit(1)
    changed = {f for f in work if work[f] != files[f]}
    for f in changed:
        if not dry:
            f.write_text(json.dumps(work[f], indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(("checked (dry run) " if dry else "applied ") + f"{len(patches)} patches to {len(changed)} file(s)")


if __name__ == "__main__":
    main()
