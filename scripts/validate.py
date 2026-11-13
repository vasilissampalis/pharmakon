#!/usr/bin/env python3
"""Pre-publish validation (METHODS.md §11): schemas, citation integrity, verification flags.
Exit code 1 on any hard failure. Warnings are printed for things allowed in draft but not at publication."""
import json, re, glob, sys, pathlib, datetime
import jsonschema

ROOT = pathlib.Path(__file__).resolve().parents[1]
_GATE = (lambda f: json.load(open(f, encoding="utf-8")) if f.exists() else {})(ROOT / "data" / "verification" / "senior-gate.json")  # section 7 approvals by the senior author
def load(p): return json.load(open(p, encoding="utf-8"))
def validate(schema, items, label):
    v = jsonschema.Draft202012Validator(load(ROOT / "schema" / schema)); n = 0
    for it in items:
        for e in v.iter_errors(it):
            n += 1; print(f"  SCHEMA {label} {it.get('id', it.get('slug','?'))}: /{'/'.join(map(str,e.path))}: {e.message[:120]}")
    return n

fails = 0; warns = 0
QUOTED = re.compile(r"“[^”]*”|\"[^\"]*\"|(?<![A-Za-z])'[^']{12,}?'(?![A-Za-z])")
def unquoted(t):
    """Text with quoted source wording removed: quotations keep the source's words (METHODS §9)."""
    return QUOTED.sub(" ", t or "")
refs = []
for f in sorted(glob.glob(str(ROOT / "data/references/*.json"))): refs += load(f)
cards = []
for f in sorted(glob.glob(str(ROOT / "data/study-cards/*.json"))): cards += load(f)
claims = []
for f in sorted(glob.glob(str(ROOT / "data/claims/*.json"))): claims += load(f)
monos = [load(f) for f in sorted(glob.glob(str(ROOT / "data/monographs/*.json")))]
epi = []
for f in sorted(glob.glob(str(ROOT / "data/epidemiology/*.json"))): epi += load(f)

fails += validate("reference.schema.json", refs, "reference")
fails += validate("study-card.schema.json", cards, "study-card")
fails += validate("claim.schema.json", claims, "claim")
fails += validate("monograph.schema.json", monos, "monograph")
fails += validate("epidemiology-figure.schema.json", epi, "epidemiology")
legal = [load(f) for f in sorted(glob.glob(str(ROOT / "data/legal/*.json")))]
ident = [load(f) for f in sorted(glob.glob(str(ROOT / "data/identity/*.json")))]
fails += validate("legal.schema.json", legal, "legal")
fails += validate("identity.schema.json", ident, "identity")

# Identity sections (METHODS §10.3): sources resolve, CAS check digits, formula against molar mass, held findings
CAS_RN = re.compile(r"(?<![\d-])(\d{2,7})-(\d{2})-(\d)(?![\d-])")
ATOMIC = {"C": 12.011, "H": 1.008, "N": 14.007, "O": 15.999, "P": 30.974, "Cl": 35.45, "S": 32.06, "Na": 22.990, "Br": 79.904, "F": 18.998, "He": 4.0026, "Si": 28.085, "B": 10.81, "I": 126.904, "K": 39.098}
def _mass(formula):
    tot = 0.0
    for el, k in re.findall(r"([A-Z][a-z]?)(\d*)", formula):
        if el not in ATOMIC: return None
        tot += ATOMIC[el] * (int(k) if k else 1)
    return tot
for d in ident:
    sid = {s["id"] for s in d.get("sources", [])}; used = set(d.get("names", {}).get("source_ids", []))
    for k in ("members", "forms", "street_names", "drug_checking"):
        for x in d.get(k, []): used |= set(x.get("source_ids", []))
    for i in sorted(used - sid): print(f"  FAIL identity {d['substance']}: source id {i} is not in its sources"); fails += 1
    for i in sorted(sid - used): print(f"  WARN identity {d['substance']}: source {i} is listed but supports nothing"); warns += 1
    n = d.get("names", {})
    for t in list(n.get("cas", [])) + [x.get("detail", "") for x in d.get("forms", [])] + [c for mb in d.get("members", []) for c in mb.get("cas", [])]:
        for a, b, c in CAS_RN.findall(re.sub(r"(?<![A-Za-z])'[^']*'(?![A-Za-z])|\"[^\"]*\"|“[^”]*”", " ", t)):  # a misprint quoted from a source keeps the source's wording
            if sum((j + 1) * int(x) for j, x in enumerate((a + b)[::-1])) % 10 != int(c):
                print(f"  FAIL identity {d['substance']}: CAS {a}-{b}-{c} fails its check digit"); fails += 1
    for who, blk in [("", n)] + [(" (" + mb.get("name", "?") + ")", mb) for mb in d.get("members", [])]:
        fm = re.match(r"\s*([A-Z][A-Za-z0-9]*)", blk.get("formula", "") or ""); mm = re.match(r"\s*(\d+(?:\.\d+)?)", blk.get("molar_mass", "") or "")
        if fm and mm and (_mass(fm.group(1)) is None or abs(_mass(fm.group(1)) - float(mm.group(1))) > 0.05):
            print(f"  WARN identity {d['substance']}{who}: molar mass {mm.group(1)} does not match formula {fm.group(1)}"); warns += 1
    held = [x for x in d.get("drug_checking", []) if x.get("hold")]
    if held: print(f"  WARN identity {d['substance']}: {len(held)} drug-checking finding(s) held (not shown) until read in full text"); warns += 1

ref_ids = {r["id"] for r in refs}; card_ids = {c["id"] for c in cards}; claim_ids = {c["id"] for c in claims}
card_status = {c["id"]: c["verification"]["status"] for c in cards}
dup = len(refs) - len(ref_ids)
if dup: print(f"  FAIL duplicate reference ids: {dup}"); fails += dup
for c in claims:
    if not c["evidence"]: print(f"  FAIL claim {c['id']} has no evidence"); fails += 1
    for e in c["evidence"]:
        if e["reference"] not in ref_ids: print(f"  FAIL claim {c['id']} cites unknown reference {e['reference']}"); fails += 1
        if e["study_card"] not in card_ids: print(f"  FAIL claim {c['id']} points to unknown study card {e['study_card']}"); fails += 1
        if e["anchor_status"] != "senior-verified": warns += 1
        if e["anchor_status"] in ("ai-located", "ai-checked", "senior-verified") and any("[to be" in e[k] for k in ("page", "locator", "extracted")):
            print(f"  FAIL claim {c['id']} anchor to {e['reference']} is marked {e['anchor_status']} but still has a placeholder"); fails += 1
        q = e.get("quote")
        if q and len(q.split()) > 15:
            print(f"  FAIL claim {c['id']} quotes {len(q.split())} words from {e['reference']} (limit 15, METHODS §4.5)"); fails += 1
    if sum(1 for e in c["evidence"] if e.get("quote")) > 1:
        print(f"  FAIL claim {c['id']} has more than one quotation (METHODS §4.5)"); fails += 1
    if c["status"] == "contested" and not c.get("debate"): print(f"  FAIL contested claim {c['id']} has no debate box"); fails += 1
    # GRADE arithmetic (METHODS §6.3): certainty = start − downgrades + upgrades, bounded to very low … high
    g = c["grade"]; d = g["domains"]
    lv = ["very-low", "low", "moderate", "high"]
    down = sum(d[k]["levels"] for k in ("risk_of_bias", "inconsistency", "indirectness", "imprecision", "publication_bias"))
    up = sum(d.get(k, {"levels": 0})["levels"] for k in ("large_effect", "dose_response", "plausible_confounding"))
    expect = lv[max(0, min(3, (3 if g["starting_level"] == "high" else 1) - down + up))]
    if g["certainty"] != expect:
        print(f"  FAIL claim {c['id']} GRADE arithmetic: starts {g['starting_level']}, −{down} +{up} gives {expect}, not {g['certainty']}"); fails += 1
    if up and g["starting_level"] == "high":
        print(f"  FAIL claim {c['id']} upgrades evidence that starts high (upgrades apply to observational evidence only)"); fails += 1
    # status ladder (METHODS §12)
    vs = c["verification"]["status"]; st = [e["anchor_status"] for e in c["evidence"]]
    if vs == "ai-anchored" and any(x not in ("ai-checked", "senior-verified") for x in st):
        print(f"  FAIL claim {c['id']} is ai-anchored but not every anchor is ai-checked"); fails += 1
    if vs in ("anchor-verified", "appraised", "senior-reviewed", "published") and any(x != "senior-verified" for x in st):
        print(f"  FAIL claim {c['id']} is {vs} but not every anchor is senior-verified"); fails += 1
    if vs != "draft" and "unchecked" in st:
        print(f"  FAIL claim {c['id']} is {vs} but has unchecked anchors"); fails += 1
    if vs in ("senior-reviewed", "published") and (c.get("senior_review") or {}).get("decision") not in ("approved", "approved-with-edits"):
        print(f"  FAIL claim {c['id']} is {vs} without a senior-author approval"); fails += 1
    if vs in ("appraised", "senior-reviewed", "published"):
        unread = sorted({e["study_card"] for e in c["evidence"] if card_status.get(e["study_card"]) != "appraised"})
        if unread:
            print(f"  FAIL claim {c['id']} is {vs} but these study cards are not appraised by the senior author: {', '.join(unread)} (METHODS §5.5)"); fails += 1
    # language (METHODS §9)
    lang_fields = [(f, c.get(f) or "") for f in ("statement", "plain", "magnitude", "population", "exposure", "comparator", "outcome")]
    lang_fields += [("grade.reasoning", c["grade"].get("reasoning") or "")] + [(f"evidence[{i}].extracted", e.get("extracted") or "") for i, e in enumerate(c["evidence"])]
    lang_fields += [("debate." + k, v) for k, v in (c.get("debate") or {}).items() if isinstance(v, str)]
    for fld, raw in lang_fields:
        txt = raw.lower()
        for term in ("addict", "abuser", "junkie", "clean urine", "dirty urine", "harmless", "devastating"):
            if term in txt:
                print(f"  WARN claim {c['id']} {fld} uses '{term}' (METHODS §9)"); warns += 1
        if re.search(r"\bcl_[a-z]+_\w+", raw):
            print(f"  WARN claim {c['id']} {fld} shows a raw claim identifier; use a readable cross-reference"); warns += 1
        if re.search(r"\b(non-)?users?\b", unquoted(txt)):
            print(f"  WARN claim {c['id']} {fld} uses 'user(s)'; write 'people who use…' (METHODS §9)"); warns += 1
    if c["relation"] == "causes" and c["grade"]["certainty"] in ("low", "very-low") and c["grade"]["starting_level"] != "high":
        print(f"  WARN claim {c['id']} uses 'causes' with {c['grade']['certainty']} certainty from observational evidence"); warns += 1
sys.path.insert(0, str(ROOT / 'scripts'))
from rob_vocab import problems as rob_problems, design_problems, amstar_item_problems
for sc in cards:
    for pr in rob_problems(sc):
        print(f"  FAIL study card {sc['id']}: {pr} (METHODS §5.3)"); fails += 1
    for pr in amstar_item_problems(sc):
        # reported, not failed, until the readers re-decide these items (a matter of judgment: yes or no)
        print(f"  WARN study card {sc['id']}: {pr} (METHODS §5.3)"); warns += 1
    for pr in design_problems(sc):
        # reported, not failed, while the re-appraisal of narrative reviews (protocol 0.2.2) is under way; see docs/STATUS.md
        print(f"  WARN study card {sc['id']}: {pr} (METHODS §5.3; re-appraisal pending)"); warns += 1
# a claim below the rung its anchors and references support is reported (METHODS §12): it may move up
ref_status = {r["id"]: r["verification"]["status"] for r in refs}
for c in claims:
    st = c["verification"]["status"]
    if st in ("draft", "metadata-verified") and all(e["anchor_status"] in ("ai-checked", "senior-verified") for e in c["evidence"]) \
            and all(ref_status.get(e["reference"]) not in (None, "unverified") for e in c["evidence"]) \
            and not all((next((k for k in cards if k["id"] == e["study_card"]), {}) or {}).get("design") in ("narrative-review", "commentary", "editorial") for e in c["evidence"]):
        print(f"  WARN claim {c['id']} is {st} but every anchor is checked and every reference verified: it may move up to ai-anchored (METHODS §12)"); warns += 1
# claims resting only on narrative reviews stay at draft and stay out of the at-a-glance box (METHODS §6.3)
NARRATIVE = {"narrative-review", "commentary", "editorial"}
card_design = {sc["id"]: sc.get("design") for sc in cards}
narrative_only = set()
for c in claims:
    sup = [e for e in c["evidence"] if e["role"] == "supports"]
    if sup and all(card_design.get(e["study_card"]) in NARRATIVE for e in sup):
        narrative_only.add(c["id"])
        if c["verification"]["status"] != "draft":
            print(f"  FAIL claim {c['id']} rests only on narrative reviews but is {c['verification']['status']}, not draft (METHODS §6.3)"); fails += 1
        if not any(w in (c.get("statement") or "") for w in ("narrative review", "second-hand", "as summarized", "as described")):
            print(f"  WARN claim {c['id']} rests only on narrative reviews but its statement does not say so (METHODS §6.3)"); warns += 1
by_id = {c["id"]: c for c in claims}
LV = {"very-low": 1, "low": 2, "moderate": 3, "high": 4}
for m in monos:
    ag = m.get("at_a_glance") or {}
    for cid in ag.get("best_established", []):
        if cid in narrative_only:
            print(f"  FAIL monograph {m['slug']} shows {cid}, which rests only on narrative reviews, as best established (METHODS §8)"); fails += 1
        elif cid in claim_ids and by_id[cid]["verification"]["status"] == "draft":
            print(f"  WARN monograph {m['slug']} shows draft claim {cid} as best established"); warns += 1
    # §6.3: claims resting only on narrative reviews are never shown in the at-a-glance box (methods audit M16)
    for cid in ag.get("largest_uncertainties", []):
        if cid in narrative_only:
            print(f"  FAIL monograph {m['slug']} lists {cid}, which rests only on narrative reviews, among the largest uncertainties (METHODS §6.3, §8)"); fails += 1
        elif cid in claim_ids and not (by_id[cid]["grade"]["certainty"] == "very-low" or by_id[cid]["status"] == "contested"):
            print(f"  FAIL monograph {m['slug']} lists {cid} among the largest uncertainties, but it is neither very low certainty nor contested (METHODS §8)"); fails += 1
    # §8: best-established facts ordered by certainty
    be = [by_id[c] for c in ag.get("best_established", []) if c in by_id]
    if any(LV[a["grade"]["certainty"]] < LV[b["grade"]["certainty"]] for a, b in zip(be, be[1:])):
        print(f"  WARN monograph {m['slug']}: best-established facts are not ordered by certainty (METHODS §8)"); warns += 1

# Language in other reader-facing text: monograph notes, site tables, legal and identity notes (METHODS §9; audit M29)
def _strings(o, at=""):
    if isinstance(o, dict):
        for k, v in o.items(): yield from _strings(v, f"{at}/{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from _strings(v, f"{at}[{i}]")
    elif isinstance(o, str): yield at, o
SKIP_KEYS = ("/title", "/source_title", "/url", "/source_url", "/page_or_table", "/locator", "/URL", "/changelog")
for label, obj in [("monograph", m) for m in monos] + [("glossary", load(ROOT / "data/site/glossary.json")), ("home figures", load(ROOT / "data/site/landing-stats.json"))] + [(f"legal {x.get('substance')}", x) for x in [load(f) for f in sorted(glob.glob(str(ROOT / "data/legal/*.json")))]] + [(f"identity {x.get('substance')}", {k: v for k, v in x.items() if k != "sources"}) for x in ident] + [(f"statistics {r['id']}", {k: r.get(k) for k in ("measure_definition", "population", "denominator_note", "display")}) for r in epi]:
    for at, t in _strings(obj):
        if any(k in at for k in SKIP_KEYS): continue
        if re.search(r"\b(non-)?users?\b", unquoted(t), re.I):
            print(f"  WARN {label} {at}: 'user(s)' (METHODS §9)"); warns += 1

# Quotations over 15 words in statistics (after display trimming), legal and identity text (METHODS §4.5; audit M27)
import subprocess
try:
    out = subprocess.run(["node", str(ROOT / "scripts" / "quote_limits.js")], capture_output=True, text=True, timeout=60)
    if out.returncode != 0:
        for line in out.stdout.splitlines():
            if line.startswith(("STILL LONG", "LONG QUOTE")): print("  FAIL " + line[:200] + " (METHODS §4.5)"); fails += 1
except Exception as e:
    print(f"  WARN quotation check not run: {e}"); warns += 1

# Home-page figures are presentation only: each points to a schema-checked statistics record (METHODS §10.2; audit M42)
epi_by_id = {r["id"]: r for r in epi}
for t in load(ROOT / "data/site/landing-stats.json"):
    r = epi_by_id.get(t.get("epi_id"))
    if not r:
        print(f"  FAIL home figure {t['id']} points to no statistics record (epi_id {t.get('epi_id')})"); fails += 1; continue
    nums = re.findall(r"\d+(?:\.\d+)?", str(t["value"]).replace(" ", "").replace(",", ""))
    if not nums or abs(float(nums[-1]) - float(r["value"])) > 1e-9:
        print(f"  FAIL home figure {t['id']} shows {t['value']!r} but its record {r['id']} holds {r['value']}"); fails += 1
    if (t.get("status") == "verified") != (r["verification"]["status"] == "verified"):
        print(f"  FAIL home figure {t['id']} is {t.get('status')} but its record {r['id']} is {r['verification']['status']}"); fails += 1

# Further mechanical rules (methods audit M8, M26, M33, M37, M38)
sys.path.insert(0, str(ROOT / "scripts"))
from check_card import check_card
for sc in cards:
    f, _ = check_card(sc)
    f = [x for x in f if not x.startswith(("schema ", "risk of bias:"))]  # already counted above
    if f and sc["verification"]["status"] != "draft":
        for x in f: print(f"  FAIL study card {sc['id']}: {x} (METHODS §5)"); fails += 1
    elif f:
        print(f"  WARN study card {sc['id']} (draft): {len(f)} card-check problems, e.g. {f[0][:90]}"); warns += 1
    rb = sc.get("risk_of_bias") or {}
    if rb.get("instrument") == "AMSTAR 2" and any(d.get("judgment") == "no-information" for d in rb.get("domains", [])) \
            and "provisional" not in (rb.get("reasoning") or "").lower():
        print(f"  WARN study card {sc['id']}: an AMSTAR 2 item is 'no-information' but the rating is not marked provisional (METHODS §5.3)"); warns += 1
    if rb.get("instrument") == "JBI-prevalence":
        for d in rb.get("domains", []):
            if d.get("judgment") == "partial-yes" and not (d.get("note") or "").strip():
                print(f"  WARN study card {sc['id']}: JBI 'partial yes' without its reason (METHODS §5.3)"); warns += 1
PRECLINICAL = {"preclinical-animal", "in-vitro"}
for c in claims:
    for i, e in enumerate(c["evidence"]):
        lb = e.get("located_by") or ""
        # an anchor written by the second reader needs independent confirmation: a matching first-reader card finding,
        # or a check at the stated place by a reader who wrote neither the anchor nor that finding (METHODS §5.5)
        # "AI reader 2" is the round-1 second reader; readers 20, 21, 22 … are other readers (the number must end there)
        r2 = lambda t: re.match(r"AI reader 2(?!\d)", t or "") is not None
        if e["anchor_status"] == "ai-checked" and r2(lb) and "card sc_" not in lb \
                and (r2(e.get("checked_by")) or (e.get("checked_by") or "").startswith("AI editor")):
            print(f"  FAIL claim {c['id']} anchor {i}: written by the second reader and not confirmed independently, so it cannot be ai-checked (METHODS §5.5)"); fails += 1
        if e["anchor_status"] == "ai-checked" and (e.get("checked_by") or "").startswith("AI editor"):
            print(f"  FAIL claim {c['id']} anchor {i}: checked by the editor, which is not a second reader's check (METHODS §5.5)"); fails += 1
        # nobody checks their own anchor: the checker must differ from the reader who located it (e.g. an adjudicator)
        base = lambda s: re.split(r" \(|,", s or "")[0].strip().lower()
        if e["anchor_status"] == "ai-checked" and lb and "card sc_" not in lb and base(lb) == base(e.get("checked_by")):
            print(f"  FAIL claim {c['id']} anchor {i}: checked by the same reader who located it ({base(lb)}) (METHODS §5.5)"); fails += 1
    if c["section"] == 7 and "senior" not in (c["verification"].get("drafted_by") or "").lower():
        # Decision p-ways-of-taking: the co-editor may draft section 7 comparisons as findings only; site/build.js leaves each one out of the page
        # until the senior author has approved that version (data/verification/senior-gate.json). Practical risk-reduction advice stays his alone.
        g7 = _GATE.get(c["id"]) or {}
        if not (str(g7.get("decision", "")).startswith("approved") and g7.get("version") == c.get("version")):
            print(f"  WARN claim {c['id']} is a section 7 draft by the co-editor: held off the site until the senior author approves this version (decision p-ways-of-taking; METHODS §1.2, §8)"); warns += 1
    g = c["grade"]; d = g["domains"]
    if c["relation"] == "describes" and d.get("large_effect", {}).get("levels", 0) > 0:
        print(f"  FAIL claim {c['id']} is descriptive but upgraded for a large effect (METHODS §6.3)"); fails += 1
    ups = sum(d.get(k, {"levels": 0})["levels"] for k in ("large_effect", "dose_response", "plausible_confounding"))
    if ups and d["risk_of_bias"]["levels"] > 0 and not re.search(r"strict|without (it|the upgrade|this upgrade|that upgrade)", g.get("reasoning", ""), re.I):
        print(f"  WARN claim {c['id']} upgrades evidence already rated down for risk of bias without stating the strict-reading certainty (METHODS §6.3)"); warns += 1
    sup = [e for e in c["evidence"] if e["role"] == "supports"]
    if sup and all(card_design.get(e["study_card"]) in PRECLINICAL for e in sup) and LV[g["certainty"]] > LV["low"]:
        print(f"  FAIL claim {c['id']} rests only on preclinical evidence but is rated above low (METHODS §5.4)"); fails += 1
    if c["relation"] in ("increases", "reduces") and g["certainty"] in ("low", "very-low") and g["starting_level"] != "high":
        print(f"  WARN claim {c['id']} uses '{c['relation']}' (causal) with {g['certainty']} certainty from observational evidence (METHODS §6.1)"); warns += 1
    sr = c.get("senior_review") or {}
    if c["verification"]["status"] in ("senior-reviewed", "published") and sr.get("claim_version") != c.get("version"):
        print(f"  FAIL claim {c['id']} is {c['verification']['status']} but the senior decision was made on version {sr.get('claim_version')}, not {c.get('version')} (METHODS §5.5)"); fails += 1
for sc in cards:
    if sc["reference"] not in ref_ids: print(f"  FAIL study card {sc['id']} references unknown {sc['reference']}"); fails += 1
cited = {e["reference"] for c in claims for e in c["evidence"]} | {t.get("reference") for sc in cards for t in (sc.get("replication", {}).get("timeline") or [])}
for m in monos:
    for s in m["sections"]:
        for cid in s["claims"]:
            if cid not in claim_ids: print(f"  FAIL monograph {m['slug']} section {s['number']} lists unknown claim {cid}"); fails += 1
            elif next(c for c in claims if c["id"] == cid)["section"] != s["number"] and s["number"] != 14:
                print(f"  WARN claim {cid} is in section {s['number']} but declares section {next(c for c in claims if c['id']==cid)['section']}"); warns += 1
for r in refs:
    v = r["verification"]
    if v["status"] == "unverified": print(f"  WARN reference {r['id']} metadata unverified"); warns += 1
    rc = v.get("retraction_check")
    if r.get("DOI") and (not rc or rc["status"] == "not-checked"): print(f"  WARN reference {r['id']} not retraction-checked"); warns += 1
    if rc and rc["status"] == "retracted":
        # METHODS §3.2: a retracted paper is never evidence. It may be cited only by a claim that documents the retraction
        # itself and names it in "documents_retraction"; any other claim citing it fails.
        users = [c["id"] for c in claims if any(e["reference"] == r["id"] for e in c["evidence"])]
        bad = [cid for cid in users if r["id"] not in (next(c for c in claims if c["id"] == cid).get("documents_retraction") or [])]
        if bad: print(f"  FAIL reference {r['id']} is RETRACTED and is cited as evidence by {', '.join(bad)}"); fails += 1
anchors = [e for c in claims for e in c["evidence"]]
by_status = {k: sum(1 for e in anchors if e["anchor_status"] == k) for k in ("unchecked", "ai-located", "ai-checked", "senior-verified")}
unverified = len(anchors) - by_status["senior-verified"]
for sc in cards:
    for kf in sc.get("key_findings", []):
        if "[" in kf["page"]: print(f"  WARN study card {sc['id']} has a key finding without a page"); warns += 1
print(f"references {len(refs)} · study cards {len(cards)} · claims {len(claims)} · monographs {len(monos)} · figures {len(epi)}")
print("evidence anchors: " + " · ".join(f"{k} {v}" for k, v in by_status.items()) + f" — not yet senior-verified: {unverified} (publication blocked until 0)")
print("study cards by status: " + " · ".join(f"{k} {sum(1 for c in cards if c['verification']['status']==k)}" for k in ("draft","first-pass","ai-checked","appraised")))
print(f"hard failures: {fails} · warnings: {warns}")
sys.exit(1 if fails else 0)
