"""place_1114.py [--dry]: put the new answers of round pdf-2026-11-14 on their pages (data/site/questions.json, each in one
home page, in people's words from its plain lines), in the MDMA monograph's sections where they are MDMA answers, and in
data/site/mix-drugs.json for the mixing answers. Only answers that are published (their plain lines installed) are placed;
an answer placed already is left alone. Other pages show an answer through its plain lines' `pages`."""
import json, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
dry = "--dry" in sys.argv
QF, MF, XF = ROOT / "data/site/questions.json", ROOT / "data/monographs/mdma.json", ROOT / "data/site/mix-drugs.json"
Q = json.load(open(QF, encoding="utf-8")); M = json.load(open(MF, encoding="utf-8")); X = json.load(open(XF, encoding="utf-8"))
S = json.load(open(ROOT / "data/site/simple.json", encoding="utf-8"))["claims"]
PLACE = [  # (page, group, claim, monograph section for MDMA answers or None)
 ("psilocybin", "Beliefs and personality", "cl_xc_psychedelic_beliefs", None),
 ("psilocybin", "Beliefs and personality", "cl_psi_personality", None),
 ("lsd", "What it feels like", "cl_xc_visual_patterns", None),
 ("lsd", "What it feels like", "cl_lsd_vs_psilocybin", None),
 ("mdma", "What it feels like", "cl_mdma_empathy", 5),
 ("mdma", "What it feels like", "cl_mdma_vs_mda", 5),
 ("mdma", "Sex", "cl_mdma_sex", 5),
 ("mdma", "Mixing with alcohol and other drugs", "cl_mix_mdma_alcohol", 6),
 ("mdma", "Mixing with alcohol and other drugs", "cl_mix_mdma_lsd", 6),
 ("interactions", "Depressants|Entactogens", "cl_mix_mdma_alcohol", None),
 ("interactions", "Entactogens|Classic psychedelics", "cl_mix_mdma_lsd", None),
 ("fentanyl-and-analogues", "Fake pills", "cl_fent_fake_pills", None),
 ("heroin", "Preventing overdose deaths", "cl_opi_overdose_recognition", None),
 ("heroin", "Overdose risk", "cl_opi_conditioned_tolerance", None),
 ("heroin", "After stopping", "cl_opi_withdrawal_deaths", None),
 ("methadone-buprenorphine", "After stopping", "cl_opi_treatment_mortality", None),
 ("cannabis", "Strains", "cl_can_strain_labels", None),
 ("general", "Helping someone you love", "cl_gen_family_craft", None),
 ("general", "Drug laws and policy", "cl_gen_festival_policing", None),
 ("benzodiazepines", "After stopping", "cl_benzo_stopping_suddenly", None),
]
MIX = {"cl_mix_mdma_alcohol": ["mdma", "alcohol"], "cl_mix_mdma_lsd": ["mdma", "lsd"]}
RENAME = {("mdma", "Using several drugs"): "Mixing with alcohol and other drugs"}  # one group for all mixing with drugs
done = []
for (page, old), new in RENAME.items():
    for g in Q.get(page, []):
        if g.get("topic") == old: g["topic"] = new; done.append(f"{page}: group '{old}' renamed '{new}'")
for page, group, cid, sec in PLACE:
    if cid not in S or not S[cid].get("q"): print("  not yet published, not placed:", cid, "on", page); continue
    groups = Q.setdefault(page, [])
    if any(it[0] == cid for g in groups for it in g["items"]): continue
    g = next((g for g in groups if g.get("topic") == group), None)
    if not g: g = {"topic": group, "items": []}; groups.append(g)
    g["items"].append([cid, S[cid]["q"]]); done.append(f"{page} / {group}: {cid}")
    if sec:
        s = next(x for x in M["sections"] if x.get("number") == sec)
        if cid not in s["claims"]: s["claims"].append(cid); done.append(f"  monograph mdma section {sec}: {cid}")
for cid, pages in MIX.items():
    if cid in S and S[cid].get("q") and cid not in X: X[cid] = pages; done.append(f"mix-drugs: {cid} -> {pages}")
print("\n".join(done) or "nothing to place")
if not dry:
    for f, d in ((QF, Q), (MF, M), (XF, X)):
        f.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
