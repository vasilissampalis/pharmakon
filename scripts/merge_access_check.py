#!/usr/bin/env python3
"""Merge a free-full-text check (OpenAlex through WebFetch, one JSON line per DOI) into data/access/.

Usage: merge_access_check.py RESULTS.jsonl [--date YYYY-MM-DD]

- A DOI with a PubMed Central id goes to data/access/pmc-index.txt as doi>PMCID>? ('?': whether the PMC copy carries an
  open licence is not known from OpenAlex; every PMC article is free to read).
- Otherwise a DOI whose open-access status is gold, hybrid, bronze or diamond goes to data/access/publisher-oa.txt as
  doi>status (free to read at the publisher; read through the app's browser; moves back to the PDF list if not).
- Green-only, closed and not-found DOIs stay on the senior editor's PDF list.
- Every checked DOI is recorded in data/access/access-checked.tsv (doi, date, source, found, pmcid, oa_status,
  is_retracted), so later checks skip it; a retraction flag is listed for a Crossref check (it is a screen, not proof).
Existing lines are never rewritten; a DOI already present in a file is left as it is.
"""
import json, sys, pathlib, re, datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
ACC = ROOT / "data" / "access"
FREE = {"gold", "hybrid", "bronze", "diamond"}

def existing(path, sep=">"):
    if not path.exists(): return set()
    return {l.split(sep)[0].strip().lower() for l in path.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")}

def main():
    if len(sys.argv) < 2: sys.exit(__doc__)
    src = pathlib.Path(sys.argv[1])
    date = sys.argv[sys.argv.index("--date") + 1] if "--date" in sys.argv else datetime.date.today().isoformat()
    rows, seen = [], set()
    for line in src.read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        r = json.loads(line)
        d = r["doi"].strip().lower()
        if d in seen: continue  # first answer wins; later duplicates ignored
        seen.add(d); rows.append(r)
    pmc_f, po_f, chk_f = ACC / "pmc-index.txt", ACC / "publisher-oa.txt", ACC / "access-checked.tsv"
    have_pmc, have_po, have_chk = existing(pmc_f), existing(po_f), existing(chk_f, "\t")
    add_pmc, add_po, add_chk, retracted, bad = [], [], [], [], []
    for r in rows:
        d = r["doi"].strip().lower()
        pmcid = r.get("pmcid")
        if pmcid and not re.fullmatch(r"PMC\d{4,9}", pmcid):
            bad.append((d, pmcid)); pmcid = None
        if not pmcid:
            # OpenAlex often lacks ids.pmcid while its oa_url points to the PMC (or Europe PMC) article page
            m = re.search(r"(?:ncbi\.nlm\.nih\.gov/pmc/articles/|pmc\.ncbi\.nlm\.nih\.gov/articles/|europepmc\.org/articles/)(?:PMC)?(\d{4,9})", r.get("oa_url") or "", re.I)
            if m: pmcid = "PMC" + m.group(1)
        st = (r.get("oa_status") or "").lower() or None
        if pmcid and d not in have_pmc and d not in have_po:
            add_pmc.append(f"{d}>{pmcid}>?")
        elif not pmcid and st in FREE and d not in have_po and d not in have_pmc:
            add_po.append(f"{d}>{st}")
        if r.get("is_retracted"):
            retracted.append((d, r.get("retraction_recheck")))
        if d not in have_chk:
            add_chk.append("\t".join([d, date, "openalex via WebFetch", str(bool(r.get("found"))).lower(), pmcid or "",
                                      st or "", str(r.get("is_retracted")).lower() if r.get("is_retracted") is not None else ""]))
    if add_pmc:
        with open(pmc_f, "a", encoding="utf-8") as f: f.write("\n".join(add_pmc) + "\n")
    if add_po:
        with open(po_f, "a", encoding="utf-8") as f:
            f.write(f"# Added {date} from the OpenAlex check of DOIs added to the evidence maps after 15 October\n" + "\n".join(add_po) + "\n")
    if add_chk:
        new = not chk_f.exists()
        with open(chk_f, "a", encoding="utf-8") as f:
            if new: f.write("# doi\tdate\tsource\tfound\tpmcid\toa_status\tis_retracted\n")
            f.write("\n".join(add_chk) + "\n")
    print(f"rows {len(rows)} · to PMC index {len(add_pmc)} · to publisher-OA {len(add_po)} · recorded as checked {len(add_chk)}")
    if bad: print("unparsed PMC ids (not used):", bad)
    if retracted:
        print("flagged as retracted by OpenAlex (check each against Crossref before acting):")
        for d, rc in retracted: print("  ", d, "| recheck:", rc)

if __name__ == "__main__":
    main()
