#!/usr/bin/env python3
"""Staged EU rows (EU-wide control through the Annex of Framework Decision 2004/757/JHA), first reading of 2026-10-16.
Not applied until the second reading agrees. Usage: staged_rows.py [--apply ACT_3MMC]  (e.g. --apply "(EU) 2022/1326")
"""
import json, sys, pathlib

ROOT = pathlib.Path('/home/claude/drug-encyclopedia')
UK_ANNEX = 'https://www.legislation.gov.uk/eudr/2017/2103/annex'
COM_REPORT = 'https://data.consilium.europa.eu/doc/document/ST-9820-2022-INIT/en/pdf'
EUDA_2026 = 'https://www.euda.europa.eu/news/2026/eu-takes-action-control-three-harmful-new-drugs_en'
EURLEX_2025 = 'https://eur-lex.europa.eu/eli/dir_del/2025/2062/oj'
CB = 'AI reader 2 (blind second reading of the same five sources through WebFetch; compared fact by fact by the editor; agreed)'
FD = 'Council Framework Decision 2004/757/JHA, Annex (list of new psychoactive substances included in the definition of \'drug\')'


def rows(act_3mmc):
    common_note = ("Read through WebFetch on 2026-10-16 (first reading by the editor; blind second reading by AI reader 2, which agreed). The EUR-Lex "
                   "consolidated text of the Framework Decision could not be read (EUR-Lex closes its text pages to automated "
                   "readers), so the Annex was read in three parts: as inserted by Directive (EU) 2017/2103 (legislation.gov.uk "
                   "copy); the Commission's report of 1 June 2022 on the delegated directives adopted from 2019 to 2022 (COM(2022) "
                   "251); and the EUDA's news item of 30 January 2026 on Delegated Directive (EU) 2025/2062. No other act amending "
                   "the Annex between June 2022 and October 2025 was found. The Framework Decision defines 'drug' as any substance "
                   "covered by the 1961 or 1971 Conventions or listed in its Annex; national classification is in the Greece row.")
    return {
        '2c-x': {
            'jurisdiction': 'European Union',
            'status': "2C-I and 2C-T-7: in the definition of 'drug' in EU law (Annex of the Framework Decision, point 3, with 2C-T-2 and TMA-2). 2C-E and 2C-C: not in the Annex as read. 2C-B: covered through the 1971 Convention (see the UN row).",
            'instrument': FD + ', point 3, as inserted by Directive (EU) 2017/2103',
            'source_url': UK_ANNEX,
            'source_title': 'Directive (EU) 2017/2103, Annex: list of substances (legislation.gov.uk copy)',
            'source_date': 'Annex as inserted in 2017; later additions read in COM(2022) 251 (2019–2022) and the EUDA news item of 30 January 2026',
            'checked_on': '2026-10-16',
            'note': "Point 3 of the Annex names 2,5-dimethoxy-4-iodophenethylamine (2C-I), 2,5-dimethoxy-4-ethylthiophenethylamine (2C-T-2), 2,5-dimethoxy-4-(n)-propylthiophenethylamine (2C-T-7) and 2,4,5-trimethoxyamphetamine (TMA-2). " + common_note,
            'checked_by': CB,
            'verification': 'ai-checked'},
        'synthetic-cathinones': {
            'jurisdiction': 'European Union',
            'status': f"In the definition of 'drug' in EU law (Annex of the Framework Decision): mephedrone (4-MMC), MDPV and alpha-PVP (Annex as inserted by Directive (EU) 2017/2103); 3-MMC and 3-CMC (Commission Delegated Directive {act_3mmc}); 2-MMC, 4-BMC and N-ethylnorpentedrone (NEP) (Commission Delegated Directive (EU) 2025/2062, in force from 12 January 2026; Member States to bring national control into force by 12 July 2026).",
            'instrument': FD + ', as inserted by Directive (EU) 2017/2103 and amended by Commission Delegated Directives ' + act_3mmc + ' and (EU) 2025/2062',
            'source_url': EUDA_2026,
            'source_title': "EUDA news, 'EU takes action to control three harmful new drugs' (30 January 2026); Annex of Directive (EU) 2017/2103 (legislation.gov.uk); Commission report COM(2022) 251",
            'source_date': 'Delegated Directive (EU) 2025/2062 of 14 October 2025 (EUR-Lex), in force 12 January 2026',
            'checked_on': '2026-10-16',
            'note': "Cathinone and cathine are covered through the 1971 Convention (see the UN row); 4-CMC is not in the Annex as read but is in Schedule II of the 1971 Convention. 3-MMC and 3-CMC are points 20 and 21 of the Annex (EUDA Drugs Library entry for (EU) 2022/1326; Council cover note 7430/22 of 21 March 2022, which sent the act as C(2022) 1552). The Commission's report of 1 June 2022 prints the act as '(EU) 2022/1552', its document number; the Official Journal number is (EU) 2022/1326 (EUDA Drugs Library; Publications Office). " + common_note,
            'checked_by': CB,
            'verification': 'ai-checked'},
        'synthetic-cannabinoids': {
            'jurisdiction': 'European Union',
            'status': "MDMB-4en-PINACA: in the definition of 'drug' in EU law (Annex of the Framework Decision, added by Commission Delegated Directive (EU) 2021/802, with 4F-MDMB-BICA). The other members named on this page are covered through the 1971 Convention (see the UN rows).",
            'instrument': FD + ', as amended by Commission Delegated Directive (EU) 2021/802',
            'source_url': COM_REPORT,
            'source_title': 'Commission report COM(2022) 251 on the exercise of the power to adopt delegated acts under Framework Decision 2004/757/JHA (Council document 9820/22)',
            'source_date': 'Report of 1 June 2022',
            'checked_on': '2026-10-16',
            'note': "The same report lists ADB-CHMINACA and CUMYL-4CN-BINACA (Delegated Directive (EU) 2019/369), which are not members of this page. " + common_note,
            'checked_by': CB,
            'verification': 'ai-checked'},
        'fentanyl-and-analogues': {
            'jurisdiction': 'European Union',
            'status': "Furanylfentanyl: in the definition of 'drug' in EU law (Annex of the Framework Decision, added by Commission Delegated Directive (EU) 2019/369, with cyclopropylfentanyl and methoxyacetylfentanyl); acryloylfentanyl is in the Annex as inserted by Directive (EU) 2017/2103. The other members named on this page are covered through the 1961 Convention (see the UN rows).",
            'instrument': FD + ', as amended by Commission Delegated Directive (EU) 2019/369',
            'source_url': COM_REPORT,
            'source_title': 'Commission report COM(2022) 251 on the exercise of the power to adopt delegated acts under Framework Decision 2004/757/JHA (Council document 9820/22)',
            'source_date': 'Report of 1 June 2022',
            'checked_on': '2026-10-16',
            'note': common_note,
            'checked_by': CB,
            'verification': 'ai-checked'},
    }


if __name__ == '__main__':
    act = sys.argv[sys.argv.index('--apply') + 1] if '--apply' in sys.argv else '(EU) 2022/1326 [to confirm]'
    r = rows(act)
    if '--apply' not in sys.argv:
        print(json.dumps(r, ensure_ascii=False, indent=1)[:3000]); sys.exit()
    for slug, row in r.items():
        p = ROOT / f'data/legal/{slug}.json'
        d = json.load(open(p, encoding='utf-8'))
        ents = d['entries']
        # insert after the generic EU row; replace an earlier staged row if present
        ents[:] = [e for e in ents if not (e['jurisdiction'] == 'European Union' and e['status'].startswith(row['status'][:25]))]
        idx = next(i for i, e in enumerate(ents) if e['jurisdiction'] == 'European Union')
        g = ents[idx]
        g['note'] = g['note'].replace("whether a substance that is not under UN control is listed in the Framework Decision's Annex (substances brought under EU-wide control) was not checked here.",
                                      "members listed in the Framework Decision's Annex (substances brought under EU-wide control) are in the next row.")
        ents.insert(idx + 1, row)
        open(p, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=1) + '\n')
        print('applied', slug)
