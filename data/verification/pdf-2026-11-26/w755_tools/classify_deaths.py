import sys, json, re
from collections import Counter, defaultdict
rows = json.load(open(sys.argv[1]))
deaths = [r for r in rows if r['Study'] == 'Death']
OPI = ['MTD', 'EDDP', 'MOR', '6-AM', 'COD', 'DHC', 'HCOD', 'TMD', 'TAP', 'FEN', 'NOR-FEN', 'NORFENTANYL', '4-ANPP', 'CFN',
       'BUP', 'NOR-BUP', 'BRP', 'ITZ', 'OXY', 'OXM', 'U-47700', 'U-4770', 'HEROIN', 'FENTANYL', 'ACETYLFENTANYL', 'FURANYLFENTANYL',
       'HYDROMORPHONE', 'PETHIDINE', 'METHADONE', 'MORPHINE', 'NORFEN', 'ACRYLFENTANYL', 'CYCLOPROPYLFENTANYL', 'METONITAZENE', 'ISOTONITAZENE', 'BRORPHINE']
def tokens(line):
    # first token of a co-exposure line is the substance name
    t = line.strip().split(' ')[0]
    return t
def is_opioid(name):
    n = name.upper().replace('–', '-')
    return any(n == o or n.startswith(o + ' ') for o in OPI) or 'FENTANYL' in n or n in ('NOR-OXY', 'NOROXYCODONE')
out = []
cnt = Counter(); by = defaultdict(lambda: [0, 0])
names = Counter()
for i, r in enumerate(deaths):
    subs = [tokens(l) for l in r['Co-Exposure'] if l.strip() not in ('-', '')]
    for s in subs: names[s] += 1
    opi = [s for s in subs if is_opioid(s)]
    lpm = [s for s in subs if s.upper().startswith('LPM')]
    own = r['Compound'].lower()
    nonown = [s for s in subs if own not in s.lower()]
    cat = 'opioid' if opi else ('loperamide' if lpm else ('none' if not nonown else 'other'))
    cnt[cat] += 1
    by[r['Compound']][0] += 1
    if opi: by[r['Compound']][1] += 1
    out.append((i + 1, r['page'], r['Compound'], r['Age'], r['Observations'], r['Concentration'], subs, cat))
for o in out:
    if o[-1] != 'opioid':
        print(o)
print(cnt)
print(dict(by))
print(sorted(names.items(), key=lambda x: -x[1]))
