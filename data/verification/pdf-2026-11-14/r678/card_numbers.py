#!/usr/bin/env python3
"""Self-check for a study card read from a PDF: for every key finding and reporting issue, look for each number
(two or more digits, or with a decimal point) on the PDF pages the anchor names, in a pdftotext extraction.

Usage: card_numbers.py CARD.json PDF OFFSET
OFFSET = PDF page index minus printed page number (0 when printed page = PDF page; for 'PDF p. N' anchors use 0).
Numbers after the word "editors'" in the same field are skipped. Output lists numbers not found, for a look by eye.
"""
import json, re, subprocess, sys

card = json.load(open(sys.argv[1], encoding="utf-8"))
pdf = sys.argv[2]
offset = int(sys.argv[3])
txt = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout
pages = txt.split("\f")

NUM = re.compile(r"(?<![\w.])[−-]?\d+(?:[.,]\d+)*(?:\.\d+)?(?![\w])")


def norm(x):
    return x.replace("−", "-").replace(",", "").lstrip("-")


def page_list(spec):
    out = []
    for part in re.split(r"[;,]", spec):
        nums = [int(x) for x in re.findall(r"\d+", part)]
        if len(nums) >= 2 and ("–" in part or "-" in part):
            out += list(range(nums[0], nums[1] + 1))
        else:
            out += nums
    return out


def variants(n):
    v = {n}
    if "." in n:
        a, b = n.split(".")
        v.add(a + "." + b.rstrip("0") if b.rstrip("0") else a)
    return v


def check(text, pagespec):
    pl = page_list(pagespec)
    hay = " ".join(pages[p - 1 + offset] for p in pl if 0 <= p - 1 + offset < len(pages))
    hay_n = {norm(m.group(0)) for m in NUM.finditer(hay)}
    cut = text.find("editors'")
    body = text if cut < 0 else text[:cut]
    miss = []
    for m in NUM.finditer(body):
        n = norm(m.group(0))
        if len(n.replace(".", "")) < 2 and "." not in n:
            continue
        if not (variants(n) & hay_n):
            miss.append(n)
    return pl, miss


for kind in ("key_findings", "reporting_issues"):
    for i, k in enumerate(card.get(kind, [])):
        text = k.get("finding") or k.get("issue") or ""
        pl, miss = check(text, k["page"])
        flag = "ok " if not miss else "LOOK"
        print(f"{flag} {kind}[{i}] {k['page']} -> pages {pl}: missing {miss}")
