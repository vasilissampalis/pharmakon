"""papers_1115.py [--write]: the senior author's paper list of 15 November 2026 for the to-do page
(scripts/editor/todo/pharmakon-todo.html, DATA.papers). Two new groups go first, both asked for by him on 15 November:
the sources for "Seven questions to ask about any drug story" ("i think this should be cited ... and be objective
scientific questions about how to read a paper on drugs"), and Carl Hart's papers on addiction and the brain with two
classics on recovery ("it would be nice to add carl hart facts about drugs addiction wellbeing and policy"). The list of
14 November follows unchanged (same keys, so the papers he has ticked stay ticked). APA references come from the cached
Crossref records and documented overrides (apa_from_cache.py); nothing is typed by hand."""
import json, re, sys, pathlib, importlib.util
ROOT = pathlib.Path(__file__).resolve().parents[3]
argv = sys.argv; sys.argv = [argv[0]]
spec = importlib.util.spec_from_file_location("old", ROOT / "scripts/editor/todo/papers_1114b.py"); old = importlib.util.module_from_spec(spec); spec.loader.exec_module(old)
sys.argv = argv; A = old.A
def ref(doi):
    r = A.apa(doi)
    return re.sub(r"^([^()]*[^.\s]) \((\d{4})\)", r"\1. (\2)", r, count=1)   # a group author takes a full stop before the year (APA 7)
NEW = []
def add(group, doi, name, star=True):
    NEW.append({"k": name, "group": group, "star": star, "kind": "original", "apa": ref(doi), "folder": "_Cross-cutting", "name": name + ".pdf", "url": "https://doi.org/" + doi})
g = "How to read a drug study: sources for our 'Seven questions'"
add(g, "10.1001/archpsyc.1984.01790230064010", "Cohen_1984_CliniciansIllusion")
add(g, "10.1177/003591576505800503", "Hill_1965_AssociationOrCausation")
add(g, "10.1080/00031305.2016.1154108", "Wasserstein_2016_ASAStatementPValues")
add(g, "10.1111/j.1539-6053.2008.00033.x", "Gigerenzer_2007_MakingSenseOfHealthStatistics")
add(g, "10.1126/science.aac4716", "OpenScienceCollaboration_2015_ReproducibilityPsychology")
add(g, "10.1371/journal.pmed.0020124", "Ioannidis_2005_WhyMostFindingsAreFalse", star=False)
add(g, "10.1136/bmj.g7015", "Sumner_2014_ExaggerationPressReleases")
add(g, "10.1001/jama.2010.651", "Boutron_2010_SpinNonsignificantTrials", star=False)
g = "Carl Hart on addiction and the brain, and two classics on recovery"
add(g, "10.1038/s41562-017-0055", "Hart_2017_AddictionBrainDiseaseSocialInjustice")
add(g, "10.1016/j.neuron.2020.06.019", "Hart_2020_ExaggeratingHarmfulDrugEffects")
add(g, "10.1146/annurev-clinpsy-032511-143041", "Heyman_2013_QuittingDrugs")
add(g, "10.1111/j.1360-0443.1993.tb02123.x", "Robins_1993_VietnamVeteransHeroinRecovery")
P = NEW + old.P
keys = [p["k"] for p in P]; assert len(keys) == len(set(keys)), "duplicate keys"
if "--write" in sys.argv:
    f = ROOT / "scripts/editor/todo/pharmakon-todo.html"; s = f.read_text(encoding="utf-8")
    m = re.search(r"const DATA = (\{.*?\});\n", s, re.S); D = json.loads(m.group(1)); D["papers"] = P
    f.write_text(s[:m.start(1)] + json.dumps(D, ensure_ascii=False) + s[m.end(1):], encoding="utf-8"); print("wrote", len(P), "papers into", f)
else:
    for p in NEW: print(p["apa"], "->", p["folder"] + "/" + p["name"])
