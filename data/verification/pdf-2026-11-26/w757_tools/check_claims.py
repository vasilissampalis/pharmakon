import json, re, sys
QUOTED = re.compile(r"“[^”]*”|\"[^\"]*\"|(?<![A-Za-z])'[^']{12,}?'(?![A-Za-z])")
unq = lambda t: QUOTED.sub(" ", t or "")
claims = json.load(open(sys.argv[1]))
refs = set()
import glob
for f in glob.glob('data/references/*.json'):
    for r in json.load(open(f)): refs.add(r['id'])
cards = set()
for f in glob.glob('data/study-cards/_incoming/*/*.json'):
    cards.add(json.load(open(f))['id'])
lv = ["very-low","low","moderate","high"]
for c in claims:
    g=c['grade']; d=g['domains']
    down=sum(d[k]['levels'] for k in ('risk_of_bias','inconsistency','indirectness','imprecision','publication_bias'))
    up=sum(d.get(k,{'levels':0})['levels'] for k in ('large_effect','dose_response','plausible_confounding'))
    exp=lv[max(0,min(3,(3 if g['starting_level']=='high' else 1)-down+up))]
    print(c['id'], 'GRADE', g['certainty'], 'expected', exp, 'OK' if exp==g['certainty'] else 'FAIL')
    for e in c['evidence']:
        if e['reference'] not in refs: print('  unknown ref', e['reference'])
        if e['study_card'] not in cards: print('  unknown card', e['study_card'])
    q=[e for e in c['evidence'] if e.get('quote')]
    print('  quotes', len(q))
    fields=[(f,c.get(f) or '') for f in ('statement','plain','magnitude','population','exposure','comparator','outcome')]
    fields+=[('reasoning',g['reasoning'])]+[(f'ev{i}',e['extracted']) for i,e in enumerate(c['evidence'])]
    for fld,raw in fields:
        t=raw.lower()
        for term in ("addict","abuser","junkie","clean urine","dirty urine","harmless","devastating"):
            if term in t: print('  WARN',fld,term)
        if re.search(r"\bcl_[a-z]+_\w+", raw): print('  WARN raw id', fld)
        if re.search(r"\b(non-)?users?\b", unq(t)): print('  WARN user', fld)
        for m in re.finditer(r"\babus\w*", unq(raw)):
            s=unq(raw); i=m.start(); print('  abuse-word', fld, '...'+s[max(0,i-60):i+40].replace('\n',' ')+'...')
    print('  statement words', len(c['statement'].split()), 'plain words', len(c['plain'].split()))
