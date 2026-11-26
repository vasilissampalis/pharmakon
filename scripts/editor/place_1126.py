"""place_1126.py [--dry]: put the new answers of round pdf-2026-11-26 on their home pages (data/site/questions.json, in people's
words from their plain lines) and the mixing answer in data/site/mix-drugs.json. Only answers with plain lines installed are
placed; an answer placed already is left alone; the nose-damage answer (section 7) waits for the senior author's approval and
the gabapentin answer for its last two anchors. Other pages show an answer through its plain lines' `pages`."""
import json, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
dry = "--dry" in sys.argv
QF, XF = ROOT / "data/site/questions.json", ROOT / "data/site/mix-drugs.json"
Q = json.load(open(QF, encoding="utf-8")); X = json.load(open(XF, encoding="utf-8"))
S = json.load(open(ROOT / "data/site/simple.json", encoding="utf-8"))["claims"]
PLACE = [  # (page, group, claim)
 ("general", "Addiction and recovery", "cl_gen_most_users_not_addicted"),
 ("general", "Drug tests", "cl_gen_drug_test_times"),
 ("general", "Drug tests", "cl_gen_drug_test_false_positives"),
 ("heroin", "After stopping", "cl_opi_vietnam_veterans"),
 ("mdma", "What it does to the body", "cl_mdma_peeing"),
 ("drug-checking", "What the tests find", "cl_dc_pill_logo"),
 ("lsd", "Fakes and look-alikes", "cl_lsd_nbome"),
 ("benzodiazepines", "What it feels like", "cl_benzo_liking"),
 ("benzodiazepines", "Who uses them and why", "cl_benzo_misuse_reasons"),
 ("benzodiazepines", "Street and designer benzos", "cl_benzo_designer"),
 ("benzodiazepines", "Mixing with alcohol", "cl_mix_benzodiazepines_alcohol"),
 ("interactions", "Depressants|Depressants", "cl_mix_benzodiazepines_alcohol"),
 ("methadone-buprenorphine", "Buprenorphine and other opioids", "cl_bup_other_opioids"),
 ("methadone-buprenorphine", "Buprenorphine and other opioids", "cl_bup_fentanyl_withdrawal"),
 ("methadone-buprenorphine", "After stopping", "cl_bup_after_stopping"),
 ("prescription-opioids", "Tramadol", "cl_opi_tramadol_overdose"),
 ("prescription-opioids", "Tramadol", "cl_opi_tramadol_withdrawal"),
 ("amphetamine", "Amphetamine or methylphenidate?", "cl_amph_vs_mph"),
 ("amphetamine", "Amphetamine or methylphenidate?", "cl_amph_vs_mph_psychosis"),
]
MIX = {"cl_mix_benzodiazepines_alcohol": ["benzodiazepines", "alcohol"]}
done = []
for page, group, cid in PLACE:
    if cid not in S or not S[cid].get("q"): print("  not yet published, not placed:", cid, "on", page); continue
    groups = Q.setdefault(page, [])
    if any(it[0] == cid for g in groups for it in g["items"]): continue
    g = next((g for g in groups if g.get("topic") == group), None)
    if not g: g = {"topic": group, "items": []}; groups.append(g)
    g["items"].append([cid, S[cid]["q"]]); done.append(f"{page} / {group}: {cid}")
for cid, pages in MIX.items():
    if cid in S and S[cid].get("q") and cid not in X: X[cid] = pages; done.append(f"mix-drugs: {cid} -> {pages}")
print("\n".join(done) or "nothing to place")
if not dry:
    for f, d in ((QF, Q), (XF, X)):
        f.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
