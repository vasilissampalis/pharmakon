#!/usr/bin/env python3
"""Merge checked study cards from data/study-cards/_incoming/<substance>/ into data/study-cards/<substance>.json.

A card is merged only if check_card.py passes and its reference record exists. An existing card with the
same id is replaced (the replaced version is kept in data/study-cards/_superseded/). Merged incoming files
move to data/study-cards/_merged/<substance>/. Prints what was merged and what was held back, and why.
"""
import json, glob, pathlib, shutil, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from check_card import check

ROOT = pathlib.Path(__file__).resolve().parents[1]
refs = set()
for f in glob.glob(str(ROOT / "data" / "references" / "*.json")):
    refs |= {r["id"] for r in json.load(open(f, encoding="utf-8"))}

only = set(sys.argv[1:])  # optional: merge only these card ids
merged, held = [], []
for sub_dir in sorted(glob.glob(str(ROOT / "data" / "study-cards" / "_incoming" / "*"))):
    sub = pathlib.Path(sub_dir).name
    target = ROOT / "data" / "study-cards" / f"{sub}.json"
    cards = json.load(open(target, encoding="utf-8")) if target.exists() else []
    index = {c["id"]: i for i, c in enumerate(cards)}
    changed = False
    for fp in sorted(glob.glob(sub_dir + "/*.json")):
        if only and pathlib.Path(fp).stem not in only: continue
        fails, _ = check(fp)
        card = json.load(open(fp, encoding="utf-8"))
        if fails:
            held.append((fp, "check failed: " + fails[0])); continue
        if card["reference"] not in refs:
            held.append((fp, f"reference {card['reference']} not built yet")); continue
        if card["id"] in index:
            old = cards[index[card["id"]]]
            sup = ROOT / "data" / "study-cards" / "_superseded" / sub
            sup.mkdir(parents=True, exist_ok=True)
            (sup / f"{card['id']}.{old['verification'].get('first_pass_on', 'old')}.json").write_text(json.dumps(old, indent=1, ensure_ascii=False), encoding="utf-8")
            cards[index[card["id"]]] = card
        else:
            index[card["id"]] = len(cards); cards.append(card)
        dest = ROOT / "data" / "study-cards" / "_merged" / sub
        dest.mkdir(parents=True, exist_ok=True)
        shutil.move(fp, dest / pathlib.Path(fp).name)
        merged.append(card["id"]); changed = True
    if changed:
        target.write_text(json.dumps(cards, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"merged {len(merged)}: {', '.join(merged)}")
for fp, why in held:
    print(f"held  {pathlib.Path(fp).name}: {why}")
