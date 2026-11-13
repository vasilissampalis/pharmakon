#!/usr/bin/env python3
"""Compile the master PDF request list from every search-logs/*_DOI-LIST.md.

Outputs
  docs/PDF-REQUEST-LIST.md   — save order: Tier A of every substance, then B, then C
  data/evidence-maps.json    — counts per folder (papers, tierA/B/C, reports)
Uses the header-driven parser in parse_lists.py, so column order may differ between lists.
"""
import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from parse_lists import all_lists, ROOT

ORDER = ["Methamphetamine", "Alcohol", "Cannabis", "Ketamine", "Cocaine", "MDMA", "Heroin", "Fentanyl-and-analogues",
         "Benzodiazepines", "Psilocybin", "LSD", "Amphetamine", "GHB-GBL", "Nicotine", "Caffeine", "Synthetic-cathinones",
         "Methylphenidate", "DMT-Ayahuasca", "5-MeO-DMT", "Mescaline", "2C-x", "PCP", "DXM", "Nitrous-oxide",
         "Synthetic-cannabinoids", "Prescription-opioids", "Methadone-Buprenorphine", "Kratom",
         "Alkyl-nitrites-and-inhalants", "Salvia-divinorum",
         "_Overdose-and-emergency", "_Interactions", "_Harm-reduction", "_Drug-checking", "_Dependence-epidemiology", "_Harm-rankings", "_Language-and-stigma"]

def dest_and_file(folder, save_as):
    s = (save_as or "").strip().strip("`")
    if "/" in s:
        d, f = s.split("/", 1)
        return d, f
    return (folder if not folder.startswith("_") else "_Cross-cutting"), s

LANCET = ("10.1016/s0140-6736", "10.1016/s2214-109x", "10.1016/s2215-0366", "10.1016/s2468-2667", "10.1016/s1470-2045",
          "10.1016/s1473-3099", "10.1016/s2352-3018", "10.1016/s2213-8587", "10.1016/s2213-2600", "10.1016/s2352-4642",
          "10.1016/j.eclinm", "10.1016/j.lanepe", "10.1016/j.lana", "10.1016/j.lanwpc")

def blocked_for_ai(doi, blocked):
    """Free papers the AI cannot open: listed in data/access/blocked.txt, or hosted on ScienceDirect, which refuses the
    app's browser (CPE00001, confirmed 2026-10-15). Lancet-family journals are hosted elsewhere and open normally."""
    d = doi.lower()
    return d in blocked or (d.startswith("10.1016/") and not d.startswith(LANCET))

def load_access():
    """PMC availability (data/access/pmc-index.txt: doi>PMCID>OA) and PDFs already received (data/access/received.txt: one DOI per line)."""
    pmc, received = {}, set()
    f = ROOT / "data" / "access" / "pmc-index.txt"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            parts = line.strip().split(">")
            if len(parts) >= 2 and parts[1].startswith("PMC"):
                pmc[parts[0].lower()] = (parts[1], parts[2] if len(parts) > 2 else "")
    h = ROOT / "data" / "access" / "publisher-oa.txt"
    if h.exists():
        for line in h.read_text(encoding="utf-8").splitlines():
            if line.startswith("#") or ">" not in line: continue
            d, st = line.strip().split(">", 1)
            pmc.setdefault(d.lower(), ("publisher", st))
    g = ROOT / "data" / "access" / "received.txt"
    if g.exists():
        received = {l.strip().lower() for l in g.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")}
    b = ROOT / "data" / "access" / "blocked.txt"
    blocked = {}
    if b.exists():
        blocked = {l.split(">")[0].strip().lower(): (l.split(">", 1)[1] if ">" in l else "") for l in b.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")}
    return pmc, received, blocked

def main():
    lists = all_lists()
    pmc, received, blocked = load_access()
    chk = ROOT / "data" / "access" / "access-checked.tsv"
    checked = {l.split("\t")[0].strip().lower() for l in chk.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")} if chk.exists() else set()
    n_free = 0
    maps = {k: {"papers": sum(len(t[x]) for x in "ABC"), "tierA": len(t["A"]), "tierB": len(t["B"]), "tierC": len(t["C"]), "reports": len(t["reports"])} for k, t in lists.items()}
    (ROOT / "data" / "evidence-maps.json").write_text(json.dumps(maps, indent=1), encoding="utf-8")
    present = [o for o in ORDER if o in lists] + sorted(k for k in lists if k not in ORDER)
    seen = set(); total = 0; dupes = 0; n_user = 0; n_self = 0; n_recv = 0
    out = ["# PDF request list — all substances", ""]
    body = []
    selfread = ["# Papers the AI reads itself (free full text)", "", "These are free to read in PubMed Central or at the publisher, so they are not on your list. They are read through the app's browser and the study cards are written from the full text. If a publisher page turns out not to be free, the paper moves back to your list.", "", "| # | Paper | Folder | Where | Access | Link |", "|---|---|---|---|---|---|"]
    for tier, label in [("A", "Tier A — first, for every substance"), ("B", "Tier B — section backbone"), ("C", "Tier C — epidemiology, routes, harm reduction, policy")]:
        body += [f"## {label}", ""]
        for folder in present:
            rows = lists[folder][tier]
            if not rows: continue
            block = []
            for r in rows:
                key = r["doi"].lower()
                dest, fname = dest_and_file(folder, r["save_as"])
                if key in seen:
                    dupes += 1
                    continue
                seen.add(key); total += 1
                if key in received:
                    n_recv += 1
                    continue
                if key in pmc and (key in blocked or (pmc[key][0] == "publisher" and blocked_for_ai(key, blocked))):
                    n_user += 1
                    is_free = pmc[key][0] == "publisher" and "embargo" not in blocked.get(key, "") and "paywall" not in blocked.get(key, "")
                    n_free += 1 if is_free else 0
                    block.append(f"| {n_user} | {r['paper']} | {dest} | {fname} | https://doi.org/{r['doi']}" + (" · **free, open access**" if is_free else "") + " |")
                    continue
                if key in pmc:
                    n_self += 1
                    pid, oa = pmc[key]
                    if pid == "publisher":
                        selfread.append(f"| {n_self} | {r['paper']} | {dest} | publisher ({oa}) | free at the publisher | https://doi.org/{r['doi']} |")
                    else:
                        selfread.append(f"| {n_self} | {r['paper']} | {dest} | {pid} | {'yes' if oa == 'Y' else 'free to read'} | https://pmc.ncbi.nlm.nih.gov/articles/{pid}/ |")
                    continue
                n_user += 1
                block.append(f"| {n_user} | {r['paper']} | {dest} | {fname} | https://doi.org/{r['doi']} |")
            if block:
                body += [f"### {folder} ({len(block)})", "", "| # | Paper | Save into folder | Filename | Link |", "|---|---|---|---|---|"] + block + [""]
    n_unchecked = sum(1 for d in seen if d not in checked and d not in received and d not in pmc and not blocked_for_ai(d, blocked))
    out += [f"**{n_user} papers for you to save.** The evidence maps list {total} unique papers ({len(present)} maps; {dupes} duplicates collapsed). Of these, {n_recv} you have already saved, and {n_self} are free in PubMed Central or at the publisher, so I read those myself (see `docs/READ-MYSELF-LIST.md`). " + (f"Of the papers below, {n_unchecked} have not yet been checked for a free full text (that check is running; every one found free moves to my own reading list, so the number for you will fall); the rest are paywalled or on ScienceDirect, which refuses the app's browser" if n_unchecked else "What remains below is paywalled or on ScienceDirect, which refuses the app's browser") + f"; {n_free} of them are marked **free, open access**: free to download, but I cannot open them. Only items 1–10 are needed now.", "",
            "**How to work through this:** in order, ten at a time. For each paper: open the link, save the PDF into `DrugEncyclopedia/PDFs/<folder>/` with the exact filename shown (if your save dialog adds `.pdf` by itself, type the name without `.pdf`). Tell me when a batch is done and I start reading. Tier A of every substance comes first because those papers turn draft claims into verified ones.", "",
            "Per-substance detail (journal, year, tier, search log) is in `PDFs/<Substance>/_DOI-LIST.md`.", ""] + body
    (ROOT / "docs" / "PDF-REQUEST-LIST.md").write_text("\n".join(out), encoding="utf-8")
    (ROOT / "docs" / "READ-MYSELF-LIST.md").write_text("\n".join(selfread) + "\n", encoding="utf-8")
    print(json.dumps(maps, indent=1)); print("unique papers:", total, "| duplicates collapsed:", dupes, "| for the user:", n_user, f"(of which free but blocked for the AI: {n_free})", "| self-read:", n_self, "| received:", n_recv)

if __name__ == "__main__":
    main()
