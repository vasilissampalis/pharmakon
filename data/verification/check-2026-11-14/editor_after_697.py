"""Editor's adjustments after blind check 697 (14 November 2026), applied to data/site/simple.json after apply_check.py:
cl_opi_treatment_mortality: How point 3 says its figures come from the 5 studies that split deaths by time (so its 32
does not read as smaller than the 36 of the 16 studies in the short answer by mistake); How point 4 says the buprenorphine
deaths came almost all from Australian studies, as the statement says (96% of the deaths), not from 'one' study."""
import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "scripts" / "editor"))
import sj
S = sj.load(); c = S["claims"]["cl_opi_treatment_mortality"]
old2 = "Deaths in the first 4 weeks off methadone ran at about 32 a year per 1,000 people, against about 14 later on."
new2 = "In the 5 studies that split deaths by time, deaths in the first 4 weeks off methadone ran at about 32 a year per 1,000 people, against about 14 later on."
old3 = "Buprenorphine looked similar, but from just three groups, mostly one Australian study."
new3 = "Buprenorphine looked similar, but from just three groups, with almost all the deaths in Australian studies."
assert c["how"][2].startswith(old2) and old3 in c["how"][3], c["how"]
c["how"][2] = c["how"][2].replace(old2, new2); c["how"][3] = c["how"][3].replace(old3, new3)
sj.save(S); print("ok")
