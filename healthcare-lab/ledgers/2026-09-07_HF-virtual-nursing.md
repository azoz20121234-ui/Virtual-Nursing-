# Evidence Ledger — Virtual/remote nursing (telemonitoring) & heart-failure readmission
**Investigation date:** 2026-09-07 · **Analyst:** Healthcare Evidence→Innovation Agent
**Question class:** therapy / service-delivery (effectiveness)
**Tools used (verified working this session):** PubMed (search + metadata), ClinicalTrials.gov, WebSearch
**Degraded / unavailable:** Elicit (no API plan), Consensus (quota 30/30), Scite (quota 25/25) → cross-database triangulation NOT available; confidence capped accordingly.
**Access caveat:** all study rows are **abstract-only** (full texts not pulled this session) — findings limited to what abstracts support.

---

- claim_id: C1
  claim: In a SR of transitional-care interventions, telemonitoring did NOT reduce readmission or mortality, whereas home-visiting and multidisciplinary HF clinics did.
  source: Feltner et al., 2014, Annals of Internal Medicine
  identifier: PMID 24862840 · DOI 10.7326/M14-0083
  tier: 1
  study_type: Systematic review + meta-analysis (47 RCTs)
  population: Adults hospitalized with HF, mean age ~70; 47 trials
  intervention: Transitional-care interventions (home visiting, MDS-HF clinics, structured telephone support (STS), telemonitoring, education)
  comparator: Usual care
  outcome: All-cause & HF-specific readmission, mortality (patient-important)
  effect: Home-visiting & MDS-HF clinics ↓ all-cause readmission over 3–6 mo (high SOE) & mortality; STS ↓ HF-specific readmission (high SOE) & mortality; "Neither telemonitoring nor primarily educational interventions reduced readmission or mortality rates."
  confidence: Moderate–High — large SR, high SOE for the positive arms; telemonitoring null is a documented finding, not absence of data.
  limitations: Few trials reported 30-day readmission; usual care heterogeneous; 2013 search (dated). Appraisal: authors graded SOE (GRADE-style).
  contradicts: C2 (partial)
  applicability: Direct to hospitalized HF; comparator "usual care" varies.
  access: abstract-only
  evidence_date: 2014 (search to Oct 2013) — older; newer evidence exists (see C3).
  retrieved: PubMed get_article_metadata ["24862840"]

- claim_id: C2
  claim: Combined remote monitoring + consultation reduced CV-specific mortality and hospitalization in HF, but had NO effect on all-cause mortality or all-cause hospitalization, and benefit was mostly short-term.
  source: Kuan et al., 2022, The Lancet Digital Health
  identifier: PMID 36028290 · DOI 10.1016/S2589-7500(22)00124-8
  tier: 1
  study_type: Systematic review + meta-analysis (72 studies / 127,869; 34 in MA)
  population: Cardiovascular disease incl. HF subgroup
  intervention: Telemedicine — remote monitoring + consultation (and consultation alone)
  comparator: Usual care
  outcome: CV mortality, CV hospitalization, all-cause mortality/hospitalization (patient-important)
  effect: HF: ↓ CV mortality RR 0.83 (95% CI 0.70–0.99, p=0.036); ↓ CV hospitalization RR 0.71 (0.58–0.87, p=0.0002); all-cause hospitalization RR 1.02 (0.94–1.10, ns); all-cause mortality RR 0.90 (0.77–1.06, ns). No benefit from remote consultation in isolation.
  confidence: Low–Moderate — large SR but effects "mostly in studies with short-term follow-up," heterogeneous, CV-specific (not all-cause). Single MA; no triangulation available.
  limitations: Short-term follow-up bias; CV-specific outcomes are narrower than all-cause; composite "telemedicine" pools heterogeneous interventions. Appraisal: Cochrane RoB + Newcastle-Ottawa (per abstract).
  contradicts: C1, C3 (nuance — depends on outcome chosen)
  applicability: Indirect (broad CVD, HF is a subgroup).
  access: abstract-only
  evidence_date: 2022 (search to Jan 2021)
  retrieved: PubMed get_article_metadata ["36028290"]

- claim_id: C3
  claim: In a 2026 network meta-analysis, nurse-led Home Visiting ranked highest for reducing all-cause readmission and mortality; Telemonitoring ranked poorly for readmission prevention (moderate only for mortality).
  source: Dai & Wu, 2026, BMC Cardiovascular Disorders
  identifier: PMID 42141394 · DOI 10.1186/s12872-026-05929-z
  tier: 1
  study_type: Systematic review + frequentist network meta-analysis (19 trials / 11,452)
  population: Hospitalized HF patients
  intervention: 8 transitional-care nodes incl. Telemonitoring (TM), Home Visiting (HV), Multidisciplinary Clinics (MDC), STS, pharmacy, rehab, education
  comparator: Usual care + each other (network)
  outcome: All-cause & HF-specific readmission, all-cause mortality, QoL (patient-important)
  effect: HV only intervention significantly superior to usual care for all-cause readmission RR 0.67 (0.52–0.86), P-score 0.902 (ranked 1st) and highest for mortality; MDC 1st for HF-specific readmission; "TM showed moderate efficacy in mortality reduction but ranked poorly for readmission prevention."
  confidence: Moderate — recent, largest & most current synthesis; network MA adds indirect-comparison assumptions (transitivity) as a caveat.
  limitations: Network MA assumes transitivity/consistency; ranking (P-score) ≠ definitive superiority; 19 trials. Appraisal: not stated in abstract.
  contradicts: C2 (on readmission)
  applicability: Direct to hospitalized HF transition of care.
  access: abstract-only
  evidence_date: 2026 (search to Jan 2025) — most current.
  retrieved: PubMed get_article_metadata ["42141394"]

- claim_id: C4
  claim: A SR of HF systems of care found conflicting evidence on telemonitoring efficacy, while nurse-led clinics and early outpatient follow-up reduced readmissions.
  source: Driscoll et al., 2016, BMC Cardiovascular Disorders
  identifier: PMID 27729027 · DOI 10.1186/s12872-016-0371-7
  tier: 1
  study_type: Systematic review (29 articles)
  population: Diagnosed HF across care settings
  intervention: Systems of care (specialist teams, nurse-led clinics, transitional care, telemonitoring)
  comparator: Usual care / alternative models
  outcome: Readmission, mortality (patient-important)
  effect: Specialist HF teams, nurse-led clinics, early follow-up ↓ readmission/mortality; "There was a lack of evidence as to the efficacy of telemonitoring with many studies finding conflicting evidence."
  confidence: Moderate — consistent with C1/C3 on the human-follow-up signal; narrative SR (no pooled effect).
  limitations: No meta-analysis; 2015 search. Appraisal: Newcastle-Ottawa + GRADE (per abstract).
  contradicts: —
  applicability: Direct.
  access: abstract-only
  evidence_date: 2016
  retrieved: PubMed get_article_metadata ["27729027"]

- claim_id: C5
  claim: TIM-HF2 is a randomised controlled trial of remote patient management vs usual care in HF; its primary outcome is % days lost to unplanned CV hospitalisation or death.
  source: Koehler et al., 2018, European Journal of Heart Failure (STUDY DESIGN / PROTOCOL paper)
  identifier: PMID 30230666 · DOI 10.1002/ejhf.1300 · NCT01878630
  tier: 3
  study_type: Clinical Trial PROTOCOL (design description — NO RESULTS in this record)
  population: HF patients (design)
  intervention: Remote patient management + usual care
  comparator: Usual care only
  outcome: % days lost to unplanned CV hospitalisation or all-cause death (patient-important)
  effect: NOT AVAILABLE — this is the design paper; it reports no results. **Do not state a TIM-HF2 effect from this record.** The results publication was not retrieved this session.
  confidence: n/a — no result to be confident about. Flagged so the brief does not fabricate an outcome.
  limitations: Protocol only. To use TIM-HF2's result, retrieve the results paper (Lancet 2018) — not done here.
  contradicts: —
  applicability: EU population; would need results + Saudi transfer analysis.
  access: abstract-only (protocol)
  evidence_date: 2018 (design)
  retrieved: PubMed get_article_metadata ["30230666"]

- claim_id: C6
  claim: A small pilot RCT of nurse-led collaborative management WITH telemonitoring showed lower rehospitalization vs usual care (20% vs 57.9%; readmission-free survival P=0.020), but was underpowered and QoL-primary.
  source: Mizukawa et al., 2019, International Heart Journal
  identifier: PMID 31735786 · DOI 10.1536/ihj.19-313
  tier: 3
  study_type: RCT (pilot, n=59; 3 arms)
  population: HF patients, Japan; UC n=19, SM n=20, CM n=20
  intervention: Nurse-led collaborative management + telemonitoring (CM)
  comparator: Self-management education (SM); usual care (UC)
  outcome: Primary = QoL (surrogate for this question); Secondary = rehospitalization (patient-important)
  effect: Rehospitalization UC 57.9% vs SM 27.8% vs CM 20.0%; readmission-free survival CM vs UC P=0.020.
  confidence: Low — n=59 pilot, readmission was secondary, single-country; hypothesis-generating.
  limitations: Tiny sample; primary endpoint was QoL not readmission; multiplicity. Appraisal: RoB 2 would flag small n / open design.
  contradicts: supports C3's "human follow-up" reading (the active arm was nurse-led, not device-only).
  applicability: Indirect (Japan, small).
  access: abstract-only
  evidence_date: 2019
  retrieved: PubMed get_article_metadata ["31735786"]

- claim_id: C7
  claim: A home telerehabilitation RCT (remote monitoring + weekly nurse calls + exercise) in older COPD+CHF patients improved exercise tolerance and lengthened time to hospitalisation/death.
  source: Bernocchi et al., 2018, Age and Ageing
  identifier: PMID 28985325 · DOI 10.1093/ageing/afx146
  tier: 3
  study_type: RCT (n=112, multicentre)
  population: Older patients with combined COPD + CHF, Italy
  intervention: Integrated home telerehabilitation (remote monitoring + weekly nurse phone calls + physiotherapist-monitored exercise)
  comparator: Usual care
  outcome: Primary = 6-min walk (surrogate); Secondary = time to hospitalisation/death (patient-important)
  effect: Δ6MWT +60 m (IG) vs −15 m (CG), p=0.0040; median time to hospitalisation/death 113.4 vs 104.7 days, p=0.0484.
  confidence: Low — indirect (telerehab, mixed COPD+CHF), surrogate primary, modest event-time effect.
  limitations: Combined disease population; intervention bundles exercise (not isolatable). 
  contradicts: —
  applicability: Indirect.
  access: abstract-only
  evidence_date: 2018
  retrieved: PubMed get_article_metadata ["28985325"]

- claim_id: C8
  claim: Saudi Arabia's Seha Virtual Hospital delivers HF remote monitoring at national scale, but published Saudi data is descriptive (utilization + satisfaction), NOT comparative effectiveness on readmission/mortality.
  source: Alabdulaali et al., 2025, Telemedicine and e-Health (SEHA Virtual Hospital, MOH)
  identifier: PMID 41081638 · DOI 10.1177/15305627251387590
  tier: 4
  study_type: Retrospective descriptive analysis (EHR/administrative, 2022–2024)
  population: SVH beneficiaries (national), incl. cardiology
  intervention: Virtual hospital services (incl. remote monitoring)
  comparator: None (descriptive)
  outcome: Service volume, case mix, patient satisfaction (NOT readmission/mortality)
  effect: Large growth 2022→2024; outpatient visits 1,717→27,896; satisfaction 82–86%. No comparative clinical outcomes reported.
  confidence: Moderate (for existence/scale) — official MOH-authored; but NO effectiveness inference possible.
  limitations: Descriptive, no comparator, satisfaction ≠ outcome. Cannot be upgraded into an effectiveness claim.
  contradicts: —
  applicability: Saudi-specific CONTEXT (not evidence of effect).
  access: abstract-only
  evidence_date: 2025
  retrieved: PubMed get_article_metadata ["41081638"]; WebSearch (Seha Virtual Hospital, MOH.gov.sa)

- claim_id: C9
  claim: HF telemonitoring / remote monitoring is an active, large research field — 242 registered trials — with ongoing large studies, i.e. the evidence base is still moving.
  source: ClinicalTrials.gov (NIH/NLM registry)
  identifier: 242 trials (query: condition=heart failure, intervention=telemonitoring OR remote patient monitoring). Examples: NCT05653726 (n=390), NCT05960890 (n=1000), NCT06379529 (n=1050)
  tier: 0
  study_type: Trial registry (existence/design data)
  population: Various HF populations
  intervention: Telemonitoring / remote monitoring variants
  comparator: Various
  outcome: Various (existence data, not results)
  effect: n/a — registry count, not an effect. None of these were appraised for results here.
  confidence: High (for the fact that the field is active/unsettled).
  limitations: Registration ≠ completion ≠ positive result; no results extracted.
  contradicts: —
  applicability: Signals the question is not yet settled.
  access: tool result (metadata)
  evidence_date: 2026 (live registry)
  retrieved: Clinical_Trials search_trials (count_total=true)

---
## Ledger notes
- **Central pattern:** across C1, C3, C4 the consistent winners are HUMAN follow-up
  models (home visiting, nurse-led/multidisciplinary clinics), not device-only
  telemonitoring. C2 finds a benefit only for *combined* monitoring+consultation and
  only CV-specific/short-term. C6 (the one nurse-led+TM pilot that "worked") had the
  nurse as the active ingredient. → "Telemonitoring" is a composite label, not one thing.
- **Saudi:** C8 establishes the SYSTEM exists (Seha) but provides NO comparative
  outcome data → the Saudi evidence gap is explicit.
- **Discipline flag:** C5 is a protocol; no TIM-HF2 result is asserted anywhere.
