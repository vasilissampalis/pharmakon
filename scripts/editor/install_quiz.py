"""install_quiz.py DIR N [N ...] [--dry]: hold the myth-or-fact writers' statements (data/verification/DIR/<N>_mf.json) for
the blind check, in data/verification/quiz/pending.json, the way install_lines.py holds quiz items (apply_check.py moves the
checked ones onto the site). Only items marked keep, for answers on the site with their plain lines at the answer's current
version; v is set to that version. Dropped items and their reasons are listed in data/verification/DIR/dropped.json.
Problems are listed and the item skipped: an empty statement or why, an answer that is not true or false, a statement over 25
words."""
import json, glob, sys, os, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]; os.chdir(ROOT)
args = [a for a in sys.argv[1:] if not a.startswith("--")]; dry = "--dry" in sys.argv
d, ns = args[0], args[1:]
D = pathlib.Path(f"data/verification/{d}")
C = {}
for f in glob.glob("data/claims/*.json"):
    for c in json.load(open(f, encoding="utf-8")): C[c["id"]] = c
S = json.load(open("data/site/simple.json", encoding="utf-8"))["claims"]
PP = pathlib.Path("data/verification/quiz/pending.json")
P = json.load(open(PP, encoding="utf-8"))
dropped, held, skipped = [], [], []
for n in ns:
    W = json.load(open(D / f"{n}_mf.json", encoding="utf-8"))
    for it in W["items"]:
        k = it.get("claim")
        if not it.get("keep"): dropped.append({"claim": k, "kind": it.get("from"), "writer": n, "reason": it.get("reason", "")}); continue
        why = []
        if k not in C or k not in S or S[k].get("v") != C[k]["version"]: why.append("answer not on the site at its current version")
        st = (it.get("statement") or "").strip()
        if not st or not (it.get("why") or "").strip(): why.append("empty statement or why")
        if not isinstance(it.get("answer"), bool): why.append("answer is not true or false")
        if len(st.split()) > 25: why.append(f"statement of {len(st.split())} words")
        if why: skipped.append(f"{k}: {'; '.join(why)}"); continue
        item = {"claim": k, "statement": st, "answer": it["answer"], "v": C[k]["version"], "why": it["why"].strip()}
        if it.get("alt_of"): item["alt_of"] = it["alt_of"]     # two wordings of one fact: the checker passes at most one (apply_check.py takes the mark off again)
        P["tf"] = [x for x in P["tf"] if (x["claim"], x["item"]["statement"]) != (k, st)]
        entry = {"claim": k, "page": it.get("page") or C[k]["substance"], "item": item}
        if it.get("old_statement"): entry["replaces"] = it["old_statement"]   # a clearer wording of a card already on the site: if it passes, the old card leaves
        P["tf"].append(entry); held.append(k)
print("held for the blind check:", len(held), "statements;", "dropped:", len(dropped))
for s in skipped: print("!! skipped", s)
if not dry:
    with open(PP, "w", encoding="utf-8") as f: json.dump(P, f, ensure_ascii=False, indent=1); f.write("\n")
    with open(D / "dropped.json", "w", encoding="utf-8") as f: json.dump(dropped, f, ensure_ascii=False, indent=1); f.write("\n")
