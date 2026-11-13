#!/usr/bin/env python3
"""Compare the blind second reading of legal rows (scratchpad/legal2nd/out/) with data/legal/*.json.
Usage: compare.py  -> prints a table and writes legal2nd/compare.json
"""
import json, glob, re, pathlib, collections

ROOT = pathlib.Path('/home/claude/drug-encyclopedia')
S = pathlib.Path('/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/legal2nd')
TL = {'Α': 'Α', 'A': 'Α', 'Β': 'Β', 'B': 'Β', 'Γ': 'Γ', 'C': 'Γ', 'G': 'Γ', 'Δ': 'Δ', 'D': 'Δ'}
ROM = {'I': 1, 'II': 2, 'III': 3, 'IV': 4}


def gr_places(s):
    """All (table, item) pairs in a string such as 'Table Α΄, item 38' or 'Table Γ΄ (Table C), item 52; ... item 110'."""
    out = []
    last_table = None
    for m in re.finditer(r"(?:Table|Πίνακας|Πίνακα)\s*([ΑΒΓΔABCDG])[΄'’`]?(?:\s*\(Table [A-D]\))?|item\s*(\d+)|αρ(?:ιθμ[οό]ς)?\.?\s*(\d+)", s):
        if m.group(1):
            last_table = TL[m.group(1)]
        elif last_table:
            out.append((last_table, int(m.group(2) or m.group(3))))
    return out


def un_sched(s):
    """(convention, {schedules}) from 'Schedule II of the Convention on Psychotropic Substances, 1971' or 'Schedules I and IV ... 1961'."""
    conv = '1971' if ('1971' in s or 'Psychotropic' in s) else ('1961' if ('1961' in s or 'Single Convention' in s or 'Narcotic' in s) else None)
    m = re.search(r"Schedules?\s+((?:I{1,3}V?|IV)(?:\s*(?:,|and|&)\s*(?:I{1,3}V?|IV))*)", s)
    sch = set(re.findall(r"IV|I{1,3}", m.group(1))) if m else set()
    return conv, sch


def first_reading():
    rows = {}
    for f in sorted(glob.glob(str(ROOT / 'data/legal/*.json'))):
        slug = pathlib.Path(f).stem
        for i, e in enumerate(json.load(open(f, encoding='utf-8'))['entries']):
            rows[f'{slug}#{i}'] = e
    return rows


def main():
    rows = first_reading()
    second = {}
    for f in glob.glob(str(S / 'out/*.json')):
        key = pathlib.Path(f).stem
        if key.endswith('_meta'):
            continue
        try:
            second[key] = {x['id']: x for x in json.load(open(f, encoding='utf-8'))}
        except Exception as ex:
            print('cannot read', f, ex)
    res = []
    for rid, e in rows.items():
        j = e['jurisdiction']
        if j == 'Greece':
            exp = gr_places(e['status'])
            not_conf = bool(re.search(r'Not confirmed|not found|none found', e['status']))
            got = second.get('GR_MOH_2026', {}).get(rid)
            if not got:
                res.append((rid, 'Greece', 'not read by reader 2', e['status'][:80], '')); continue
            gp = gr_places((got.get('where') or '') + ' ; ' + ' ; '.join(got.get('other_places') or []))
            found = (got.get('found') or '').lower().startswith('yes')
            if not_conf:
                # first reading: not in the June 2026 text received (Table Δ΄ unreadable) — except the Δ΄ item read in the 2024 copy
                verdict = 'agree (not in text)' if not found else ('agree' if exp and gp and gp[0] in exp else 'DIFFER: reader 2 found it')
            else:
                if not found:
                    verdict = 'DIFFER: reader 2 did not find it'
                elif exp and gp and exp[0] == gp[0]:
                    verdict = 'agree' if set(exp) <= set(gp) or len(exp) == 1 else 'agree (primary); check other places'
                else:
                    verdict = 'DIFFER: place'
            res.append((rid, 'Greece', verdict, e['status'][:90], f"{got.get('found')} | {got.get('where')} | {got.get('printed')} | {got.get('other_places')}"))
        elif j.startswith('International'):
            conv, sch = un_sched(e['status'])
            notfound = e['status'].startswith(('Not found', 'Not under')) or ': Not found' in e['status']
            g71 = second.get('UN_1971_2024', {}).get(rid) or {}
            g61 = second.get('INCB_YL64', {}).get(rid) or {}
            gnew = second.get('INCB_NEW2025', {}).get(rid) or {}
            f71 = (g71.get('found') or '').lower().startswith('yes')
            f61 = (g61.get('found') or '').lower().startswith('yes')
            fnew = (gnew.get('found') or '').lower().startswith('yes')
            if not (g71 or g61):
                res.append((rid, 'UN', 'not read by reader 2', e['status'][:80], '')); continue
            if notfound:
                verdict = 'agree (not found)' if not (f71 or f61 or fnew) else 'DIFFER: reader 2 found it'
            else:
                g = g71 if conv == '1971' else g61
                fg = f71 if conv == '1971' else f61
                gsch = set(re.findall(r"IV|I{1,3}", g.get('where') or '')) if g else set()
                if not fg:
                    verdict = f'DIFFER: not found in the {conv} list by reader 2'
                elif gsch == sch:
                    verdict = 'agree'
                else:
                    verdict = f'DIFFER: schedule {sorted(gsch)} vs {sorted(sch)}'
            res.append((rid, 'UN', verdict, e['status'][:90], f"71: {g71.get('found')} {g71.get('where')} | 61: {g61.get('found')} {g61.get('where')} | new2025: {gnew.get('found')} {gnew.get('where')}"))
    c = collections.Counter((r[1], r[2].split(':')[0]) for r in res)
    for k, v in sorted(c.items()):
        print(v, k)
    for r in res:
        if not r[2].startswith('agree'):
            print(' ', r[0], '|', r[2], '|', r[3], '||', r[4][:220])
    json.dump([dict(zip(('id', 'jurisdiction', 'verdict', 'first', 'second'), r)) for r in res], open(S / 'compare.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
