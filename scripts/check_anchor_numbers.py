#!/usr/bin/env python3
"""Mechanical check of PDF-read evidence anchors (METHODS §5.5, first-reader self-check).

For every anchor read from a PDF, take each number written in `extracted` and look for it on the printed page(s) the
anchor names, in a text extraction of the PDF. Numbers that are not found are listed for a human or second-reader look.
It cannot prove an anchor right; it catches transcription slips and wrong page numbers.

Usage: check_anchor_numbers.py TEXT_DIR [claims.json ...]
TEXT_DIR holds one pdftotext extraction per PDF, named like the PDF (…/Name.pdf → TEXT_DIR/Name.txt), pages separated
by form feeds. Editors' calculations (the anchor says "editors'") are skipped for the numbers that follow that word.
"""
import json, re, sys, glob, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
text_dir = pathlib.Path(sys.argv[1])
claim_files = sys.argv[2:] or sorted(glob.glob(str(ROOT / "data" / "claims" / "*.json")))
refs = {}
for f in glob.glob(str(ROOT / "data" / "references" / "*.json")):
    for r in json.load(open(f, encoding="utf-8")):
        refs[r["id"]] = r

BASIS_FILE = ROOT / "data" / "access" / "pdf-page-basis.json"
BASIS = {k: v for k, v in (json.load(open(BASIS_FILE, encoding="utf-8")).items() if BASIS_FILE.exists() else []) if not k.startswith("_")}

def first_page(r):
    pg = str(r.get("page", ""))
    m = re.match(r"(\d+)", pg)
    return int(m.group(1)) if m else 1

def pages_for(spec):
    out = []
    for part in re.split(r"[,;]", spec):
        nums = [int(x) for x in re.findall(r"\d+", part)]
        if len(nums) >= 2 and ("–" in part or "-" in part) and nums[1] >= nums[0]:
            out += list(range(nums[0], nums[1] + 1))
        else:
            out += nums
    return out

NUM = re.compile(r"(?<![\w.])[−-]?\d+(?:[.,]\d+)?(?![\w])")
def norm(x): return x.replace("−", "-").replace(",", "").replace("\u00b7", ".")  # the Lancet prints decimals with a middle dot (1·41)

def page_text(pages, pno, first):
    i = pno - first
    if 0 <= i < len(pages):
        return pages[i]
    return ""

total = missing = checked = 0
for cf in claim_files:
    for c in json.load(open(cf, encoding="utf-8")):
        for e in c["evidence"]:
            # a PDF-read anchor says so at the start of source_read ("PDF", or "PDF PDFs/<folder>/<file>.pdf" naming the file read,
            # e.g. a corrigendum read with its paper); before 27 October only the bare "PDF" was recognized, so path-style anchors were skipped
            sr = str(e.get("source_read") or "")
            if not sr.startswith("PDF") or e["anchor_status"] == "unchecked":
                continue
            r = refs.get(e["reference"]); pdf = (r or {}).get("verification", {}).get("pdf_path", "")
            named = re.search(r"(PDFs/\S+?\.pdf(?:\.pdf)?)", sr)
            if named: pdf = named.group(1)
            name = pathlib.Path(pdf).name
            while name.lower().endswith(".pdf"):
                name = name[:-4]
            tf = text_dir / (name + ".txt")
            if not tf.exists():
                print(f"NO TEXT  {c['id']} {e['reference']} ({tf.name})"); continue
            pages = tf.read_text(encoding="utf-8", errors="replace").split("\f")
            first = BASIS[e["reference"]]["first_page"] if e["reference"] in BASIS else first_page(r)
            # an author manuscript has no journal pages: "AM p. N" is the PDF page (METHODS §6.2), and so are "PDF page N" and "PDF p. N"
            if re.match(r"\s*(AM\b|PDF page|PDF pp?\.)", str(e["page"])): first = 1
            # another file than the reference's own PDF (a corrigendum read with its paper): its page numbering is unknown here,
            # so its numbers are looked for anywhere in that file
            own = (r or {}).get("verification", {}).get("pdf_path", "")
            other = bool(named and own and named.group(1) != own)  # a reference without pdf_path: the named file is its own PDF
            want = pages_for(re.sub(r"\s+of the online-first PDF", "", e["page"]))
            # an article number (e-locator such as "111018") is not a first page: the PDF's printed pages then run from 1
            if not re.search(r"[–-]", str(r.get("page", ""))) and want and all(p < first for p in want):
                first = 1
            hay = " ".join(pages) if other else " ".join(page_text(pages, p, first) for p in want)
            hay_n = norm(re.sub(r"\s+", " ", hay)).replace("¼", "=")
            ext = e["extracted"]
            cut = ext.lower().find("editors'")
            body = ext if cut < 0 else ext[:cut]
            checked += 1
            bad = []
            page_nums = []
            for t in NUM.findall(hay_n):
                try: page_nums.append(abs(float(norm(t))))
                except ValueError: pass
            for t in re.findall(r"(?<![\d])\.\d+", hay_n):  # leading-dot decimals such as .47
                page_nums.append(float(t))
            for m in NUM.finditer(body):
                tok = norm(m.group(0)).lstrip("-")
                if len(tok.replace(".", "")) < 2 and "." not in tok:
                    continue  # single digits are too common to test
                total += 1
                if tok in hay_n:
                    continue
                x = float(tok); dec = len(tok.split(".")[1]) if "." in tok else 0
                tol = 0.5 * 10 ** (-dec) + 1e-9
                if any(abs(x - y) <= tol for y in page_nums):
                    continue  # printed with more decimals, rounded here
                bad.append(m.group(0)); missing += 1
            if bad:
                print(f"CHECK    {c['id']} · {e['reference']} {e['page']} · not found on that page: {', '.join(bad)}")
print(f"\n{checked} PDF anchors, {total} numbers tested, {missing} not found on the stated page")
