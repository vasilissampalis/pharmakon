"""editor_after_714.py: the editor's two word changes after blind check 714 (15 November 2026). The checker noted, for the
editors, that "feel warmer" in the short answer could be read as body heat (MDMA also raises body temperature). The claim
says "higher self-ratings of feeling loving and friendly", so "warmer" becomes "more loving" in the short answer and in the
one card kept (the two cards were one finding asked both ways: the myth stays, on the MDMA page). No number or meaning changes."""
import json, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]; sys.path.insert(0, str(ROOT / "scripts/editor"))
import sj
S = sj.load(); e = S["claims"]["cl_mdma_empathy"]
a, b = "Partly: people feel warmer, but they don't read others better.", "Partly: people feel more loving, but they don't read others better."
assert a in e["short"] or b in e["short"]; e["short"] = e["short"].replace(a, b)
for x in S["tf"]["mdma"]:
    if x.get("claim") == "cl_mdma_empathy":
        x["why"] = x["why"].replace("people felt warmer on MDMA", "people felt more loving on MDMA")
sj.save(S); print(e["short"]); print([x["why"] for x in S["tf"]["mdma"] if x.get("claim") == "cl_mdma_empathy"])
