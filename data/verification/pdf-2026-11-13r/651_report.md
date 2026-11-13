# Reader 651: fentanyl contact, companion papers of 13 November

Cards `sc_chiu_2019` (author manuscript) and `sc_persaud_2020` (online-first PDF), first pass. Patch `651_patch.json`
(dry run passes; not applied); plain lines `651_simple.json`.

## cl_fent_touch, 0.3.2 to 0.4.0

Chiu et al. (2019), anchors 16–19: two incidents NIOSH investigated, five officers. In one, powder later found to
contain fentanyl and methamphetamine blew onto an officer in short sleeves: non-specific symptoms within 5 minutes, no
recorded sign of opioid toxicity, no test. In the other, four officers had symptoms after a hotel-room call; one
improved after naloxone; their urine screens could not detect fentanyl. Neither is the incident of the NIOSH report on
file (other report numbers, officers, containers and laboratory results). Certainty very low, relation and status
unchanged: nothing was measured, and two authors are shared with that report, so it is not independent.

## cl_fent_police_beliefs, 0.2.2 to 0.3.0

Persaud and Jennings (2020), anchors 12–14: 149 of 187 self-selected New York State responders (79.7%) agreed that
briefly touching fentanyl could be deadly (law enforcement 86 of 92; fire or EMS 63 of 95); sources named: courses
78.1%, department training 76.5%, news 13.9%, not linked to the belief. Status now replicated for the share holding the
belief (an independent team); the answers after training still come from one team. Certainty very low.

## Figures corrected

- Anchor 8 (Attaway et al.) and the reasoning carried the survey second-hand: nearly 80% "believed that even briefly
  touching fentanyl could be deadly". The paper reports agreement at unstated levels, and its statement says briefly,
  not even briefly. Anchor 8 reworded, back to ai-located.
- The DEA roll-call video at one justice.gov address is dated 2016 by Attaway et al. (pp. 1, 6) and 6 June 2017 by
  Herman et al. (pp. 112, 114). Both dates are now attributed; new anchor 15.

## Existing cards the new papers correct (not edited)

- `sc_niosh_2018`, timeline: whether its incident is one of Chiu's two can now be told: neither.
- `sc_herman_2020`: Herman's summary of Chiu et al. (one case report, not consistent with opioids, no officer positive
  for opioid metabolites). Chiu et al. report two incidents, suggest milder opioid effects and a substantial opioid
  part for one officer, and used opiate screens that cannot detect fentanyl; one officer had no test.
- `sc_attaway_2021`: the New York survey is no longer unread, and sources of the belief are no longer described only
  qualitatively.

## Reporting issues

- Persaud and Jennings cite the ACMT and AACT statement for chronic harm from regular touching; the statement says no
  persistent effects are expected without prolonged lack of oxygen (its PDF pp. 1, 4).
- Chiu et al. list nausea, which no officer reported; one officer's breathing rate of 9 a minute is not discussed.
- `data/access/pdf-page-basis.json` calls the Persaud PDF an accepted manuscript; it is the typeset online-first
  article, with the same page numbers.

## Still missing

The two NIOSH reports behind Chiu et al.; any measurement of responders' exposure or blood levels; any random-sample
survey of responders. Until the two cards are merged, the validator reports them as unknown (7 hard failures, the only
new ones). Reference records agree with both PDFs.
