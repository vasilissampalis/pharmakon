"""papers_1114b.py [--write]: the senior author's paper list of 14 November 2026 (evening) for the to-do page
(scripts/editor/todo/pharmakon-todo.html, DATA.papers): the three still missing from the morning's list, the papers the
claim writers and first readers named as missing for this round's answers, the 29 papers paper finder 680 chose for the
next most-asked questions (and one erratum), then supplements. APA references come from the cached Crossref records
(apa_from_cache.py); nothing is typed by hand. Each paper keeps the two buttons (Copy DOI, Copy file name); a where-to-click
note only for supplements and corrections. Without --write, prints the list."""
import json, re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts" / "editor"))
import apa_from_cache as A
P = []
def no_author(doi):   # APA 7: a notice with no author starts with its title (from the cached Crossref record)
    cr = A.cache[doi.lower()]; yr = (cr.get("print") or cr.get("issued") or cr.get("online"))[0]
    return f"{cr['title']}. ({yr}). *{cr['ct']}*, *{cr['vol']}*({cr['iss']}), {cr['pg']}. https://doi.org/{cr['DOI']}"
def add(group, doi, folder, name, star=False, kind="original", note=None, k=None, suffix=""):
    ref = (A.apa(doi) if A.cache[doi.lower()].get("au") else no_author(doi)) + suffix
    P.append({"k": k or name, "group": group, "star": star, "kind": kind, "apa": ref, "folder": folder, "name": name + ".pdf", "url": "https://doi.org/" + doi, **({"note": note} if note else {})})
g = "Still missing from this morning's list"
add(g, "10.1126/science.7200260", "Heroin", "Siegel_1982_HeroinOverdoseEnvironmentalCues", True, k="Siegel_1982_HeroinOverdoseEnvironmentalCues-again")
add(g, "10.1016/j.drugalcdep.2010.11.004", "_Cross-cutting", "LopezQuintero_2011_TransitionToDependenceNESARC", True, k="LopezQuintero_2011_TransitionToDependenceNESARC-again")
add(g, "10.1136/bmj.310.6978.504a", "MDMA", "Bryden_1995_UrinaryRetentionEcstasy", True, k="Bryden_1995_UrinaryRetentionEcstasy-again")
add("Why MDMA feels so loving: one more lab study the new answer cites", "10.1007/s00213-009-1635-z", "MDMA", "Bedi_2009_MDMASociabilityNeuralResponse", True)
add("Why it's hard to pee on MDMA", "10.1155/2016/2175896", "MDMA", "Baggott_2016_MDMAWaterIntake", True)
g = "What a pill's logo or look can tell you"
add(g, "10.1111/add.13559", "MDMA", "Vrolijk_2017_OnlinePillReportsSafety", True)
add(g, "10.1111/j.1360-0443.2009.02707.x", "MDMA", "Vogels_2009_EcstasyContentNetherlands")
add(g, "10.1002/dta.323", "MDMA", "Brunt_2011_DIMSNetherlands")
add("How MDA differs from MDMA: the MDMA study it was compared with", "10.1177/0269881115626348", "MDMA", "Baggott_2016_MDMASocioemotionalFeelings")
groups = {1: "Research chemicals: NBOMes (sold as LSD) and designer benzos like etizolam", 2: "What snorting cocaine does to the nose",
          3: "Why people like Xanax and Valium", 4: "Gabapentin and pregabalin (Lyrica): misuse and risks",
          5: "Benzos with alcohol or stimulants: the risks", 6: "Suboxone (buprenorphine) with other opioids",
          7: "Tramadol: seizures, serotonin and withdrawal", 8: "Adderall or Ritalin: how they differ",
          9: "Drug tests: false positives, and how long drugs show up"}
for p in json.load(open(ROOT / "data/verification/questions-2026-11-14/papers-next.json", encoding="utf-8")):
    add(groups[p["question"]], p["doi"], p["folder"], p["file_name"], bool(p.get("star")))
    if p["doi"].lower() == "10.1016/s2215-0366(25)00062-8":
        add(groups[p["question"]], "10.1016/s2215-0366(25)00171-3", p["folder"], p["file_name"] + "_Correction", kind="correction",
            note="This is the published correction to the paper above. It has its own page: copy its DOI and save it next to the paper.")
g = "Supplements (save these after the papers above)"
for doi, folder, name, where in (
    ("10.1038/s41386-022-01297-2", "LSD", "Holze_2022_LSDVersusPsilocybin_Supplement", "On the article page, scroll to 'Supplementary information' near the end and download the supplement."),
    ("10.1038/s41386-023-01609-0", "MDMA", "Straumann_2023_MDMALSDCoadministration_Supplement", "On the article page, scroll to 'Supplementary information' near the end and download the supplement."),
    ("10.1038/s41598-021-01209-2", "_Cross-cutting", "Timmermann_2021_PsychedelicsMetaphysicalBeliefs_Supplement", "On the article page, scroll to 'Supplementary Information' near the end and download the file."),
    ("10.3389/fpsyg.2022.852248", "_Cross-cutting", "Nayak_2022_BeliefChangeConsciousness_Supplement", "On the article page, scroll to 'Supplementary material' near the end and download the file."),
    ("10.1371/journal.pone.0267498", "Cannabis", "Smith_2022_CommercialCannabisChemistry_Supplement", "On the article page, scroll to 'Supporting information' near the end and download S1 to S6; add _S1 to _S6 to the end of this name for each file."),
    ("10.1093/scan/nst161", "MDMA", "Hysek_2014_MDMAEmpathyProsocial_Supplement", "On the article page, scroll to 'Supplementary data' near the end and download the file."),
    ("10.1136/bmj.j1550", "Heroin", "Sordo_2017_MortalityOpioidSubstitution_Supplement", "On the article page, open 'Data supplement' (or 'Supplementary materials') and download appendices 1 to 3."),
    ("10.1111/add.13512", "Heroin", "Darke_2017_DeathFromOpiateWithdrawal_Supplement", "On the article page, scroll to 'Supporting Information' near the end and download Appendix S1.")):
    add(g, doi, folder, name, kind="supplement", note=where, suffix=" [Supplementary material]")
keys = [p["k"] for p in P]; assert len(keys) == len(set(keys)), "duplicate keys"
if "--write" in sys.argv:
    f = ROOT / "scripts/editor/todo/pharmakon-todo.html"
    s = f.read_text(encoding="utf-8")
    m = re.search(r"const DATA = (\{.*?\});\n", s, re.S)
    D = json.loads(m.group(1)); D["papers"] = P
    s = s[:m.start(1)] + json.dumps(D, ensure_ascii=False) + s[m.end(1):]
    f.write_text(s, encoding="utf-8")
    print("wrote", len(P), "papers into", f)
else:
    for p in P: print(f"{p['group'][:40]:<40} {'*' if p['star'] else ' '} {p['kind']:<10} {p['folder']:<22} {p['name']}")
    print(len(P), "papers")
