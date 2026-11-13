#!/usr/bin/env python3
"""Apply the senior author's decisions from the site's database to the claim and study-card files (METHODS §5.5, §12;
WORKFLOW step 11).

Export the three collections first with the ArtifactData tool (`list` with `out_dir`), which writes
<export-dir>/reviews/<claim>.json, <export-dir>/anchors/<claim>.json and <export-dir>/cards/<card>.json. Then:

  apply_senior_review.py <export-dir> [--dry-run]

- An anchor ticked by the senior author becomes 'senior-verified' (checked_by 'Senior author', checked_on the tick date);
  an anchor note is kept in the anchor as `senior_note`.
- A study card marked read against its source becomes 'appraised' (reviewed_by 'Senior author', reviewed_on the date);
  an unticked card that was appraised is reported, not changed.
- The ladder (METHODS §12) is then recomputed for each claim: 'anchor-verified' when every anchor is senior-verified;
  'appraised' when, in addition, every study card the claim rests on is appraised; 'senior-reviewed' when, in addition,
  the senior author approved the claim (with or without edits) on its current version.
- A claim decision is copied to `senior_review` {decision, note, date, claim_version}. A decision made on an older claim
  version is reported and not applied: the claim changed after the review. 'flagged' is recorded with its note and does
  not change the claim's status; the editor reworks the claim (METHODS §12: 'flagged' as a status is for post-publication
  issues).
"""
import json, sys, glob, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
exp = pathlib.Path(sys.argv[1]); dry = "--dry-run" in sys.argv
ORDER = ["draft", "metadata-verified", "ai-anchored", "anchor-verified", "appraised", "senior-reviewed", "published", "flagged"]

def load_dir(name):
    out = {}
    for f in glob.glob(str(exp / name / "*.json")):
        d = json.load(open(f, encoding="utf-8"))
        body = d.get("data", d) if isinstance(d, dict) else d
        out[pathlib.Path(f).stem] = body
    return out

reviews, anchors, cardmarks = load_dir("reviews"), load_dir("anchors"), load_dir("cards")
changed = 0; notes = []

# 1. study cards read against their sources -> appraised
card_status = {}
for cf in sorted(glob.glob(str(ROOT / "data" / "study-cards" / "*.json"))):
    cards = json.load(open(cf, encoding="utf-8")); dirty = False
    for k in cards:
        mark = cardmarks.get(k["id"]) or {}
        v = k["verification"]
        if mark.get("read") and v["status"] != "appraised":
            if v["status"] == "draft":
                notes.append(f"{k['id']}: marked read, but the card is a draft (abstract or placeholders) — not appraised");
            else:
                v["status"] = "appraised"; v["reviewed_by"] = "Senior author"; v["reviewed_on"] = mark.get("date", "")
                dirty = True; changed += 1
        elif not mark.get("read") and v["status"] == "appraised" and k["id"] in cardmarks:
            notes.append(f"{k['id']}: appraised in the files but unticked in the review queue — left as it is; check")
        card_status[k["id"]] = v["status"]
    if dirty and not dry:
        json.dump(cards, open(cf, "w", encoding="utf-8"), indent=1, ensure_ascii=False); open(cf, "a").write("\n")

# 2. anchors and claim decisions
for cf in sorted(glob.glob(str(ROOT / "data" / "claims" / "*.json"))):
    claims = json.load(open(cf, encoding="utf-8")); dirty = False
    for c in claims:
        a = (anchors.get(c["id"]) or {}).get("checks") or {}
        for i, e in enumerate(c["evidence"]):
            chk = a.get(str(i))
            if chk and chk.get("ok") and e["anchor_status"] != "senior-verified":
                if e["anchor_status"] == "unchecked":
                    notes.append(f"{c['id']} anchor {i}: ticked but still a placeholder — not applied"); continue
                e["anchor_status"] = "senior-verified"; e["checked_by"] = "Senior author"; e["checked_on"] = chk.get("date", "")
                dirty = True; changed += 1
            if chk and chk.get("note") and e.get("senior_note") != chk["note"]:
                e["senior_note"] = chk["note"]; dirty = True
        r = reviews.get(c["id"])
        current = bool(r and r.get("decision") and (not r.get("claim_version") or r["claim_version"] == c.get("version")))
        if r and r.get("decision") and not current:
            notes.append(f"{c['id']}: decision '{r['decision']}' was made on v{r['claim_version']}, claim is now v{c.get('version')} — re-review needed")
        if current:
            sr = {"decision": r["decision"], "note": r.get("note", ""), "date": r.get("date", ""), "claim_version": c.get("version")}
            if c.get("senior_review") != sr:
                c["senior_review"] = sr; dirty = True; changed += 1
            if r["decision"] == "approved-with-edits":
                notes.append(f"{c['id']}: approved with edits — apply: {r.get('note','')}")
            if r["decision"] == "flagged":
                notes.append(f"{c['id']}: FLAGGED in review — {r.get('note','')} (status unchanged; rework the claim)")
        # recompute the ladder from what is now true (never above what the evidence supports)
        st = c["verification"]["status"]
        if st in ("published", "flagged"):
            continue
        anchors_ok = all(e["anchor_status"] == "senior-verified" for e in c["evidence"])
        cards_ok = all(card_status.get(e["study_card"]) == "appraised" for e in c["evidence"])
        approved = current and r["decision"] in ("approved", "approved-with-edits")
        new = st
        if anchors_ok and ORDER.index(st) < ORDER.index("anchor-verified"):
            new = "anchor-verified"
        if anchors_ok and cards_ok and ORDER.index(new) < ORDER.index("appraised"):
            new = "appraised"
        if anchors_ok and cards_ok and approved:
            new = "senior-reviewed"
            c["verification"]["reviewed_by"] = "Senior author"; c["verification"]["reviewed_on"] = r.get("date", "")
        elif approved:
            notes.append(f"{c['id']}: approved, but " + ("not every anchor is senior-verified" if not anchors_ok else "not every study card is appraised") + f" — status {new}")
        if new != st:
            c["verification"]["status"] = new; dirty = True; changed += 1
    if dirty and not dry:
        json.dump(claims, open(cf, "w", encoding="utf-8"), indent=1, ensure_ascii=False); open(cf, "a").write("\n")
print(f"{'would apply' if dry else 'applied'} {changed} changes")
for n in notes:
    print(" -", n)
