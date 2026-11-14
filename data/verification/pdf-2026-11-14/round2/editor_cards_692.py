"""Editor's fixes to four first-pass cards after round-2 reader 692 (14 November 2026). Each change is logged in the
card's verification.disagreements with the editor's resolution. The Hazekamp and Lader points were checked by the editor
in the PDFs (PDF p. 4 of Hazekamp et al., 2012; the reference list of Lader, 2011, which ends at ref. 277)."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[4]
I = ROOT / "data/study-cards/_incoming"
WHO = "AI co-editor, on the note of AI reader 692 (round-2 check)"
def fix(path, getset, old, new, why):
    p = I / path; c = json.load(open(p, encoding="utf-8"))
    obj, key = getset(c); assert old in obj[key], (path, key, old)
    first = obj[key]; obj[key] = obj[key].replace(old, new)
    c.setdefault("verification", {}).setdefault("disagreements", []).append(
        {"field": key, "first_pass": first, "reviewer": obj[key], "resolution": f"{WHO}: {why}"})
    json.dump(c, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1); open(p, "a").write("\n")
fix("cannabis/sc_smith_2022.json", lambda c: (c["interpretation_gap"], "results_show"),
    "for about two-thirds of the 41 most common names",
    "for about two-thirds of the 41 names that at least five producers each sold with at least five samples",
    "the 41 names are those meeting the five-producer, five-sample threshold (p. 27), not necessarily the most common.")
fix("cannabis/sc_hazekamp_2012.json", lambda c: (c["interpretation_gap"], "claimed"),
    "that α-pinene might counter memory effects in Amnesia",
    "that Amnesia's lower α-pinene, described as an anticholinesterase that may reduce THC's short-term memory deficits, would be noteworthy if Amnesia does have stronger memory effects",
    "the paper's speculation runs from Amnesia's lower α-pinene to possibly stronger memory effects (PDF p. 4), not the reverse; read by the editor.")
for key in ("design_detail",):
    fix("benzodiazepines/sc_lader_2011.json", lambda c: (c, key), "274 numbered references", "277 numbered references",
        "the reference list ends at ref. 277 (checked by the editor); 23 with the author, as the card says.")
def rob_note(c):
    d = next(x for x in c["risk_of_bias"]["domains"] if "274" in x.get("note", "")); return d, "note"
fix("benzodiazepines/sc_lader_2011.json", rob_note, "23 of 274 references", "23 of 277 references",
    "the reference list ends at ref. 277 (checked by the editor).")
fix("cross-cutting/sc_hughes_2017.json", lambda c: (c, "design"), "rct", "survey",
    "the only randomized element is which written scenario people read, and the outcome is a stated intention; a survey with an embedded vignette experiment (design_detail), not a trial of policing. RoB 2 still applies to the randomized vignette comparison.")
fix("cross-cutting/sc_hughes_2017.json", lambda c: (c["interpretation_gap"], "claimed"),
    "describing hypothetical intentions as effects.",
    "describing hypothetical intentions as effects; it also says high-visibility policing most reduced overall offending, ‘including supply’ (p. 91), although it differs from drug detection dogs by 0.6 points without a test and the strategies did not differ on supply at the paper's own threshold (giving and selling p = 0.029, buying p = 0.711).",
    "the abstract's claim about high-visibility policing and supply, which the results do not support at the stated threshold.")
print("done")
