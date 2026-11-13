# Independent source-read notes — reader412

Date: 2026-11-09. Six frozen proposals checked; six confirmed. No claims, cards or ratings were edited.

## Permitted materials and method

I used only `BRIEF.md`, `tasks_reader412.json`, `claims_reader412.json` and the two original PDFs explicitly named in the tasks for substantive context. No study cards, earlier outputs, calculation ledgers, logs/plans, parent history or outside research were read. The original PDFs were independently extracted with `pdftotext -layout` and rendered with `pdftoppm`. I read the body text and my own 150 dpi page renders across both articles, and inspected relevant tables and figures using 300 dpi renders/crops. Text and page images are under `/workspace/scratch/d1ee8d93ce58/tmp/pdfs/reader412/`; they were not placed in the editorial directory. The Bass PDF emits a recoverable xref warning, but its complete five pages render and the relevant text is clear.

`arithmetic_reader412.py` contains my transcribed inputs and independent formula implementation. Running it regenerates `arithmetic_reader412.json`, which includes the exact source input hashes. The four proposed numerators are unique compatible integers conditional on their stated/assumed denominators and ordinary one-decimal percentage rounding. They are not source-reported raw counts.

## Bass locators and scope

Printed p. 2075 is PDF1. Background paragraphs on p. 2075 are (1) the American solvent-sniffing epidemic, (2) the 1963 glue-sniffing assessment, and (3) the author's 1968 encounter and 1969 survey. Paragraph 3 contains the human-and-animal-experiments basis of the historical low-toxicity description.

The Comment section begins on printed p. 2076 (PDF2). Counting actual indented paragraphs across columns and pages gives:

1. Medical textbooks; continues at the beginning of p. 2078.
2. Volatile hydrocarbons involved in aerosol deaths.
3. Fluorinated refrigerants and low acute-inhalation toxicity in rats/guinea pigs.
4. Added 1,1,1-trichloroethane and prior rat experiments.
5. Uses of liquid trichloroethane.
6. Hall and Hine's earlier cases.
7. Stewart and Andrews' human-toxicology assessment.
8. Press and Done; continues at top right of p. 2078.
9. Speizer and colleagues.
10. Comparison with hydrocarbons used in anaesthesia.
11. Rebreathing in a bag.
12. Prior experimental physiology and suggested mechanism.
13. Exercise/stress, eight eyewitnessed dashes, then uncertainty; starts bottom right p. 2078 and continues top left p. 2079.

This confirms the two Bass locator descriptions. The eight-dash observation is followed immediately by uncertainty among the proposed mechanisms. The author refers back to cases 1-5, so these are overlapping descriptions. The table's ten activity/stress counts sum to 18: `3+2+2+2+2+2+2+1+1+1`. Neither the eight nor the 18 constitutes an unexposed comparison. Historical low-toxicity assessments are reports of prior literature, not findings from the death series and not a safety conclusion for intentional inhalation. I did not extend this targeted adjudication to a new rating or a new complete claim audit.

## Allott locators and scope

Printed p. 168 is PDF1. Results 3.4 begins on p. 171: paragraph 1 covers altered use, paragraph 2 pill-testing frequency (continuing on p. 172), paragraph 3 the prompted Table 4 strategies, paragraph 4 preloading/postloading (continuing across the p. 172 columns), and the final paragraph on p. 173 gives associations. Table 5 is on p. 172; Table 6 is on p. 173.

For the Discussion, paragraph 1 starts below the Results association paragraph on p. 173; paragraph 2 describes representativeness and online interest; paragraph 3 polydrug use; paragraph 4 prompted strategies and unasked frequencies; paragraphs 5-6 risk perception and changed use; paragraphs 7-10 on p. 174 pill testing, pre/postloading frequencies and associations; paragraph 11 animal evidence; paragraph 12 possible beliefs/changed use; paragraph 13 animal extrapolation (continues onto p. 175); paragraph 14 interaction caution. The stated limitations are a subsequent paragraph on p. 175. The locators in task 5 find the intended material. Its Introduction paragraph number is page-local: the paragraph beginning 'Ecstasy users are known' is the second paragraph appearing on p. 169 after a continuation, not paragraph 2 counted from the beginning of the Introduction on p. 168.

Table 6 expressly allows multiple reasons, denominator 55. The first four shares imply compatible counts `25/55=45.4545%`, `18/55=32.7273%`, `12/55=21.8182%`, and `10/55=18.1818%`. The pleasure-related answer is a motive, pooled across preloading/postloading respondents, and cannot be assigned to a product or presented as tested efficacy. Product-source percentages match the p. 172 text but that source-response denominator is not given. The four main sources named in the proposal are not an exhaustive source list; friend (7.5%) is also printed.

The questionnaire and study aims support the qualification about untested harm reduction. The article gives no validation/piloting report and no reference period for the prompted list; that absence is limited to the report, not proof about what investigators ever did. Frequency of prompted strategies was explicitly not asked, while pill testing and pre/postloading frequency were separate questions. The rodent/injection caveat and interaction warning are narrative discussion, not interaction events measured in this sample. Cited primary animal or interaction publications were not accessed.

## Arithmetic

Wilson score interval, without continuity correction, with `z = 1.9599639845400536`, `p=x/n`:

`centre = (p + z²/(2n))/(1 + z²/n)`

`half-width = z*sqrt(p*(1-p)/n + z²/(4n²))/(1 + z²/n)`

| Quantity | Compatible fraction | Reconstructed percent | Wilson 95%, percent | Half-width, percentage points |
| --- | --- | --- | --- | --- |
| Ever preloaded | 48/116 | 41.3793 | 32.8335–50.4778 | 8.8222 |
| Ever postloaded | 55/116 | 47.4138 | 38.5564–56.4370 | 8.9403 |
| Listed 5-HTP before use | 19/46 | 41.3043 | 28.2886–55.6605 | 13.6859 |
| Easing the comedown motive | 25/55 | 45.4545 | 33.0253–58.4773 | 12.7260 |

All proposed one-decimal intervals reproduce. The half-width is half the endpoint separation, not necessarily the same distance on either side of the unadjusted percentage. The whole-sample pre/postloaded numerators use the proposal's explicit assumption of the overall 116 denominator. Subset denominators are different: product lists are 46 before and 54 after; pooled reasons are 55. Conditional arithmetic cannot establish item completeness or eliminate selection bias.

For association checking, compatible reconstructed two-by-two tables have rows high/low lifetime use or monthly-or-more/less frequency and columns yes/no:

| Association | Compatible rows | Pearson chi-square, df 1 | p |
| --- | --- | --- | --- |
| Preloading versus lifetime occasions | (29,24), (19,44) | 7.156804 | 0.007468 |
| Postloading versus lifetime occasions | (32,21), (23,40) | 6.577573 | 0.010327 |
| Postloading versus use frequency | (33,26), (20,35) | 4.381592 | 0.036329 |

These reproduce the printed statistics and rounded percentages: `29/53=54.7%`, `19/63=30.2%`, `32/53=60.4%`, `23/63=36.5%`, `33/59=55.9%`, `20/55=36.4%`. These tables are compatible reconstructions, not raw observations made available by the paper. The age t test cannot be recovered from means alone; its means, df, statistic and p match the printed source.

Methods 2.4 lists ten variables: age, gender, education, years of ecstasy use, use frequency, lifetime occasions, average dose, highest dose, use recency and place of use. Three outcomes are analysed: changed use because of dislikes, preloading and postloading. This yields `10 × 3 = 30` focal comparisons. Results 3.2 also explicitly reports three sex comparisons (highest dose, public use, >50 occasions) and three correlations (age/years, typical/highest dose, highest dose/years); that makes 36 under the full stated focal matrix, before any unreported additional comparisons. The conservative proposed 'at least 30 focal' count is supported. Methods states only significant gender differences are reported, preventing a complete additional-test count. No multiplicity correction is reported; the separate alpha 0.025 normality rule is stated as such.

Results are descriptive or bivariate cross-sectional associations in a self-selected sample. The proposals correctly retain motives as motives, qualifications as qualifications, and the Wilson figures as editorial calculations.
