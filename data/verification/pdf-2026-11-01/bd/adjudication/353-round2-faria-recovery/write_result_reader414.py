import hashlib
import json
from collections import Counter
from pathlib import Path

base=Path('/workspace/scratch/d1ee8d93ce58/pharmakon-project/data/verification/pdf-2026-11-01/bd/adjudication/353-round2-faria-recovery')
pdf=Path('/workspace/scratch/d1ee8d93ce58/pharmakon-uploads/PDFs/MDMA/Faria_2020_HyponatraemiaReview.pdf')
tasks=json.loads((base/'tasks_reader414.json').read_text())

count_extraction=(
"Table 3 is presented as published clinical cases involving hyponatraemia after phenethylamines. "
"The independent reader's count of the printed table is 52 rows from 1991-2018, 46 female and 6 male, ages 13-49 with one age unknown; "
"50 rows are labelled MDMA (including Molly described as pure MDMA), one methamphetamine and one ethcathinone with methylone. "
"Outcomes are labelled Death in 21 rows, Recovery in 27, Unknown in 3, and are blank in 1. "
"Numeric sodium appears in 36 rows and is absent in 16; the lowest reported value within each of the 36 rows ranges from 101 to 130 mmol/L. "
"One of these rows reports 137 on day one and 129 on day three, so the range of all printed sodium values is 101-137 mmol/L, without adding a case. "
"Ten Death-labelled rows report sodium, 109-126 mmol/L, within the 101-130 mmol/L range of the lowest per-row values in the 24 Recovery-labelled rows with sodium. "
"Amount is Unknown or blank in 30 rows, including 14 of the 21 Death-labelled rows, and numeric drug concentrations appear in 4 rows. "
"Nine MDMA-labelled rows list at least one additional substance; six of these list an additional substance other than MDA, while the remaining three list MDA alone in addition to MDMA. "
"Ten Death-labelled rows, nine female and one male, cite Rosenson 2007, whose bibliography entry identifies the California series: these are citation overlap with that series, not deaths independently ascertained by this review. "
"These are table counts, not verified unique patients or population rates."
)

discrepancy_extraction=(
"Table 3 contains two pairs of female rows attributed to Matthai 1996 and Wilkins 1996 with matching ages 15/16, sodium 119/112 mmol/L and Recovery outcomes; one Matthai row additionally lists MDA. "
"They appear to be repeated case entries, but the primary reports were not read and patient identity is unverified. "
"The Wilkins bibliography entry on p. 14 has the same cerebral-oedema/unrestricted-water topic and includes an author reply; this suggests correspondence on the report, but the entry does not expressly label it a letter. "
"Conditionally omitting the two Wilkins rows leaves 50 rows and 44 female rows, not a verified distinct-patient sample. "
"The female age-23, sodium-123 mmol/L Recovery row cites Chen and Viola 1991, whose bibliography title instead concerns a laboratory method for detecting ras point mutations. "
"The fatal row cited only as 2001 resolves within the review to its first bibliography entry, A fatal case of Ecstasy poisoning, Paediatr Child Health 6(7), 491, DOI 10.1093/pch/6.7.491, PMCID PMC2807764. "
"Three Death-labelled rows (Karlovsek 2005 twice; Libiseller 2005) provide neither numeric sodium nor a hyponatraemia effect label. "
"The O'Connor 1999 row has a blank outcome even though its bibliography title reports a death; the table count remains 21 Death labels and one blank, rather than 22 primary-source-confirmed deaths. "
"The Salathe 2018 row is labelled methamphetamine although its bibliography title names ecstasy. "
"These are internal discrepancies or probable duplicate entries, not corrections verified from the unseen primary reports. "
"The four rows reporting numeric drug concentrations do not establish that every other case lacked toxicological testing."
)

results=[]
for task in tasks:
    n=task['n']
    r=dict(n=n,claim_id=task['claim_id'],anchor_index=task['anchor_index'])
    if n in (1,4):
        r.update(verdict='corrected',note=(
            "All row, sex, age, outcome, sodium, amount-availability, concentration and Rosenson-reference counts were independently reproduced from both 300-dpi rotated Table 3 pages. "
            "The unqualified phrase 'other substances in 6' needs a category definition: rows 3, 5, 9, 23, 24 and 34 list an additional substance other than MDA, but rows 45, 50 and 51 also list MDA in addition to MDMA, making nine MDMA-labelled rows with any additional substance label. "
            "The complete replacement makes that distinction and specifies that the recovery range is the per-row-lowest range (all printed recovery values extend to 137). "
            "The ten Rosenson rows establish shared citation, not a primary-verified patient match or an independently reconstructed California cohort; no cited primary report was accessed. "
            "In the surrounding statement, 'three fatal rows record no low sodium' should mean no numeric low sodium is reported in those rows, not a verified absence of hyponatraemia. "
            "The case-table description must retain the missingness, reference overlap and non-unique-patient limitations; it cannot supply an incidence, sex susceptibility denominator or dose-response comparison."
        ),corrected_extracted=count_extraction,corrected_page='PDF pp. 5-7',corrected_locator=(
            "Table 3, all 52 printed rows on PDF/printed pp. 5-6; Section 5 continuation on p. 7; reader414 manual transcription and recomputation (table3_reader414.json; arithmetic_reader414.json)."
        ))
    elif n in (2,8):
        r.update(verdict='corrected',note=(
            "The table matches, conditional 50-row/44-female recount, unrelated Chen/Viola title, identifiable anonymous 2001 entry, three fatal rows without numeric sodium or hyponatraemia labels, blank O'Connor outcome and Salathe substance/title discrepancy are reproduced in the original review. "
            "One qualification is needed: the Wilkins bibliography entry does not expressly say 'letter' or directly establish patient identity; its matching topic and 'author reply 690' support a correspondence inference only. "
            "The replacement also makes explicit the MDA label in one Matthai row, so the matching age/sodium/outcome pattern is not mistaken for complete identity of all fields. "
            "Primary case reports were not read. The source supports 'probable duplicate entries' and internal discrepancies, not proof of two unique patients repeated or verified corrections to compounds/outcomes. "
            "Accordingly, the surrounding statement's 'Two patients appear twice' should remain visibly tentative, and its 'three fatal rows record no low sodium' should not be read as normal measured sodium. "
            "The anonymous reference is identifiable within the review without opening it. Unknown quantitative concentration cells do not prove that no toxicology testing occurred."
        ),corrected_extracted=discrepancy_extraction,corrected_page='PDF pp. 5-7, 12-14',corrected_locator=(
            "Table 3 on pp. 5-6 (reader414 rows 1, 22-24, 33, 36, 44-47, 52); Section 5 continuation on p. 7; anonymous 2001 entry on p. 12; Chen/Viola, Karlovsek and Libiseller entries on p. 13; Matthai, O'Connor, Salathe and Wilkins entries on p. 14."
        ))
    elif n==3:
        r.update(verdict='confirmed',note=(
            "The mechanism summary is supported by the abstract (p. 1), introduction (p. 2), Section 5/5.1 (p. 7) and Sections 5.1.2-5.1.5 (p. 10). "
            "The review itself is literature synthesis: Methods (p. 2) describes a PubMed search through October 2019 and bibliography searching, not new hormone/fluid measurements. "
            "Page 7 calls the drinking accounts anecdotal and the oedema inference speculative and says mechanisms are not fully understood; p. 10 describes Henry 1998 second-hand and narrows the single-dose statement to deaths/permanent neurological injury reported in women aged 15-30. "
            "The independent table count is 14 of 21 Death-labelled rows with Unknown amounts. "
            "Surrounding-statement limit: saying this review did not measure fluid intake is supported; claiming no cited primary study ever measured it is not established by a review-only check. "
            "Also, the p. 12 conclusion calls MDMA mechanisms relatively well characterized while cautioning about animal-to-human extrapolation; the p. 7 caveat should not be expanded into an assertion that no human/experimental mechanistic evidence exists. "
            "All primary studies remain unread; the extraction appropriately attributes the explanation to the review."
        ))
    elif n==5:
        r.update(verdict='confirmed',note=(
            "Section 5 on p. 7 prints 89% and infers probable female predisposition. Independent 300-dpi table transcription gives 46 female rows among 52: 46/52*100 = 88.4615384615%, hence 88.5% to one decimal. "
            "Conditionally removing the two Wilkins female entries yields (46-2)/(52-2)*100 = 44/50*100 = 88.0%. "
            "No alternate denominator or reason for the printed 89% can be established from the review. The exact-patient duplication is unverified, and no exposed female/male MDMA-user denominator accompanies this table. "
            "The surrounding statement must keep the percentages descriptive of selected table rows; neither recount estimates sex-specific susceptibility or age-related risk."
        ))
    elif n==6:
        r.update(verdict='confirmed',note=(
            "The full description is in the first paragraph of Section 5.1.5, right column near the bottom of p. 10; Simmler 2011's bibliography entry is on p. 14. "
            "The review explicitly describes randomized placebo-controlled crossover, eight healthy men and eight healthy women, the stated 125-mg study exposure, baseline/post-administration osmolality, ADH and copeptin measures, and the sex-specific copeptin statement. "
            "Its following 'no significant differences' sentence supplies no named comparison, statistics or interval for ADH or sodium. It does not state a laboratory setting there. "
            "Thus the surrounding statement cannot turn this sentence into demonstrated absence of a sex difference, absence of an MDMA effect or equivalence to placebo; the proposed extraction correctly preserves that ambiguity. "
            "The primary controlled study was not accessed and the exposure is reported solely as a research condition."
        ))
    elif n==7:
        r.update(verdict='confirmed',note=(
            "The approximately 25-times comparison is stated in the long second paragraph of Section 5.1.5, left column of p. 11, beginning 'A previous study showed that when hyponatraemic encephalopathy develops'. "
            "The body passage does not identify the postoperative setting; this is supplied by Ayus 1992's reference title on p. 12, which names postoperative hyponatraemic encephalopathy in menstruant women. "
            "Sections 5.1.5 on pp. 10-11 discuss reproductive-cycle/hormonal physiology in women and rats and a muscle-mass/water-distribution explanation; they do not describe testing those explanations in MDMA users. "
            "The surrounding statement must retain both the postoperative setting and the conditional population with encephalopathy, and must not present this multiplier as an MDMA risk estimate. "
            "Primary reports and experiments were not accessed; only their descriptions and bibliography titles in this review are source-checked."
        ))
    results.append(r)

out=dict(reader='AI reader414 (ChatGPT/OpenAI; fresh isolated context)',date='2026-11-10',
    independence=(
        "Fresh independent review of the frozen proposals. For project context I read only BRIEF.md, tasks_reader414.json, claims_reader414.json and the original named Faria PDF. "
        "I did not read study cards, earlier reader outputs, other project files, plans, logs or calculation ledgers and reused no earlier verdict. "
        "All 52 Table 3 rows were independently transcribed from original 300-dpi rotated PDF renders, and arithmetic was generated solely from that new transcription. No agents were delegated."
    ),
    source_access=(
        "Read the original 14-page Faria review at the supplied local PDF path, checked its full relevant methods, narrative, conclusions and reference entries, extracted its text for navigation, "
        "rendered body pages at 150 dpi and visually checked relevant pages, and rendered/rotated both Table 3 pages at 300 dpi. "
        "No cited primary case report, controlled study, physiology experiment or external web source was opened. "
        "Findings therefore verify review content, internal discrepancies, citation overlap and arithmetic, not primary-report correctness, unique patients or clinical causality."
    ),results=results)
(base/'out_reader414.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')

source_notes=dict(reader=out['reader'],date=out['date'],source=dict(path=str(pdf),sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),pages=14,title='Drinking to death: Hyponatraemia induced by synthetic phenethylamines',journal='Drug and Alcohol Dependence 212 (2020) 108045',doi='10.1016/j.drugalcdep.2020.108045'),
    render_method=dict(body='pdftoppm -r 150 -png (all 14 pages)',tables='pdftoppm -f 5 -l 6 -r 300 -png; rotate each original page clockwise 90 degrees; inspect the rotated page in two overlapping horizontal sections',temporary_directory='/workspace/scratch/d1ee8d93ce58/tmp/pdfs/reader414/'),
    notes=[
        'PDF and printed numbering agree for the cited body/table/reference pages. Page 1 has no printed page number, but is PDF page 1.',
        'Methods p. 2: PubMed search through October 2019, no year restriction, specified phenethylamine/hyponatraemia terms and bibliography searching, 168 publications. Author contribution p. 12 names ACF as mainly responsible for search/data collection. This is review synthesis, not an original 52-person series.',
        'The Table 3 title describes cases involving hyponatraemia; this does not establish numeric hyponatraemia in every table row. Rows 22, 23, 24 have Death outcomes without numeric sodium or a hyponatraemia effect label.',
        'The table has 26 rows on p. 5 and 26 on p. 6. It contains 37 printed sodium numbers in 36 rows because Vakde 2014 has two days in one row. Counting both values as cases would be wrong.',
        'Nine MDMA-labelled rows carry any additional substance label (3, 5, 9, 23, 24, 34, 45, 50, 51). Six carry an additional label other than MDA (3, 5, 9, 23, 24, 34); three list only MDA in addition to MDMA (45, 50, 51). Separately, row 6 is ethcathinone plus methylone. These are labels and not independently verified co-ingestion/toxicology.',
        'The four numeric concentration cells are rows 22-25, all on p. 5. The other 48 concentration cells say Unknown; this is not a record of whether testing occurred.',
        'Ten consecutive Death-labelled rows (11-20) cite Rosenson 2007, nine female and one male. The bibliography title on p. 14 identifies California. Primary matching and any discrepancy with the actual California data are outside this review-only assignment.',
        'Probable duplicate matches: Matthai row 44 / Wilkins row 47 (female 15, sodium 119, Recovery); Matthai row 45 / Wilkins row 46 (female 16, sodium 112, Recovery). Row 45 also lists MDA; row 46 does not. Wilkins p. 14 includes an author reply and a matching topic, but the entry does not literally say letter. Primary content and patient identity are unverified.',
        'Anonymous 2001 entry: p. 12, first reference. Paediatr Child Health 6(7), 491; DOI 10.1093/pch/6.7.491; PMID 20107556; PMCID PMC2807764. The table citation is identifiable within this review.',
        "Chen/Viola p. 13 is a ras-point-mutation methods title; O'Connor p. 14 is a death title despite a blank table outcome; Salathe p. 14 names ecstasy despite methamphetamine in the table. These are review-internal discrepancies only.",
        'Mechanisms: p. 2 lists serotonin/ADH, excessive intake and diaphoresis/sodium-loss pathways; p. 7 labels drinking reports anecdotal and the oedema inference speculative and says mechanisms remain incompletely understood. Page 10 second-hand Henry 1998 description concerns ADH after study exposure. Page 12 conclusion simultaneously describes MDMA mechanisms as relatively well characterized and cautions about animal/human and setting/metabolism extrapolation.',
        'Simmler controlled study is described on p. 10, Section 5.1.5 first paragraph: eight healthy men and eight healthy women, 125 mg as study condition, crossover and placebo-controlled. The contrast for the non-significant ADH/sodium sentence is not specified and laboratory setting is not stated there.',
        'The Ayus 1992 25-times comparison occurs on p. 11 in the encephalopathy-conditional passage; postoperative setting occurs in the p. 12 reference title, not in that body passage.',
        'No ratings, claims or study cards were changed. Results and the supporting new ledger/arithmetic are limited to the assigned directory; temporary extraction/renders are in the allowed reader414 temporary directory.'
    ],verdict_counts=dict(Counter(r['verdict'] for r in results)))
(base/'source_notes_reader414.json').write_text(json.dumps(source_notes,ensure_ascii=False,indent=2)+'\n')
# Reopen the deliverables to check JSON validity, complete result indexing and complete corrections.
loaded=json.loads((base/'out_reader414.json').read_text())
assert [r['n'] for r in loaded['results']]==list(range(1,9))
for r in loaded['results']:
    assert r['verdict'] in {'confirmed','corrected','wrong-location','not-found'}
    if r['verdict']=='corrected':
        assert all(r.get(k) for k in ('corrected_extracted','corrected_page','corrected_locator'))
print(json.dumps({'verdict_counts':source_notes['verdict_counts'],'output_path':str(base/'out_reader414.json')},indent=2))
