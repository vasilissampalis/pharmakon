import sys, json, re
from collections import Counter
rows = [r for r in json.load(open(sys.argv[1])) if r['Study'] == 'Death']
def first(l): return l.strip().split(' ')[0]
groups = {
 'methadone (MTD/EDDP)': ['MTD', 'EDDP'],
 'morphine/heroin markers (MOR/6-AM)': ['MOR', '6-AM', 'MOR-3-glucuronide', 'MOR-6-glucuronide'],
 'codeine (COD)': ['COD'],
 'dihydrocodeine (DHC)': ['DHC', 'DHC-6-glucuronide'],
 'fentanyl (FEN/Nor-FEN/4-ANPP/Acetyl-FEN)': ['FEN', 'Nor-FEN', '4-ANPP', 'Acetyl-FEN'],
 'buprenorphine (BUP/Nor-BUP/NBUP)': ['BUP', 'Nor-BUP', 'NBUP'],
 'tramadol (TMD)': ['TMD'], 'tapentadol (TAP)': ['TAP'], 'hydrocodone (HCOD)': ['HCOD'],
 'brorphine (BRP)': ['BRP'], 'isotonitazene (ITZ)': ['ITZ'], 'U-47700': ['U-47700', 'U-4770'], 'oxycodone (OXY)': ['OXY'],
}
c = Counter(); anyop = 0
alls = set(sum(groups.values(), []))
for r in rows:
    subs = set(first(l) for l in r['Co-Exposure'])
    hit = False
    for g, toks in groups.items():
        if subs & set(toks):
            c[g] += 1; hit = True
    anyop += hit
print('entries with any opioid:', anyop)
for g, n in c.most_common(): print(g, n)
# EtOH among non-opioid
nonop = [r for r in rows if not (set(first(l) for l in r['Co-Exposure']) & alls)]
print('non-opioid entries', len(nonop), 'with EtOH', sum(1 for r in nonop if 'EtOH' in set(first(l) for l in r['Co-Exposure'])))
print('all entries with EtOH', sum(1 for r in rows if 'EtOH' in set(first(l) for l in r['Co-Exposure'])))
