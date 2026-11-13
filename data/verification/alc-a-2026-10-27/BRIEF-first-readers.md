# Alcohol, Tier A: first readers (round `alc-a-2026-10-27`)

You are a first reader for Pharmakon, an evidence library about drugs for the public and for people who use drugs.
Project: `/home/claude/drug-encyclopedia`. Scratch folder:
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/` (`scratchpad/` below); your own folder
is `scratchpad/alc-a/r<N>/` (N = your reader number).

The Alcohol page so far answers only questions about the day after drinking and sleep. This round builds its core: is
any amount of drinking good or bad for health (all-cause mortality, the heart, cancer, the liver), how common alcohol use
disorder is, withdrawal, treatment, and drinking in pregnancy. The papers are the Tier A list in
`search-logs/Alcohol_DOI-LIST.md` (read its notes on how the papers answer each other). You write study cards; other
readers write claims from them later and blind second readers check everything.

## Read first

1. `docs/STUDY-CARD-BRIEF.md` in full: it is your procedure. Everything in it applies, with the changes below.
2. `docs/METHODS.md` §4.5, §5 (all of it), §6.2, §9.
3. The exemplar cards named in the brief, and `schema/study-card.schema.json`.

## Changes for this round

- **Folders.** Cards: `data/study-cards/_incoming/alcohol/<card id>.json`. Reference lines: append to
  `data/references/_incoming/alcohol.txt` (`reference_id>DOI>where-read`, e.g. `ronksley_2011>10.1136/bmj.d671>PMC3043109`).
  Check existing reference ids first (the brief gives the command); none of your papers has one yet.
- **Browser.** The tools are the app's built-in browser on the senior author's computer: load them in one call,
  `ToolSearch` with query `mcp__remote-devices__Claude_Browser__` and `max_results` 64. Open your own tab with
  `preview_start` at the paper's URL and pass its tabId on every call; one page load at a time. Never touch any other
  tab (one belongs to the senior author; others to other readers). Never open a PDF or download link, never interact
  with a check page. Close your tab when you finish. For Wiley use `https://onlinelibrary.wiley.com/doi/full/<DOI>`.
  If the browser cannot be reached, stop and say so in your final message.
- **Corrections.** Wood et al. (2018) and Bryazka et al. (2022) have published errata (the list says "obtain both").
  For these, and for any paper whose PMC page or publisher page links a correction, read the notice too (it is usually a
  linked page on PMC or the publisher's site), say on the card what it changed and whether the numbers you extract are
  the corrected ones, and give the notice's DOI in your final message so the editor can build its record.
- **Designs and instruments** (METHODS §5.3; where the protocol is silent, follow these and say why on the card):
  - Global Burden of Disease and other attributable-burden estimates (Griswold 2018, Bryazka 2022, Rumgay 2021):
    design `modelling`, no instrument; the card states the design's limits: the inputs and where they come from, the
    relative-risk curves and the theoretical-minimum (counterfactual) level used, what the uncertainty intervals do and
    do not include, and the sensitivity of the headline result to these choices.
  - Pooled individual-participant analyses of cohorts without a systematic search (for example Wood 2018): design
    `prospective-cohort`, ROBINS-E, with `design_detail` saying it is a pooled analysis and how the cohorts were chosen.
  - Mendelian randomization (Holmes 2014, Millwood 2019, Biddinger 2022, Larsson 2020): design by the data the analysis
    uses (`prospective-cohort` for one cohort or pooled cohorts; `case-control` when the outcome associations come from
    case-control genome-wide studies), `design_detail` beginning "Mendelian randomization"; appraise with ROBINS-E and
    judge, inside its domains, the three instrument assumptions: relevance (instrument strength, F statistics), no
    confounding of the instrument (population stratification, ancestry), and no other path from the variants to the
    outcome (pleiotropy, and the sensitivity analyses that test it); also whether the analysis can show the shape of a
    curve at low intake, and selection into the cohort. Where the paper also reports conventional (non-genetic)
    associations, extract both and keep them apart.
  - Commentaries, debate pieces and narrative reviews (Burton & Sheron 2018, Chikritzhs 2015): design `narrative-review`,
    the editors' checklist (STUDY-CARD-BRIEF names its five domains and the model card).
  - Systematic reviews and meta-analyses, including Cochrane reviews and prevalence meta-analyses: AMSTAR 2. For a
    review that is partly narrative (Roerecke & Rehm 2014), appraise its systematic part and say so.
  - National surveys of prevalence (Grant 2015, Grant 2017): design `cross-sectional`, JBI prevalence checklist.
- **Debates.** Several of your papers are landmarks with published critiques or replies (the J-curve, abstainer bias,
  "no safe level", genetic evidence). In each card's `replication.timeline`, name the critiques, replies and corrections
  you find (the paper's own discussion, the list's notes, linked letters); use a reference id only if it exists in
  `data/references/*.json`. Appraise every paper on its own methods: neither the "moderate drinking is healthy" reading
  nor the "any drinking is harmful" reading gets the benefit of the doubt. Note who funded each study and any industry
  ties exactly as printed.
- **Exposure units.** Studies define a "drink" and "moderate" differently (grams of ethanol, standard drinks, national
  units). Record each paper's definition and its reference group (lifetime abstainers, current non-drinkers including
  former drinkers, or occasional drinkers) with every estimate: claims will depend on it.
- No dosing advice of any kind; withdrawal and treatment studies report regimens only as what the study gave.

## Your papers

| Reader | Papers (DOI; where to read) |
|---|---|
| 154 | Griswold et al. (2018), GBD 2016 alcohol (10.1016/S0140-6736(18)31310-2; PMC6148333) · Burton & Sheron (2018), comment (10.1016/S0140-6736(18)31571-X; https://doi.org/10.1016/S0140-6736(18)31571-X) · Bryazka et al. (2022), GBD 2020 alcohol, with its erratum (10.1016/S0140-6736(22)00847-9; PMC9289789) |
| 155 | Wood et al. (2018), with its erratum (10.1016/S0140-6736(18)30134-X; PMC5899998) · Stockwell et al. (2016) (10.15288/jsad.2016.77.185; PMC4803651) · Zhao et al. (2023) (10.1001/jamanetworkopen.2023.6185; PMC10066463) · Chikritzhs et al. (2015) (10.1111/add.12828; Wiley) |
| 156 | Ronksley et al. (2011) (10.1136/bmj.d671; PMC3043109) · Roerecke & Rehm (2012) (10.1111/j.1360-0443.2012.03780.x; PMC3348338) · Roerecke & Rehm (2014) (10.1186/s12916-014-0182-6; PMC4203905) |
| 157 | Holmes et al. (2014) (10.1136/bmj.g4164; PMC4091648) · Millwood et al. (2019) (10.1016/S0140-6736(18)31772-0; PMC6497989) · Biddinger et al. (2022) (10.1001/jamanetworkopen.2022.3849; PMC8956974) · Larsson et al. (2020) (10.1161/CIRCGEN.119.002814; PMC7299220) |
| 158 | Bagnardi et al. (2015) (10.1038/bjc.2014.579; PMC4453639) · Rumgay et al. (2021) (10.1016/S1470-2045(21)00279-5; PMC8324483) · Roerecke et al. (2019) (10.14309/ajg.0000000000000340; PMC6776700) |
| 159 | Grant et al. (2015) (10.1001/jamapsychiatry.2015.0584; PMC5240584) · Grant et al. (2017) (10.1001/jamapsychiatry.2017.2161; PMC5710229) · Popova et al. (2017) (10.1016/S2214-109X(17)30021-9; https://doi.org/10.1016/S2214-109X(17)30021-9) · Lange et al. (2017) (10.1001/jamapediatrics.2017.1919; PMC5710622) |
| 160 | Amato et al. (2010), Cochrane, benzodiazepines for alcohol withdrawal (10.1002/14651858.CD005063.pub3; PMC12414628) · McPheeters et al. (2023) (10.1001/jama.2023.19761; PMC10630900) |
| 161 | Rösner et al. (2010), Cochrane, opioid antagonists (10.1002/14651858.CD001867.pub3; PMC13590218) · Rösner et al. (2010), Cochrane, acamprosate (10.1002/14651858.CD004332.pub2; PMC12147086) |

PMC pages are `https://pmc.ncbi.nlm.nih.gov/articles/<PMCID>/`. If a PMC page holds a different version or edition
than the DOI (Cochrane reviews are updated), say which version you read and whether its DOI matches the one above.

## Final message

Under 200 words: each card written (or "not readable" and why); for each, two lines on what the full text changed
compared with the abstract; correction notices read (DOI); anything the claim writers must know.
