"""gaps.py [--write]: what the site is missing, found from its own data (15 November 2026).

The senior author: "i wonder if insight should understand itself what's missing from the website like pictures, law
information, country information ... and prioritize what users really want to read". This is that list, worked out by
rule from the data, never by guessing: drug forms without a photo, drugs without a description, drug families without
"for you" lines, countries without emergency numbers or a line on test kits, the most-asked themes with few answers,
Myth or fact decks with few cards people care about, and answers Insight has no wordings for. `--write` saves
data/site/gaps.json (read by the to-do page and by the nightly run); without it, prints the summary only."""
import json, re, sys, pathlib, hashlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
J = lambda p: json.load(open(ROOT / p, encoding="utf-8"))
E = lambda p: (ROOT / p).exists()
subs = J("data/site/substances.json"); slugs = [s["slug"] for s in subs]; name = {s["slug"]: s["name"] for s in subs}
out = {"_note": "What the site is missing, worked out from its own data by scripts/editor/gaps.py. Nothing here is a claim; it is a work list.", "made_on": None}
# photos
forms = J("data/site/forms.json")
out["forms_without_photo"] = [{"drug": d, "form": f["name"], "what": f.get("what", "")} for d, fs in forms.items() if isinstance(fs, list) for f in fs if not f.get("photos")]
# descriptions and "for you" lines
desc = J("data/site/descriptions.json")["drugs"] if E("data/site/descriptions.json") else {}
out["drugs_without_description"] = [d for d in slugs if not (desc.get(d) or {}).get("lines")]
signs = J("data/site/stay-safer.json")["signs"]
out["families_without_for_you"] = [f for f, s in signs.items() if not s.get("self")]
# countries
world = J("data/site/world-law.json")["countries"]
allc = [c.get("name") or c.get("country") for c in world]
em = {c["country"] for c in J("data/site/emergency.json")["countries"]}
tw = J("data/site/tests-world.json"); kitlaw = {x["country"] for x in tw["law"]}
dc = J("data/site/drug-checking.json"); svc = {s["country"] for s in dc["services"]}
out["countries"] = {"all": len(allc), "with_emergency_numbers": len(em & set(allc)) or len(em), "without_emergency_numbers": sorted(set(allc) - em),
                    "with_test_kit_law": len(kitlaw), "without_test_kit_law": sorted(set(allc) - kitlaw), "with_a_drug_checking_service": len(svc)}
# answers per drug, and the most-asked themes with few answers
Q = J("data/site/questions.json")
per = {p: len({it[0] for g in gs for it in g["items"]}) for p, gs in Q.items() if isinstance(gs, list)}
out["answers_per_page"] = dict(sorted(per.items(), key=lambda kv: kv[1]))
themes = []
md = ROOT / "data/verification/demand-themes.md"
if md.exists():
    for line in md.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*[\d.]+\s*\|\s*[\d.]+\s*\|\s*([\d.]+)%\s*\|\s*(\d+)\s*\|", line)
        if m and not m.group(2).rstrip().endswith("(no)"): themes.append({"rank": int(m.group(1)), "theme": m.group(2), "demand_percent": float(m.group(3)), "answers": int(m.group(4))})
out["most_asked_themes_with_few_answers"] = [t for t in themes if t["answers"] <= 3][:25]
# Myth or fact
S = J("data/site/simple.json")
ti = J("data/site/tf-interest.json") if E("data/site/tf-interest.json") else None
decks = {}
for deck, cards in S["tf"].items():
    keep = 0
    for c in cards:
        k = hashlib.sha1(c["statement"].encode("utf-8")).hexdigest()[:12]; r = (ti or {}).get("items", {}).get(k)
        if not ti or not r or (r["interest"] >= ti["cut"]["interest"] and r["clear"] >= ti["cut"]["clear"]): keep += 1
    decks[deck] = {"cards": len(cards), "kept": keep}
out["myth_or_fact_decks"] = decks
# Insight
var = J("data/verification/insight/variants_reader696.json")["variants"] if E("data/verification/insight/variants_reader696.json") else {}
out["answers_without_wordings"] = sorted(set(S["claims"]) - set(var))
print(f"Photos: {len(out['forms_without_photo'])} drug forms have no photo: " + "; ".join(f"{name.get(x['drug'], x['drug']).split(' (')[0]}: {x['form']}" for x in out["forms_without_photo"]))
print(f"Descriptions: {len(out['drugs_without_description'])} of {len(slugs)} drugs have none. 'For you' lines: {len(out['families_without_for_you'])} of {len(signs)} families have none.")
c = out["countries"]; print(f"Countries: {c['all']} listed; emergency numbers for {len(em)}; a line on test-kit law for {c['with_test_kit_law']}; a drug checking service found in {c['with_a_drug_checking_service']}.")
print("Fewest answers:", ", ".join(f"{p} {n}" for p, n in list(out["answers_per_page"].items())[:10]))
print("Most-asked themes with 3 answers or fewer:"); [print(f"  {t['rank']:>3}. {t['theme']} ({t['demand_percent']}% of demand, {t['answers']} answers)") for t in out["most_asked_themes_with_few_answers"][:12]]
print(f"Myth or fact: {sum(d['kept'] for d in decks.values())} of {sum(d['cards'] for d in decks.values())} cards kept" + ("" if ti else " (no interest ratings yet)"))
print(f"Insight: {len(out['answers_without_wordings'])} answers have no extra wordings.")
if "--write" in sys.argv:
    import datetime; out["made_on"] = datetime.date.today().isoformat()
    (ROOT / "data/site/gaps.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"); print("wrote data/site/gaps.json")
