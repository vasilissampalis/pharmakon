#!/usr/bin/env python3
"""Move staged claims from data/claims/_incoming/<file>.json into data/claims/<substance>.json (WORKFLOW step 11).

Usage: merge_claims.py STAGED.json CLAIM_ID [CLAIM_ID ...] [--dry-run]

A claim is merged only if it validates against schema/claim.schema.json, every reference it cites has a record in
data/references/, every study card it cites is in the merged cards (any data/study-cards/*.json file), and its id is not
already in the target file. Each merged claim gets a patch version and a changelog line; a copy of each merged claim as it
was staged is kept in data/claims/_merged/. Claims not named stay staged. Adding the claim to its monograph section is a
separate, deliberate edit (the section list decides where it appears).
"""
import json, sys, glob, pathlib, datetime
import jsonschema

ROOT = pathlib.Path(__file__).resolve().parents[1]
TODAY = datetime.date.today().isoformat()


def bump_patch(v):
    a, b, c = (int(x) for x in v.split("."))
    return f"{a}.{b}.{c + 1}"


def main():
    args = [a for a in sys.argv[1:] if a != "--dry-run"]
    dry = "--dry-run" in sys.argv
    if len(args) < 2:
        sys.exit(__doc__)
    staged_path = pathlib.Path(args[0]).resolve()
    want = args[1:]
    staged = json.load(open(staged_path, encoding="utf-8"))
    schema = json.load(open(ROOT / "schema" / "claim.schema.json", encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    refs = set()
    for f in glob.glob(str(ROOT / "data" / "references" / "*.json")):
        refs |= {r["id"] for r in json.load(open(f, encoding="utf-8"))}
    by_id = {c["id"]: c for c in staged}
    errors, plan = [], {}
    for cid in want:
        c = by_id.get(cid)
        if c is None:
            errors.append(f"{cid}: not in {staged_path.name}"); continue
        target = ROOT / "data" / "claims" / f"{c['substance']}.json"
        # a claim may cite a card filed under another substance (for example a review covering several drugs, in cross-cutting.json):
        # the site loads every merged card file, so any of them counts
        cards = {k["id"] for f in sorted((ROOT / "data" / "study-cards").glob("*.json")) for k in json.load(open(f, encoding="utf-8"))}
        for e in validator.iter_errors(c):
            errors.append(f"{cid}: schema /{'/'.join(map(str, e.path))}: {e.message[:120]}")
        for e in c["evidence"]:
            if e["reference"] not in refs: errors.append(f"{cid}: reference {e['reference']} has no record")
            if e["study_card"] not in cards: errors.append(f"{cid}: study card {e['study_card']} is not merged")
        plan.setdefault(target, []).append(c)
    for target, cs in plan.items():
        existing = {c["id"] for c in json.load(open(target, encoding="utf-8"))} if target.exists() else set()
        for c in cs:
            if c["id"] in existing: errors.append(f"{c['id']}: already in {target.name}")
    if errors:
        print("not merged:"); print("\n".join("  " + e for e in errors)); sys.exit(1)
    if dry:
        print(f"checked (dry run): {', '.join(want)}"); return
    keep = ROOT / "data" / "claims" / "_merged"
    keep.mkdir(parents=True, exist_ok=True)
    for target, cs in plan.items():
        current = json.load(open(target, encoding="utf-8")) if target.exists() else []
        for c in cs:
            (keep / f"{c['id']}.{c['version']}.json").write_text(json.dumps(c, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            c["version"] = bump_patch(c["version"])
            c.setdefault("changelog", []).append({"version": c["version"], "date": TODAY,
                                                  "change": f"Moved from staging ({staged_path.parent.name}/{staged_path.name}) into the monograph's claims; no change of text, rating or status."})
            current.append(c)
        target.write_text(json.dumps(current, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    rest = [c for c in staged if c["id"] not in want]
    staged_path.write_text(json.dumps(rest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"merged {len(want)}: {', '.join(want)}; {len(rest)} left staged in {staged_path.name}")


if __name__ == "__main__":
    main()
