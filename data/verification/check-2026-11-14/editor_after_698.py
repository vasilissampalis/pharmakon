"""Editor's adjudication after blind check 698 (14 November 2026), run after apply_check.py 698.
cl_opi_treatment_mortality: checker 698 judged only How points 3 and 4 (its list holds null for points 1 and 2, which it
did not see), so points 1 and 2 are restored from the version before the check, and points 3 and 4 take the checker's
text, with one change by the editor to point 4: 'deaths also peaked in the first 4 weeks off' becomes 'were also higher
... (about 32 against 11 a year per 1,000) ... so it's less certain', because the statement calls the buprenorphine pattern
'similar but less certain' (two cohorts; the interval for the difference includes no difference)."""
import json, sys, subprocess, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts" / "editor"))
import sj
before = json.loads(subprocess.run(["git", "-C", str(ROOT), "show", "HEAD:data/site/simple.json"], capture_output=True, text=True, check=True).stdout)
old = before["claims"]["cl_opi_treatment_mortality"]["how"]
out = json.load(open(ROOT / "data/verification/check-2026-11-14/check_out698.json", encoding="utf-8"))
new = next(r for r in out["lines"] if r["id"] == "cl_opi_treatment_mortality")["fields"]["how"]
assert new[0] is None and new[1] is None and len(new) == 4
p4 = new[3]
o4 = "deaths also peaked in the first 4 weeks off, but in just two studies."
n4 = "deaths were also higher in the first 4 weeks off, about 32 against 11 a year per 1,000, but from just two studies, so it's less certain."
assert o4 in p4, p4
S = sj.load()
S["claims"]["cl_opi_treatment_mortality"]["how"] = [old[0], old[1], new[2], p4.replace(o4, n4)]
sj.save(S); print(json.dumps(S["claims"]["cl_opi_treatment_mortality"]["how"], ensure_ascii=False, indent=1))
