"""Independent manual Table 3 transcription and arithmetic; source PDF only.
Read the 300-dpi original renders rotated clockwise 90 degrees.
This records table labels; it does not verify primary reports or unique patients.
"""
import hashlib
import json
from collections import Counter
from pathlib import Path

OUT = Path('/workspace/scratch/d1ee8d93ce58/pharmakon-project/data/verification/pdf-2026-11-01/bd/adjudication/353-round2-faria-recovery')
PDF = Path('/workspace/scratch/d1ee8d93ce58/pharmakon-uploads/PDFs/MDMA/Faria_2020_HyponatraemiaReview.pdf')
# Columns: reference, gender label, age, substances, concentration, amount,
#          sodium values (all printed numeric values), outcome, hyponatraemia effect label.
# Empty strings mean visibly blank cells. Unknown is preserved as a category.
raw = [
('Salathe et al., 2018','Female',19,'Methamphetamine','Unknown','Unknown',[],'Unknown',True),
('Thakkar et al., 2017','Female',20,'MDMA','Unknown','A quarter tablet',[112],'Recovery',True),
('Vakde et al., 2014','Male',24,'Molly (pure form of MDMA); Cannabinoids; Benzodiazepines; Purple drank (promethazine and codeine)','Unknown','Unknown',[137,129],'Recovery',False),
('Ghatol and Kazory, 2012','Female',20,'MDMA','Unknown','Two tablets (273 mg each)',[123],'Recovery',True),
('Berney-Meyer et al., 2012','Male',23,'MDMA; BZP','Unknown','Two tablets',[],'Death',True),
('Boulanger-Gobeil et al., 2012','Female (60 Kg)',22,'Ethcathinone; Methylone','Unknown','Unknown',[120],'Recovery',True),
('Claffey, 2011','Female',26,'MDMA','Unknown','Unknown',[126],'Death',False),
('Aramendi and Manzanares, 2010','Female',None,'MDMA','Unknown','50 mg',[109],'Death',True),
('Niemeijer et al., 2009','Female',19,'MDMA; Benzodiazepines','Unknown','Unknown',[118],'Recovery',True),
('Farah and Farah, 2008','Female',13,'MDMA','Unknown','Unknown',[123],'Recovery',True),
('Rosenson et al., 2007','Female',19,'MDMA','Unknown','Unknown',[122],'Death',True),
('Rosenson et al., 2007','Female',20,'MDMA','Unknown','Unknown',[124],'Death',True),
('Rosenson et al., 2007','Female',20,'MDMA','Unknown','Unknown',[119],'Death',True),
('Rosenson et al., 2007','Female',16,'MDMA','Unknown','Unknown',[123],'Death',True),
('Rosenson et al., 2007','Female',29,'MDMA','Unknown','Unknown',[],'Death',True),
('Rosenson et al., 2007','Female',16,'MDMA','Unknown','Unknown',[],'Death',True),
('Rosenson et al., 2007','Female',14,'MDMA','Unknown','Unknown',[],'Death',True),
('Rosenson et al., 2007','Male',18,'MDMA','Unknown','Unknown',[],'Death',True),
('Rosenson et al., 2007','Female',18,'MDMA','Unknown','Unknown',[],'Death',True),
('Rosenson et al., 2007','Female',16,'MDMA','Unknown','Unknown',[],'Death',True),
('Kalantar-Zadeh et al., 2006','Female (55 Kg)',20,'MDMA','Unknown','Several tablets',[117],'Death',True),
('Karlovsek et al., 2005','Male',21,'MDMA','Blood: 3.2 mg/L; Urine: 280 mg/L','Two tablets',[],'Death',False),
('Karlovsek et al., 2005','Male',49,'MDMA; Insulin (diabetic individual)','Blood: 9.1 mg/L MDMA and 510.4 mE/L insulin; Urine: 13.5 mg/L MDMA','Unknown',[],'Death',False),
('Libiseller et al., 2005','Female (52 Kg)',19,'MDMA; MDA; Cannabinoids (11-hydroxy-THC; and 11-nor-9-carboxy-THC)','Blood: 3.8 mg/L MDMA; 1.6 microgram/L 11-hydroxy-THC; 65 microgram/L 11-nor-9-carboxy-THC','Four tablets',[],'Death',False),
('Brvar et al., 2004','Female (65 Kg)',18,'MDMA','Blood: 0.87 mg/L','5 tablets (60 mg each)',[130],'Recovery',True),
('Ben-Abraham et al., 2003','Female',24,'MDMA','Unknown','Unknown',[],'Recovery',True),
('Ben-Abraham et al., 2003','Female',23,'MDMA','Unknown','Unknown',[],'Recovery',True),
('Ben-Abraham et al., 2003','Male',21,'MDMA','Unknown','Unknown',[],'Recovery',True),
('Budisavljevic et al., 2003','Female (65 Kg)',18,'MDMA','Unknown','One tablet',[124],'Recovery',True),
('Cherney et al., 2002','Female (50 Kg)',20,'MDMA','Unknown','One tablet',[112],'Unknown',True),
('Traub et al., 2002','Female',19,'MDMA','Unknown','One tablet',[121],'Recovery',True),
('Braback and Humble, 2001','Female',20,'MDMA','Unknown','One tablet',[],'Death',True),
('2001','Female',21,'MDMA','Unknown','One tablet',[126],'Death',True),
('Balmelli et al., 2001','Female',23,'MDMA; A2 (BZP)','Unknown','Unknown',[115],'Death',True),
('Gomez-Balaguer et al., 2000','Female',18,'MDMA','Unknown','Three tablets',[120],'Recovery',True),
("O'Connor et al., 1999",'Female',27,'MDMA','Unknown','',[],'',True),
('Holmes et al., 1999','Female',26,'MDMA','Unknown','One tablet',[101],'Recovery',True),
('Magee et al., 1998','Female',17,'MDMA','Unknown','One tablet',[124],'Recovery',True),
('Ajaelo et al., 1998','Female',19,'MDMA','Unknown','Unknown',[115],'Recovery',True),
('Nuvials et al., 1997','Female',20,'MDMA','Unknown','One and a half tablets',[119],'Recovery',True),
('Parr et al., 1997','Female',15,'MDMA','Unknown','Unknown',[125],'Death',True),
('Box et al., 1997','Female',30,'MDMA','Unknown','One tablet',[117],'Unknown',True),
('Watson et al., 1997','Female',24,'MDMA','Unknown','Unknown',[113],'Recovery',True),
('Matthai et al., 1996','Female',15,'MDMA','Unknown','Unknown',[119],'Recovery',True),
('Matthai et al., 1996','Female',16,'MDMA; MDA','Unknown','Unknown',[112],'Recovery',True),
('Wilkins, 1996','Female',16,'MDMA','Unknown','Unknown',[112],'Recovery',True),
('Wilkins, 1996','Female',15,'MDMA','Unknown','Unknown',[119],'Recovery',True),
('Holden and Jackson, 1996','Female',20,'MDMA','Unknown','One tablet',[112],'Recovery',True),
('Satchell and Connaughton, 1994','Female',24,'MDMA','Unknown','Unknown',[120],'Recovery',True),
('Maxwell et al., 1993','Female',17,'MDMA; MDA','Unknown','One capsule',[118],'Recovery',True),
('Maxwell et al., 1993','Female',17,'MDMA; MDA','Unknown','One and a half tablets',[130],'Recovery',True),
('Chen and Viola, 1991','Female',23,'MDMA','Unknown','One-half tablet',[123],'Recovery',True),
]
rows=[]
for n, (ref, gender, age, substances, concentration, amount, sodium, outcome, hypo) in enumerate(raw, 1):
    rows.append(dict(row=n, pdf_page=5 if n<=26 else 6, reference=ref,
        gender_printed=gender, sex=gender.split(' ')[0], age=age,
        age_printed='Unknown' if age is None else str(age), substances=substances,
        concentration=concentration, amount_ingested=amount,
        amount_availability='blank' if amount=='' else 'unknown' if amount=='Unknown' else 'reported',
        sodium_numeric_mmol_per_L=sodium, sodium_min_mmol_per_L=min(sodium) if sodium else None,
        sodium_reporting='numeric' if sodium else 'blank' if n==36 else 'unknown',
        outcome=outcome, hyponatraemia_in_effect_labels=hypo))
rows[2]['sodium_printed_context']='137 mmol/L (day one); 129 mmol/L (day three)'
rows[17]['sodium_printed_spelling']='Unknonwn'
rows[38]['sodium_printed_context']='115 mmol7L (printed unit typo; numeric value counted as 115)'
rows[35]['blank_cells']=['amount_ingested','sodium_plasma_concentration','outcome']
for r in rows:
    r['mdma_labelled']='MDMA' in r['substances']
    r['additional_label_beyond_MDMA']=r['mdma_labelled'] and (';' in r['substances'])
    # MDA-only additional labels are kept distinct; they are not evidence of an independent co-exposure.
    r['additional_label_other_than_MDA']=r['row'] in [3,5,9,23,24,34]

j=lambda name,data: (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
j('table3_reader414.json',dict(reader='AI reader414 (ChatGPT/OpenAI; fresh isolated context)',
    source=str(PDF),method='Independent visual transcription of both original Table 3 pages rendered at 300 dpi and rotated clockwise 90 degrees. Row numbers are reader-assigned, not printed in the article.',
    conventions=['Rows, not verified unique patients.','Numeric sodium values, amount text and outcome labels are table data, not clinical validation.','Unknown and blank cells remain distinct.','Molly (pure form of MDMA) is included in MDMA-labelled rows.','Additional MDMA substance labels are counted separately from labels other than MDA.'],rows=rows))

ids=lambda seq:[r['row'] for r in seq]
fatal=[r for r in rows if r['outcome']=='Death']
recovered=[r for r in rows if r['outcome']=='Recovery']
with_sodium=[r for r in rows if r['sodium_numeric_mmol_per_L']]
fatal_na=[r for r in fatal if r['sodium_numeric_mmol_per_L']]
recovery_na=[r for r in recovered if r['sodium_numeric_mmol_per_L']]
missing_amount=[r for r in rows if r['amount_availability']!='reported']
rosenson=[r for r in rows if r['reference']=='Rosenson et al., 2007']
all_values=[v for r in rows for v in r['sodium_numeric_mmol_per_L']]
mins=[r['sodium_min_mmol_per_L'] for r in with_sodium]
rg=lambda vals:[min(vals),max(vals)]
calc=dict(
    total_rows=len(rows),rows_by_page=dict(Counter(str(r['pdf_page']) for r in rows)),
    sex_counts=dict(Counter(r['sex'] for r in rows)),
    male_rows=ids([r for r in rows if r['sex']=='Male']),
    age_range=rg([r['age'] for r in rows if r['age'] is not None]),age_unknown_rows=ids([r for r in rows if r['age'] is None]),
    reference_year_range=[1991,2018],mdma_labelled_rows=sum(r['mdma_labelled'] for r in rows),
    other_main_substance_rows=[dict(row=1,substances=rows[0]['substances']),dict(row=6,substances=rows[5]['substances'])],
    outcome_counts=dict(Counter(r['outcome'] or 'blank' for r in rows)),
    death_rows=ids(fatal),recovery_rows=ids(recovered),unknown_outcome_rows=ids([r for r in rows if r['outcome']=='Unknown']),blank_outcome_rows=ids([r for r in rows if r['outcome']=='']),
    sodium_reporting_counts=dict(Counter(r['sodium_reporting'] for r in rows)),
    sodium_numeric_rows=ids(with_sodium),sodium_absent_rows=ids([r for r in rows if not r['sodium_numeric_mmol_per_L']]),
    sodium_rows_count=len(with_sodium),sodium_all_numeric_entries_count=len(all_values),
    sodium_lowest_per_row_range=rg(mins),sodium_all_printed_values_range=rg(all_values),
    fatal_sodium_rows=ids(fatal_na),fatal_sodium_count=len(fatal_na),fatal_sodium_range=rg([r['sodium_min_mmol_per_L'] for r in fatal_na]),
    recovery_sodium_rows=ids(recovery_na),recovery_sodium_count=len(recovery_na),recovery_sodium_lowest_per_row_range=rg([r['sodium_min_mmol_per_L'] for r in recovery_na]),
    recovery_sodium_all_values_range=rg([v for r in recovery_na for v in r['sodium_numeric_mmol_per_L']]),
    amount_availability_counts=dict(Counter(r['amount_availability'] for r in rows)),
    amount_unknown_or_blank_count=len(missing_amount),amount_unknown_or_blank_rows=ids(missing_amount),
    fatal_amount_unknown_or_blank_count=sum(r['amount_availability']!='reported' for r in fatal),
    fatal_amount_unknown_or_blank_rows=ids([r for r in fatal if r['amount_availability']!='reported']),
    numeric_concentration_rows=ids([r for r in rows if r['concentration']!='Unknown']),
    additional_substance_label_MDma_rows=ids([r for r in rows if r['additional_label_beyond_MDMA']]),
    additional_label_other_than_MDA_rows=ids([r for r in rows if r['additional_label_other_than_MDA']]),
    MDA_only_additional_label_rows=ids([r for r in rows if r['additional_label_beyond_MDMA'] and not r['additional_label_other_than_MDA']]),
    multiple_substance_label_rows_including_ethcathinone_methylone=ids([r for r in rows if ';' in r['substances']]),
    fatal_rows_without_numeric_sodium_and_without_hyponatraemia_effect_label=ids([r for r in fatal if not r['sodium_numeric_mmol_per_L'] and not r['hyponatraemia_in_effect_labels']]),
    Rosenson_citation_rows=ids(rosenson),Rosenson_citation_outcome_counts=dict(Counter(r['outcome'] for r in rosenson)),
    Rosenson_citation_sex_counts=dict(Counter(r['sex'] for r in rosenson)),
    female_share=dict(formula='46 / 52 * 100',percent=46/52*100,one_decimal=round(46/52*100,1),article_printed_percent=89),
    conditional_duplicate_omission=dict(probable_matching_pairs=[[44,47],[45,46]],omitted_Wilkins_rows=[46,47],formula_rows='52 - 2 = 50',formula_female='46 - 2 = 44',formula_percent='44 / 50 * 100',rows=50,female_rows=44,percent=44/50*100,unique_patient_count_verified=False),
    scope='These calculations reproduce the printed table labels. Shared references are citation overlap; exact primary patient identity, primary-report correctness, case completeness, population rates and causal mechanisms are not verified.'
)
assert len(rows)==52
assert Counter(r['sex'] for r in rows)=={'Female':46,'Male':6}
assert Counter(r['outcome'] or 'blank' for r in rows)=={'Death':21,'Recovery':27,'Unknown':3,'blank':1}
assert len(with_sodium)==36 and len(all_values)==37
assert len(fatal_na)==10 and len(recovery_na)==24
assert len(missing_amount)==30
assert len([r for r in fatal if r['amount_availability']!='reported'])==14
assert ids([r for r in rows if r['additional_label_beyond_MDMA']])==[3,5,9,23,24,34,45,50,51]
j('arithmetic_reader414.json',calc)
print(json.dumps({k:calc[k] for k in ['total_rows','sex_counts','outcome_counts','sodium_rows_count','sodium_lowest_per_row_range','sodium_all_printed_values_range','amount_unknown_or_blank_count','fatal_amount_unknown_or_blank_count','female_share','conditional_duplicate_omission']},indent=2))
