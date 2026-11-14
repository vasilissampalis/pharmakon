import json, re, sys
P = '/home/claude/pharmakon/data/study-cards/mdma.json'
L = json.load(open(P, encoding='utf-8'))
c = next(x for x in L if x['id'] == 'sc_hysek_2014')
ver = c['verification']; dis = ver.setdefault('disagreements', [])
WHO = "AI reader 674 (first reader, PDF, 14 November 2026); checked at the PDF by AI reader 688 (round-2 check)"
def log(field, old, new, res="Correction from the PDF by AI reader 674, confirmed at the PDF by AI reader 688; adopted by the AI co-editor."):
    dis.append({"field": field, "first_pass": old, "reviewer": new, "resolution": res})
def rep(obj, key, old, new, field):
    assert obj[key].count(old) == 1, (field, old[:60])
    before = obj[key]; obj[key] = before.replace(old, new); log(field, old, new)
# 0. inequality-aversion: the group is named (prosocial orientation); only the number is missing
rep(c['sample'], 'attrition', "without saying which volunteers or how many were analysed.", "the inequality-aversion test in volunteers 'with a prosocial orientation' (how many is not given), the plasma comparison without saying how many were analysed.", "sample.attrition")
rep(c['reporting_issues'][1], 'issue', "and the inequality-aversion test with 1 and 20, without saying how many volunteers were analysed.", "and the inequality-aversion test with 1 and 20; the latter was run in volunteers 'with a prosocial orientation' (p. 1647), without saying how many.", "reporting_issues[1].issue")
# 1. plasma levels: the figure's mean curves and the printed means disagree for the area under the curve (editors' calculation)
c['reporting_issues'].append({"issue": "The printed areas under the plasma MDMA curve (AUC0-6h 926.8 ng/mL h in men, 1146.5 in women, p. 1648) do not match Figure 4E: the area under its plotted mean curves is about 866 (men) and 921 (women) ng/mL h (editors' trapezoid calculation from the plotted means; the area under a mean curve equals the mean of the individual areas). The curves peak at about 183 (men) and 194 (women) ng/mL at 2.5 h, below the printed mean Cmax of 209 and 269.9, which by itself is expected, since people peak at different times.", "consequence": "The size of the sex difference in plasma levels is uncertain (about 20% smaller in women by the figure); the paper does not explain the gap.", "page": "pp. 1648-1649", "locator": "Results > Endocrine effects and pharmacokinetics of MDMA, 2nd paragraph; Figure 4E"})
log("reporting_issues (added)", "", "AUC mismatch between text and Figure 4E", "Missed reporting issue found by AI reader 674; AI reader 688 confirmed it in part (the Cmax gap alone is expected; the AUC gap is real) and gave the calculation; adopted by the AI co-editor.")
# 2. effect sizes can be read from the vector figures
rep(c, 'cannot_establish', "the size of any effect (the text prints test statistics, not means; means are in Figures 1 to 3 and Supplementary Table S1, not read); ", "the exact size of each effect (the text prints test statistics, not means; approximate means can be read from the figures, and Supplementary Table S1 was not read); ", "cannot_establish")
rep(c['analysis'], 'effect_sizes', "No means, SDs or effect sizes are printed in the text; the values are in the figures and Supplementary Table S1 (not read).", "No means, SDs or effect sizes are printed in the text; Supplementary Table S1 was not read. Approximate means read from the PDF's vector figures (editors' readings by two readers, placebo then MDMA): explicit emotional empathy (1 to 9 scale) all 4.40 and 5.01, women 4.96 and 5.15, men 3.84 and 4.87; implicit all 4.30 and 4.81, women 4.79 and 4.79, men 3.81 and 4.83; cognitive empathy 62.3% and 61.9%; prosocial angle all 31.2 and 36.9 degrees, women 36.8 and 36.6, men 25.7 and 37.2; inequality-aversion index all 0.48 and 0.38; change in oxytocin 12.2 and 65.9 pg/mL.", "analysis.effect_sizes")
rep(c['reporting_issues'][4], 'issue', "No means or SDs for any outcome are printed in the text; the results are test statistics and p-values, with values in figures and a supplement.", "No means or SDs for the task and rating outcomes are printed in the text (the pharmacokinetic means are, with SEM); the values are in the figures and a supplement.", "reporting_issues[4].issue")
rep(c['reporting_issues'][4], 'consequence', "The size of effects cannot be taken from the article text; the supplement was not read.", "Effect sizes can only be read approximately from the figures (given under analysis); the supplement was not read.", "reporting_issues[4].consequence")
# 3. the citation of Bedi et al.
t0 = c['replication']['timeline'][0]
old = t0['event']
t0['event'] = "Bedi et al. (Chicago): MDMA impaired recognition of fearful faces and did not improve emotion recognition overall. These authors cite Bedi et al. (2009 and 2010) together for raised self-rated sociability; in Bedi et al. (2010) only methamphetamine raised self-rated sociability significantly (MDMA raised loving and friendliness ratings), so the citation holds for the 2009 study only."
log("replication.timeline[0].event", old, t0['event'])
# 4. where the sessions took place is not stated
rep(c, 'can_establish', "as measured in a hospital laboratory over the hours", "as measured in laboratory sessions (where they took place is not stated) over the hours", "can_establish")
rep(c['sample'], 'selection_effects', "tested in a hospital unit;", "tested in laboratory sessions (the place is not stated);", "sample.selection_effects")
rep(c, 'what_would_settle_it', "outside a hospital room.", "outside the laboratory.", "what_would_settle_it")
# 5. random order is stated only in the abstract
rob = c['risk_of_bias']['domains'][0]
rep(rob, 'note', "Random order is stated;", "Random order is stated only in the abstract (the Methods describe a double-blind, placebo-controlled cross-over without mentioning randomization);", "risk_of_bias.domains[0].note")
rep(c, 'design_detail', "Double-blind, placebo-controlled, random-order crossover laboratory study", "Double-blind, placebo-controlled crossover laboratory study (random order stated in the abstract only)", "design_detail")
# 6 and 7. face recognition: sex interactions and the correlation in women
kf5 = c['key_findings'][5]; old = kf5['finding']
kf5['finding'] = old.rstrip() + " MDMA's effect on recognising fearful and sad faces differed between women and men (sex-by-treatment F(1,31) = 6.61, p = 0.015, and 9.42, p = 0.005). In women, fear recognition accuracy was lower the higher the plasma MDMA (Cmax Rp = -0.62, P = 0.014; AUC0-6h Rp = -0.66, P = 0.006; n = 16; editors' calculation: P = 0.014 fits 15 women, P = 0.006 fits 16)."
log("key_findings[5].finding (added)", "", "sex interactions for fearful and sad faces; the correlation with plasma levels in women")
# 8. the Discussion reverses the inequality-aversion direction
c['reporting_issues'].append({"issue": "The Discussion describes 'a trend reduction in inequality-aversion' (p. 1648), but by the paper's own definition (index 0 = perfect inequality aversion, p. 1646) a lower index after MDMA means a shift towards inequality aversion, as the Results say (p. 1647).", "consequence": "The direction of this non-significant trend is stated the wrong way round in the Discussion; the Results and Figure 3 are consistent with each other.", "page": "pp. 1646-1648", "locator": "Methods (definition of the index); Results > Social Value Orientation, 1st paragraph; Discussion, 1st paragraph"})
log("reporting_issues (added)", "", "inequality-aversion direction reversed in the Discussion")
# 9. the 'more than two doses' limitation
kf7 = c['key_findings'][7]; old = kf7['finding']
kf7['finding'] = old.rstrip() + " The limitations give avoiding exposure of mostly drug-naive volunteers to more than two doses of MDMA as the reason no dose-response study was done, although the Methods describe one MDMA session per person."
log("key_findings[7].finding (added)", "", "the 'more than two doses' limitation")
# 10. pharmacokinetics printed in the text
kf6 = c['key_findings'][6]; old = kf6['finding']
kf6['finding'] = old.rstrip() + " Printed pharmacokinetics (mean, SEM): AUC0-6h 926.8 (29.3) ng/mL h in men and 1146.5 (37.9) in women, F(1,15) = 20.77; Tmax 2.44 h (0.14) overall, 2.10 (0.20) in men and 2.75 (0.17) in women."
log("key_findings[6].finding (added)", "", "AUC0-6h and Tmax as printed")
rep(c['exposure'], 'measurement', "(Cmax 209 ng/mL in men and 269.9 in women, SEM 6.4 and 9.3).", "(Cmax 209 ng/mL in men and 269.9 in women, SEM 6.4 and 9.3; AUC0-6h 926.8 and 1146.5 ng/mL h, SEM 29.3 and 37.9; Tmax 2.10 and 2.75 h).", "exposure.measurement")
# 11. printed pages for every key finding
pages = ["pp. 1645-1646", "p. 1647", "p. 1647", "p. 1647", "p. 1647", "pp. 1647-1648", "p. 1648", "p. 1650", "p. 1645"]
for i, pg in enumerate(pages):
    assert c['key_findings'][i]['page'] == 'PMC HTML', i
    c['key_findings'][i]['page'] = pg
log("key_findings[].page", "PMC HTML", "printed pages of the version of record (pp. 1645-1651)")
ver['status'] = 'ai-checked'
ver['source_read'] = ver['source_read'] + " Re-read from the PDF (version of record, Social Cognitive and Affective Neuroscience 9(11):1645-1652, all 8 pages; figures read at 300 dpi and from the vector coordinates) by AI reader 674 on 14 November 2026, whose corrections AI reader 688 checked at the PDF, also confirming every other number on the card; pages now cite the printed pages. Supplementary Table S1 not read."
ver['checked_by'] = "AI reader 688 (round-2 check at the PDF, round pdf-2026-11-14); adjudicated by the AI co-editor"
ver['checked_on'] = "2026-11-14"
json.dump(L, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); open(P, 'a').write('\n')
print('Hysek card corrected:', len(dis), 'disagreement entries')
