"""Fresh reader418 calculations, from supplied primary PDFs only.

No cards, prior calculations or other readers' files are inputs.
Table 3 is independently extracted from the original PDF's cell grid and
checked visually against reader418's own 300 dpi render. Leikin Table 2
and the Drummer/Hancock counts below are independently transcribed.
"""
from pathlib import Path
from decimal import Decimal
from statistics import median
import csv
import json
import re
import pdfplumber

BASE = Path('/workspace/scratch/d1ee8d93ce58/pharmakon-project/data/verification/pdf-2026-11-01/dd/adjudication/349-round2-recovery')
TMP = Path('/workspace/scratch/d1ee8d93ce58/tmp/pdfs/reader418')
PDF = Path('/workspace/scratch/d1ee8d93ce58/pharmakon-uploads/PDFs')
with pdfplumber.open(PDF / '_Cross-cutting/Ketola_2019_PostMortemSpecimenRatiosMA.pdf') as doc:
    table = doc.pages[43].extract_tables()[0]
rows = table[1:-3]
assert len(rows) == 50 and all(len(r) == 21 for r in rows)
specimens = ['other blood', 'vitreous humour', 'muscle', 'liver', 'kidney', 'brain', 'heart', 'lung', 'spleen', 'bile']
with (BASE / 'ketola_table3_reader418.csv').open('w') as f:
    writer = csv.writer(f)
    writer.writerow(['compound'] + [x for s in specimens for x in (s, s + ' N')])
    writer.writerows(rows)
summary = {}
for j, specimen in enumerate(specimens):
    values = [(Decimal(r[1+2*j]), r[0], int(r[2+2*j])) for r in rows if r[1+2*j]]
    lo, hi = min(x[0] for x in values), max(x[0] for x in values)
    summary[specimen] = {
        'numeric_drug_medians': len(values),
        'sum_N_cells': sum(int(r[2+2*j]) for r in rows if r[2+2*j]),
        'median_of_printed_drug_medians': str(median(x[0] for x in values)),
        'printed_summary_median': table[-1][1+2*j],
        'minimum': str(lo), 'minimum_drugs_and_N': [[n, N] for v, n, N in values if v == lo],
        'maximum': str(hi), 'maximum_drugs_and_N': [[n, N] for v, n, N in values if v == hi],
        'max_div_min': str(hi / lo),
        'positive_N_without_ratio': [[r[0], int(r[2+2*j])] for r in rows if not r[1+2*j] and r[2+2*j] and int(r[2+2*j]) > 0]
    }

# Entries transcribed column-by-column from Leikin Table 2, printed p.49.
leikin_left = '''Alfentanil
Alprazolam (1.5)
Amantadine (2)
Amineptine hydrochloride
Amitriptyline (3.1)
Amoxapine (1.8)
Amphetamine (2.0)
Benztropine (1.3)
Brompheniramine
Bupropion (1.9)
Chloroquine (3.0)
Chlorpheniramine (3.1)
Chlorpromazine (4.0)
Clomipramine (1.9)
Clonazepam (2.0)
Clothiapine
Clozapine (2.8)
Cocaine (1.5 to 2.3)
Codeine (1.8)
Cyanide (1.3)
Cyclobenzaprine (2.2)
D-methamphetamine (2.1)
Desipramine (2.4)
Dextromethorphan (2)
Diazepam (1.6)
Diltiazem (2.6)
Diphenhydramine (2.3)
Dothiepin (3)
Doxepin (5.5)
Doxylamine
Flecanide (3.6)
Flunitrazepam (3)
Fluoxetine (2.9)
Flurazepan (3.0)
Fluvoxamine (1.7)
Furosemide (1.7)
Gamma hydroxybutyrate (2)
Haloperidol (3.6)
Hydrochlorthiazide (23)
Ibuprofen (1.8)
Imipramine (1.8 to 2.2)
Indomethacin (1.9)
Ketamine (1.6)
Lidocaine
Maprotiline (4.7)
Meprobamate (1.7)
Mesoridazine (1.3)
Metapramine
Methamphetamine (2.4)
Methotrimeprazine (1.3)'''
leikin_right = '''Methylenedioxy methamphetamine MDMA (2.65)
Methylfentanyl
Methyprylon (1.9)
Metoprolol (3.8)
Mexiletine (3.6)
Midazolam (4)
Morphine (heroin) (2.2)
Naproxen (1.5)
N-methylbenzodioxazolybutamine or MBDB (2.5)
Nicotine (Cotinine-3)
Nitrazepam
Nortriptyline (2.4)
Orphenadrine (1.9)
Oxazepam (1.3)
Oxycodone (3.1)
Paramethoxyamphetamine (1.6)
Paroxetine (2.7)
Pentazocine (2)
Pentobarbital
Pethidine or meperidine (2.1)
Phencyclidine (1.8)
Phentermine (1.7)
Phenylbutazone (2.3)
Phenylpropanolamine (2.4)
Phenytoin (1.4)
Protriptyline
Promethazine (1.6)
Propafenone (2.4)
Propoxyphene (3.5)
Propranolol (2.5)
Pseudoephedrine (1.5)
Quetiapine
Remifentanil
Secobarbital (1.5)
Strychnine (15)
Sufentanil
Temazepam (1.6.)
Tetrahydrocannabinol
Thiopental (1.9)
Timolol (2)
Tranylcypromine (2.2)
Trazadone (1.6)
Triazolam (2.8)
Trichlorethanol (2.0)
Trimipramine (1.6)
Venlafaxine (1.6)
Venlafaxine (1.6)
Verapamil
Zolpidem (2.1)'''
leikin_entries = []
for column, text in [('left', leikin_left), ('right', leikin_right)]:
    for i, line in enumerate(text.splitlines(), 1):
        label = re.sub(r'\s+\([^()]*[0-9][^()]*\)$', '', line)
        numeric_annotation = bool(re.search(r'\([^()]*[0-9][^()]*\)$', line))
        m = re.search(r'\(([0-9.]+)\)$', line)
        value = Decimal(m.group(1).rstrip('.')) if m else None
        leikin_entries.append({'column': column, 'entry_in_column': i, 'printed_entry': line,
                               'label': label, 'numeric_parentheses': numeric_annotation,
                               'single_numeric_ratio': str(value) if value is not None else None})
with (BASE / 'leikin_table2_reader418.json').open('w') as f:
    json.dump(leikin_entries, f, indent=2, ensure_ascii=False)
unique_labels = set(r['label'] for r in leikin_entries)
numeric_labels = {r['label'] for r in leikin_entries if r['numeric_parentheses']}
no_numeric = sorted(unique_labels - numeric_labels)

def comparison_name(label):
    return {'Morphine (heroin)': 'Morphine', 'Trazadone': 'Trazodone'}.get(label, label)
other_blood = {r[0]: Decimal(r[1]) for r in rows if r[1]}
leikin_values = {comparison_name(r['label']): Decimal(r['single_numeric_ratio']) for r in leikin_entries if r['single_numeric_ratio']}
comparison = []
for label in sorted(leikin_values.keys() & other_blood.keys()):
    ratio = leikin_values[label] / other_blood[label]
    category = 'above_1.10' if ratio > Decimal('1.10') else 'below_1_div_1.10' if ratio < 1 / Decimal('1.10') else 'between'
    comparison.append({'label': label, 'Leikin': str(leikin_values[label]), 'Ketola_other_blood': str(other_blood[label]),
                       'Leikin_div_Ketola': str(ratio), 'category': category})

# Table 1 nonfatal cases. Every listed individual is represented, including
# the three-person and two-person rows; age 40(s) is retained as an interval.
drummer_nonfatal = [
 (1, [25], 'M'), (2, [21], 'M'), (3, [33], 'F'), (4, [24], 'F'),
 (5, [18,26,30], 'M'), (6, [21], 'M'), (7, [35], 'F'), (8, [48,22], 'M'),
 (9, [26], 'M'), (10, [53], 'M'), (11, [23,50], 'M'), (12, [15], 'M'),
 (13, [36], 'F'), (14, [45], 'F'), (15, [26], 'M'), (16, [37], 'M'),
 (17, [26], 'M'), (18, [19], 'M'), (19, [33], 'M'), (20, [42], 'M'),
 (21, ['40s'], 'M'), (22, [24], 'M'), (23, [21], 'M'), (24, [23], 'M'),
 (25, [21], 'M'), (26, [29], 'M'), (27, [27], 'M'), (28, [19], 'M'),
 (29, [24], 'M'), (30, [15], 'M'), (31, [28], 'M')
]
ages_min = [40 if a == '40s' else a for _, ages, _ in drummer_nonfatal for a in ages]
ages_max = [49 if a == '40s' else a for _, ages, _ in drummer_nonfatal for a in ages]
female_ages = [a for _, ages, sex in drummer_nonfatal if sex == 'F' for a in ages]

# Relevant Table 3 effect/interval transcriptions are from the review, not
# independently read original Mittleman/Mukamal/etc. primary articles.
drummer_epi = {
 'Mittleman': {'n':3882,'AMI_first_hour':4.8,'printed_95_CI':[2.9,9.5], 'AMI_second_hour_text':1.7,
               'second_effect_95_CI_from_table':[0.6,5.1], 'table_window_label':'within 2 h',
               'centers':64, 'enrollment':'August 1989–September 1996'},
 'Mukamal': {'n':1913,'weekly_HR':4.2,'weekly_95_CI':[1.2,14], 'less_than_weekly_HR':2.5,
              'less_than_weekly_95_CI':[0.9,7.3], 'centers':45,'enrollment':'1989–1994'},
 'Frost': {'n':3886,'follow_up_years':18,'mortality_percent_higher':29,'significant':False,
           'centers':64,'enrollment':'1989–1996','study_name':'Determinants of MI Onset Study'},
 'Rumalla': {'stroke_adjusted_RR':1.17,'printed_95_CI':[1.15,1.20]},
 'DeFilippis': {'n':2097,'CV_mortality_adjusted_HR':2.22,'printed_CI_level':'90%', 'printed_CI':[1.27,3.70]},
 'Reis': {'n':5113,'follow_up':'>25 years','CV_mortality':'no association'},
 'Jouanjus': {'notification_period':'2006–2010','cardiovascular_notifications':35,'deaths':9,
              'deaths_div_CV_notifications_percent':9/35*100},
 'Desai': {'text_population':'>2 million AMI admissions','overall_in_hospital_mortality':'no increase',
           'table_population':'2.45 million admissions','table_outcome':'AMI association'}
}

calculations = {
 'method':'reader418 own primary-PDF extraction, manual transcription and arithmetic; no prior calculation file used',
 'ketola_table3':summary,
 'ketola_table3_N_total':sum(x['sum_N_cells'] for x in summary.values()),
 'ketola_known_ratio_N_total':sum(x['sum_N_cells'] for x in summary.values())-1,
 'leikin_counts':{'entries':len(leikin_entries),'distinct_labels':len(unique_labels),
                  'numeric_annotated_entries':sum(r['numeric_parentheses'] for r in leikin_entries),
                  'distinct_numeric_annotated_labels':len(numeric_labels),
                  'numeric_annotated_label_with_ambiguous_target':'Nicotine (Cotinine-3)',
                  'distinct_labels_without_numeric_parentheses':len(no_numeric),'labels_without_numeric_parentheses':no_numeric},
 'leikin_ketola_comparison':{'denominator_definition':'distinct labels with a single numeric Leikin Table 2 ratio AND a numeric Ketola Table 3 other-blood ratio; Morphine (heroin) mapped to Morphine and printed Trazadone to Trazodone',
                            'n':len(comparison),'counts':{c:sum(r['category']==c for r in comparison) for c in ['above_1.10','below_1_div_1.10','between']},'rows':comparison},
 'pounder_surrounding_editorial_arithmetic':{'max_min_ratios':{k:hi/lo for k,lo,hi in [
    ('doxepin',3.6,12.5),('amobarbital',4.3,25.8),('secobarbital',3.9,25.3),('pentobarbital',5.1,31.5),
    ('clomipramine',4.0,21.5),('flurazepam',0.15,0.99),('imipramine',4.1,18.1),('hospital_lidocaine',0.9,1.4)]},
    'imipramine_post_vs_hospital':[4.1/2.3,18.1/2.3],'hospital_sample_to_death_implied_hours':9.25-7.25,
    'caution':'Case 2 printed blood range is explicitly systemic; portal venous values are higher and are separately reported. Case 1 actual death time is unknown (17 h after discovery; 40 h after last known alive).'},
 'hancock_table1':{'cells':{'preliminary_yes_final_yes':2454,'preliminary_yes_final_no':265,
                          'preliminary_no_final_yes':115,'preliminary_no_final_no':122},
                    'preliminary_yes_total':2454+265,'preliminary_no_total':115+122,
                    'final_yes_total':2454+115,'final_no_total':265+122,'total':2454+265+115+122,
                    'non_drug_among_suspected_percent':265/(2454+265)*100,
                    'drug_related_among_unsuspected_percent':115/(115+122)*100,
                    'source_printed_FN_percent_uses_final_positive_denominator':115/(2454+115)*100,
                    'internal_inconsistency':'Opening Results paragraph calls the column totals 2569 and 387 the preliminary groups, contrary to the table row totals 2719 and 237 and to the component case descriptions.'},
 'drummer_table1':{'numbered_reports':len(drummer_nonfatal),'individuals':len(ages_min),
                   'female_count':len(female_ages),'female_ages':female_ages,
                   'age_min':min(ages_min),'age_max':max(ages_max),
                   'median_age_using_40_for_40s':median(ages_min),'median_age_using_49_for_40s':median(ages_max),
                   'stroke_TIA_cases':{'Mouzak_table_row_5':3,'Duchene_table_row_14':1,'Leblanc_table_row_15':1,'Renard_table_row_19':1},
                   'stroke_TIA_total':6,'text_stroke_TIA_total':5,
                   'Brugada_rows':[18,20,28],'myocarditis_rows':[30],
                   'reported_text_only_counts':{'no_evidence_of_coronary_artery_disease':24,'AMI_with_CK_or_troponin_confirmation':18},
                   'limits':'Table 1 does not give a complete explicit per-case CAD/biomarker classification from which 24 and 18 can uniquely be reconstructed. They are confirmed as the review narrative counts; cited case originals were not supplied/read.'},
 'drummer_table3_secondary_only':drummer_epi,
 'borra_timing':{'reported_mean_h':17,'reported_range_h':[1,292],
                 'cited_refs':[13,18,21,22,29,72,73,75,76,77,79,80],
                 'cited_ref_count':12,'THC_repeated_sampling_ref':30,'THC_ref_in_timing_list':False,
                 'limit':'No underlying per-case timing values, weights, or aggregation method are given in the supplied review; 17 h and the range can be transcribed but cannot be recomputed here.'}
}
(BASE / 'calculations_reader418.json').write_text(json.dumps(calculations, indent=2, ensure_ascii=False)+'\n')
print(json.dumps({'Leikin':calculations['leikin_counts'],
                  'comparison_counts':calculations['leikin_ketola_comparison']['counts'],
                  'Ketola_N':calculations['ketola_table3_N_total'],
                  'Hancock_percentages':[calculations['hancock_table1']['non_drug_among_suspected_percent'],calculations['hancock_table1']['drug_related_among_unsuspected_percent']],
                  'Drummer_table1_people':calculations['drummer_table1']['individuals']}, indent=2))
