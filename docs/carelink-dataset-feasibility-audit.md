# CareLink — Dataset Feasibility Audit (Phase 0)

**Scope of this document.** This is a *feasibility audit only*. It determines whether publicly
documented, research-approved clinical datasets can support retrospective testing of mechanisms
M1–M8. It does not analyse CareLink as a product, does not attempt to demonstrate that CareLink is
effective, and contains no results. No statistical analysis has been performed and none should be
performed on the basis of this document alone.

**Date of audit:** 2026-09-01
**Datasets audited:** MIMIC-IV (hosp/icu), MIMIC-IV-Note, MIMIC-IV-ED, eICU-CRD v2.0
**Auditor stance:** adversarial. Every claim of availability must be traceable to authoritative
documentation. Clinical plausibility is not evidence of availability.

### Evidence-level notation used throughout

| Tag | Meaning |
|---|---|
| **[DOC]** | **Documented fact.** Stated explicitly in official dataset documentation or the peer-reviewed dataset paper. Source cited. |
| **[INF]** | **Researcher inference.** A conclusion drawn from documented facts. Logically derived, not stated verbatim in the source. |
| **[PROP]** | **Proposed analytic approach.** A design suggestion. Not a fact about the data. |
| **[VERIFY]** | **Uncertain — requires verification** against the actual schema/data before use. |

### Availability notation

`DIRECTLY AVAILABLE` · `PROXY AVAILABLE` · `NOT AVAILABLE` · `UNCERTAIN — REQUIRES VERIFICATION`

A proxy is never reported as a direct measurement. `PARTIAL` is never upgraded to `YES`.

---

## 1. Executive Feasibility Verdict

**Headline: the datasets can support a *risk-prediction and discharge-destination* study at T0. They
cannot support a study of the CareLink transition-care mechanisms themselves.**

Five findings drive every downstream conclusion:

1. **eICU cannot measure 30-day readmission — at all.** The official eICU documentation states:
   *"There is no systematic method for chronologically ordering `patientHealthSystemStayID` for the
   same patient within the same year."* **[DOC]** Combined with the fact that calendar dates were
   removed under HIPAA Safe Harbor and only `hospitalDischargeYear` (year granularity) survives
   **[DOC]**, the elapsed time between two hospitalisations for the same patient is not computable.
   eICU therefore **cannot serve as an external replication dataset for any readmission-window or
   post-discharge time-to-event outcome**. This is not a data-quality caveat; it is a structural
   impossibility.

2. **MIMIC-IV can measure 30-day readmission, but only *observed* readmission at one hospital.**
   MIMIC-IV is sourced from a single centre (Beth Israel Deaconess Medical Center) **[DOC]**. Absence
   of a subsequent `hadm_id` means "no readmission observed at BIDMC", not "no readmission occurred".
   Every outcome in this design is a *left-truncated, institution-bounded observation*, and must be
   reported as such (see §10).

3. **The core M1 constructs do not exist in either dataset in the required form.** Functional status,
   cognition, mobility, ADL capability and "discharge readiness" have no hospital-wide structured
   representation in MIMIC-IV. Ward vital signs are not in MIMIC-IV at all — `chartevents` is sourced
   from the ICU clinical information system and covers ICU stays only **[DOC]**. For a
   general-medicine patient discharged from a ward, there are *no charted vital signs near T0*.

4. **The M4 intervention content was deliberately deleted.** The MIMIC-IV dataset paper states that
   *"As a part of the deidentification process, the Social History and Discharge Instructions sections
   have been removed"* from discharge summaries **[DOC]**. The single richest source of discharge
   instructions and social/caregiver context is, by design, absent.

5. **M5 and M6 have no data at all.** There is no outpatient-visit table, no primary-care encounter,
   no home-health encounter, no telephone encounter and no post-discharge physiologic monitoring in
   either dataset. **Not directly testable in this dataset.**

### Decision

| | Verdict |
|---|---|
| **MIMIC-IV** | **PRIMARY DATASET** — for T0-side prediction and discharge-destination questions only. |
| **eICU-CRD** | **NOT SUITABLE** as an external replication dataset for the post-discharge outcome design. Retained only as a **SECONDARY DATASET** for pre-T0 construct availability (functional/ADL/care-plan documentation) and in-hospital outcomes. |

| Mechanism | Level | One-line basis |
|---|---|---|
| M1 Structured reassessment | **LEVEL C** | Functional/cognitive/mobility/ADL/readiness absent; ward vitals absent. |
| M2 Patient selection | **LEVEL B** | T0 features rich; outcome is an institution-bounded proxy. |
| M3 Level-of-care selection | **LEVEL B** | Destination is direct; the dominant confounder (function) is unmeasured. |
| M4 Coordinated transition | **LEVEL C** | Discharge instructions deleted; bundle not measurable. |
| M5 Post-discharge follow-up | **LEVEL C** | No outpatient/home-health/telephone encounter data. |
| M6 Remote monitoring | **LEVEL C** | No post-discharge monitoring exists. Not directly testable. |
| M7 Escalation pathway | **LEVEL C** (mechanism) / **LEVEL B** (retrospective detectability only) | No pathway exists to evaluate. |
| M8 Safety / failure modes | **LEVEL C** (**LEVEL B** for the utilisation sub-domain only) | Most failure modes unobservable; no present-on-admission flag. |

**Stop condition invoked for M1, M4, M5, M6, M7, M8: DO NOT TEST YET.**

---

## 2. Dataset Eligibility Audit

| Criterion | MIMIC-IV (+ED, +Note) | eICU-CRD v2.0 |
|---|---|---|
| **Adult patients** | **YES** — patients under 18 at first visit were excluded **[DOC]**; neonates removed in v2.0 **[DOC]**. | **YES** — adult ICU population; ages >89 collapsed to `"> 89"` **[DOC]**. |
| **Acute discharge** | **YES** — `admissions` is the ADT record of every hospitalisation, with `admittime`/`dischtime` **[DOC]**. Note the cohort universe is patients admitted to the **ED or an ICU** 2008–2019 **[DOC]**, not all hospital admissions. | **PARTIAL** — the unit of observation is the ICU/step-down stay; hospital admit/discharge are represented only as offsets from ICU admission **[DOC]**. Patients with only step-down/low-acuity stays were removed **[DOC]**. |
| **Discharge data** | **YES** — `discharge_location` with a documented value set mapped to UB-04 codes (HOME, SKILLED NURSING FACILITY, REHAB, HOME HEALTH CARE, HOSPICE, CHRONIC/LONG TERM ACUTE CARE, ASSISTED LIVING, ACUTE HOSPITAL, AGAINST ADVICE, DIED, PSYCH FACILITY, HEALTHCARE FACILITY, OTHER FACILITY) **[DOC]**. | **PARTIAL** — `hospitalDischargeLocation` is a structured list ("Home, Nursing Home, Death, etc.") **[DOC]**, but the full value set is not published in the documentation **[VERIFY]**. |
| **30-day outcome** | **PARTIAL** — computable at BIDMC only. Date shifting uses a **patient-level offset that preserves intervals** **[DOC]**, so within-patient interval arithmetic is valid. Cross-institution readmission is unobservable **[INF]**. | **NO** — no chronological ordering of hospitalisations for the same patient; dates removed **[DOC]**. |
| **90-day outcome** | **PARTIAL** — same mechanics and same institutional bound as 30-day. | **NO** — same reason. |
| **Medication** | **YES** — `prescriptions`, `pharmacy`, `emar`, `emar_detail` **[DOC]**; pre-admission list in MIMIC-IV-ED `medrecon` **[DOC]**. Caveat: eMAR was deployed 2014–2016 and full coverage is only expected from 2016 onward **[DOC]**. | **PARTIAL** — `medication` (verified orders, not administrations) and `infusionDrug` (continuous infusions only, present in 152/208 hospitals = 73%) **[DOC]**. `admissionDrug` is documented as *"Extremely infrequently used"* **[DOC]**. |
| **Functional data** | **NO** (hospital-wide). ICU-only bedside documentation exists in `chartevents` **[DOC]**; whether specific functional/mobility items exist is **UNCERTAIN — REQUIRES VERIFICATION** against `d_items`. | **PARTIAL** — `nurseCare` documents *Activity* and *Hygiene/ADLs* categories **[DOC]**; `nurseAssessment` documents Braden Scale including an *Activity* subscale **[DOC]**. ICU-level only; completion varies by hospital **[DOC]**. |
| **Cognitive data** | **PARTIAL** — `chartevents` is documented to contain Glasgow Coma Scale and Richmond Agitation-Sedation Scale **[DOC]**. ICU only. No delirium/cognition instrument documented for wards. | **PARTIAL** — GCS components (`verbal`, `motor`, `eyes`) in `apachePredVar` **[DOC]**, taken from the *worst* GCS set — a severity variable, not a discharge-time cognition measure **[INF]**. |
| **Social / caregiver data** | **NO** — `marital_status`, `insurance`, `language` exist in `admissions` **[DOC]** but are demographics, not caregiver capacity. The Social History section of discharge summaries was **removed** **[DOC]**. | **PARTIAL** — `carePlanGeneral` documents *Family/Health Care Proxy/Contact Info*, *End of Life Discussion*, *Psychosocial Status*, *Baseline Status* **[DOC]**. Structured picklists, ICU-scoped, completeness unknown **[VERIFY]**. |
| **Monitoring data** | **PARTIAL (in-hospital ICU only)** — `chartevents`, `procedureevents` **[DOC]**. **NO** post-discharge monitoring. | **PARTIAL (in-hospital ICU only)** — `vitalPeriodic` (5-minute medians from bedside monitors) and `vitalAperiodic` **[DOC]**. **NO** post-discharge monitoring. |
| **Escalation data** | **NO** — no escalation pathway, alert, or response record exists. Rapid-response/MET events are not a documented table **[VERIFY]**. Subsequent ED/ICU/readmission *events* are observable **[DOC]**. | **NO** — eICU is itself a tele-ICU alerting programme, but the alert/response record is not in the released schema **[INF]**; `carePlanGeneral` acuity flags exist **[DOC]** but are not an escalation pathway. |
| **Access** | **PARTIAL** — credentialed PhysioNet access, CITI training and a DUA are required **[DOC]**. **Not obtainable in this environment** (see §11). | **PARTIAL** — identical requirements: CITI "Data or Specimens Only Research" course + PhysioNet credentialed application + DUA **[DOC]**. **Not obtainable in this environment.** |
| **Main limitation** | Single centre; no post-discharge care observable; discharge instructions and social history deleted; ward vitals absent. | Hospitalisations cannot be ordered in time ⇒ **no post-discharge outcome of any kind**. |

---

## 3. MIMIC-IV Schema Audit (hosp / icu / ed)

Version note: the official MIMIC documentation site states *"The latest version of MIMIC-IV is
v2.2"* **[DOC]**, and the OMR/`poe_detail` value tables in that documentation are explicitly
"as of MIMIC-IV v2.2". However, the MIMIC Code Repository — updated far more recently — refers to
release-specific derived datasets such as `physionet-data.mimiciv_3_1_derived` on BigQuery **[DOC]**,
confirming that **v3.1 is a current release and the documentation site is stale on version
numbering**. **Row counts, value sets and `itemid` assignments in this audit are anchored to v2.2 and
must be re-verified against whichever version is actually used. [VERIFY]** In particular, `itemid`
values for laboratory measurements are known to have changed between releases; any analysis must pin
an exact version.

### Structure **[DOC]**

- Modules: `hosp` (hospital-wide EHR), `icu` (MetaVision bedside), `ed` (MIMIC-IV-ED), `note`
  (MIMIC-IV-Note), `cxr`.
- `subject_id` = patient; `hadm_id` = one hospitalisation; `stay_id` = one ICU or ED stay.
- **Rows without an `hadm_id` pertain to data collected outside an inpatient encounter** — this is
  the single most useful and most dangerous fact in the schema (see §7 and §13).
- Dates are shifted by a **patient-level offset**; intervals within a patient are preserved.
- `subject_id` cannot be linked to MIMIC-III.

### Key tables

| Table | Fields relevant to this design | Timing | Notes |
|---|---|---|---|
| `hosp.patients` | `subject_id, gender, anchor_age, anchor_year, anchor_year_group, dod` | lifetime | `dod` from hospital records **and** the Massachusetts State Registry of Vital Records; **out-of-hospital mortality available up to one year post-discharge; deaths beyond one year are censored** **[DOC]**. |
| `hosp.admissions` | `hadm_id, admittime, dischtime, deathtime, admission_type, admission_location, discharge_location, insurance, language, marital_status, race, edregtime, edouttime, hospital_expire_flag` | admission→discharge | `deathtime` present only for in-hospital death **[DOC]**. Organ-donor accounts create short/negative-LOS admissions that must be excluded **[DOC]**. |
| `hosp.transfers` | `transfer_id, eventtype ('ed','admit','transfer','discharge'), careunit, intime, outtime` | continuous | ED stays appear here even without admission **[DOC]**. |
| `hosp.diagnoses_icd` | `seq_num, icd_code, icd_version` | **post-discharge coding** | Assigned by coders *after reviewing signed notes* **[DOC]**. **No present-on-admission flag exists in the schema** — complications cannot be separated from comorbidities **[DOC, by absence]**. Max 39 codes; `seq_num` is not a reliable importance ranking **[DOC]**. |
| `hosp.procedures_icd` | `chartdate, icd_code, icd_version` | dated | Usable for procedure-based planned-readmission logic **[PROP]**. |
| `hosp.drgcodes` | `drg_type, drg_code, drg_severity, drg_mortality` | post-discharge | Billing artefact; **not available at T0** **[INF]**. |
| `hosp.labevents` | `charttime, storetime, valuenum, ref_range_lower/upper, flag, priority, comments` | continuous, incl. outpatient | Reference ranges present ⇒ abnormality is computable without hand-coded thresholds **[DOC]**. `hadm_id` is assigned by proximity via `transfers` and does not perfectly capture stay boundaries **[DOC]**. |
| `hosp.microbiologyevents` | specimen/organism/antibiotic/dilution | continuous | Only the final interpretation is stored; interim results are not **[DOC]**. |
| `hosp.prescriptions` | `starttime, stoptime, drug, gsn, ndc, dose_val_rx, route, doses_per_24_hrs` | order-time | Prescriptions, **not** administrations; start time is not guaranteed to be first administration **[DOC]**. |
| `hosp.pharmacy` | `status, entertime, verifiedtime, frequency, duration, dispensation, fill_quantity` | order-time | |
| `hosp.emar` / `emar_detail` | `charttime, medication, event_txt, scheduletime` | administration | Barcode-verified administration **[DOC]**. Coverage incomplete before 2016 **[DOC]**. ~713k rows (2.5%) fall **outside** the administrative admit/discharge window **[DOC]** — a leakage hazard. |
| `hosp.poe` | `ordertime, order_type, order_subtype, transaction_type, order_status` | order-time | `order_type` includes *Consults*, *Nutrition*, *Hemodialysis*, *ADT orders* **[DOC]**. |
| `hosp.poe_detail` | `field_name, field_value` | order-time | Documented `field_name` values include **`Discharge Planning`** (475,428 rows; most frequent value *"Finalized"*), **`Discharge When`** (431,642 rows; *"Discharge Now"*), `Code status` (197,932; *"Resuscitate (Full code)"*), `Consult Status`, `Level of Urgency`, `Admit to`, `Transfer to` **[DOC]**. This is the only *structured* discharge-planning signal in MIMIC-IV. |
| `hosp.omr` | `chartdate, seq_num, result_name, result_value` | **inpatient and outpatient** | Documented `result_name` values: Blood Pressure (2,169,549), Weight (Lbs) (1,889,542), BMI (kg/m2) (1,662,112), Height (Inches) (706,906), orthostatic BP variants, eGFR (240) **[DOC]**. Baseline pre-hospitalisation values often available **[DOC]**. |
| `hosp.services` | `transfertime, prev_service, curr_service` | continuous | Documented service abbreviations (MED, CMED, SURG, NMED, …) **[DOC]**. |
| `icu.icustays` | `stay_id, first_careunit, last_careunit, intime, outtime, los` | ICU only | Stays within 24 h are merged into one `stay_id` **[DOC]**. |
| `icu.chartevents` | `charttime, storetime, itemid, value, valuenum, warning` | **ICU only** | *"acts as a catch-all for documentation at the bedside"* **[DOC]**; documented to include GCS, RASS and Code Status **[DOC]**. The MetaVision **problem list** was added in v2.0 under `itemid` 220001, mostly documented at nurse shift change **[DOC]**. |
| `icu.procedureevents` | `starttime, endtime, itemid, location, statusdescription` | ICU only | Organ-support treatments incl. mechanical ventilation **[DOC]**. |
| `ed.edstays` | `stay_id, intime, outtime, arrival_transport, disposition, hadm_id` | ED | **425,087 rows.** `hadm_id` NULL ⇒ the patient was **not** admitted **[DOC]**. Documented dispositions: HOME (241,632), ADMITTED (158,010), TRANSFER (7,025), ELOPED (5,710), LEFT WITHOUT BEING SEEN (6,155), LEFT AGAINST MEDICAL ADVICE (1,881), OTHER (4,297), EXPIRED (377) **[DOC]**. |
| `ed.triage` | `temperature, heartrate, resprate, o2sat, sbp, dbp, pain, acuity, chiefcomplaint` | ED arrival | All fields were originally free text; deidentification introduced NULLs, and **missing values cannot be distinguished from deidentified values** **[DOC]**. |
| `ed.vitalsign` | serial ED vitals incl. `rhythm`, `pain` | ED | Same missingness caveat **[DOC]**. |
| `ed.medrecon` | `name, gsn, ndc, etccode, etcdescription` | ED arrival | **2,987,342 rows.** Medicines the patient reports taking on arrival **[DOC]**. |
| `ed.diagnosis` | `seq_num, icd_code, icd_title` | ED | |
| `ed.pyxis` | `charttime, name, gsn` | ED | Dispensing records. |

**Coverage discontinuity — RESOLVED, and it constrains the cohort.** The MIMIC Code Repository README
states the coverage windows explicitly **[DOC]**:

- MIMIC-IV — *"hospital and critical care data for patients admitted to the ED or ICU between
  **2008 - 2019**"*
- MIMIC-IV-ED — *"emergency department data for individuals attending the ED between **2011 - 2019**"*

**[INF] Consequence:** MIMIC-IV-ED is the *only* source of non-admitted ED visits, so for index
discharges occurring in **2008–2010 the post-discharge ED-visit outcome is undefined, not negative**.
Treating those index stays as "no ED visit" would fabricate three years of false negatives.
**Any cohort must be restricted to index discharges from 2011 onward whenever an ED-visit outcome (or
an acute-care-utilisation composite containing one) is used.** Because dates are patient-shifted, this
restriction must be applied via `anchor_year_group` rather than raw `dischtime` **[PROP]**, and the
resulting loss of index stays should be reported in the cohort flow diagram.

---

## 4. MIMIC-IV-Note Audit

**Contents [DOC]:** four tables only — `discharge`, `discharge_detail`, `radiology`,
`radiology_detail`. Linked to MIMIC-IV by `subject_id` / `hadm_id`.

`discharge`: `note_id, subject_id, hadm_id, note_type ('DS' | 'AD' addendum), note_seq, charttime,
storetime, text`. `discharge_detail` is an entity-attribute-value table whose documented
`field_name` is `author`.

**What is present [DOC]:** discharge summaries organised into sections including chief complaint,
history of present illness, past medical history, brief hospital course, physical exams and discharge
diagnoses; radiology reports with indication/comparison/findings/impression sections.

**What is absent — decisive for this project:**

1. **Discharge Instructions section: REMOVED.** *"As a part of the deidentification process, the
   Social History and Discharge Instructions sections have been removed. These sections typically
   contained social and logistical information which was irrelevant for medical care but introduced a
   higher risk of reidentification."* **[DOC]** ⇒ Domain W (discharge instructions) is **NOT
   AVAILABLE**, and the primary narrative source of social/caregiver context is **NOT AVAILABLE**.
   *Note: the MIMIC website's one-line description of the `discharge` table still says summaries
   describe "any relevant discharge instructions". The peer-reviewed dataset paper is the more
   specific and more recent statement about the deidentification pipeline and is taken as
   authoritative here; the discrepancy should be resolved empirically on the actual release before
   any note-based work.* **[VERIFY]**
2. **Nursing notes: NOT PRESENT.** The note module contains discharge summaries and radiology reports
   only **[DOC]**. Unlike MIMIC-III's `NOTEEVENTS`, there is no nursing-note or progress-note table.
   ⇒ Domain O (nursing documentation) is **NOT AVAILABLE in MIMIC-IV** as free text.
3. **Physician progress notes, consult notes, therapy (PT/OT) notes: NOT PRESENT** **[DOC, by
   absence]**. PT/OT evaluations are the usual EHR home for functional and mobility assessment; their
   absence is why M1 fails.

**Timing hazard [INF]:** a discharge summary is authored at or after the discharge decision and
narrates the entire hospitalisation and the disposition. It is a **post-T0 artefact for most
purposes**. `storetime` (when the note was completed and signed) **[DOC]** is the only defensible
timestamp for a T0 availability filter, and even a note signed before `dischtime` narrates the whole
stay. Treat note text as a T0 feature only with an explicit, pre-registered justification.

**Legitimate uses that remain [PROP]:** presence/absence and timing of a discharge summary as a
process measure; extraction of a discharge-medication list *if* such a section survives
deidentification (**[VERIFY]** — not confirmed); extraction of documented unresolved issues from the
"brief hospital course" section (a proxy, never a direct measure).

---

## 5. eICU Schema Audit

**Scale [DOC]:** 200,859 unit encounters, 139,367 unique patients, 335 units, 208 hospitals,
admitted 2014–2015.

**Sampling [DOC]:** all hospital discharges 2014–2015 were identified; one index stay per unique
patient was extracted; a stratified sample by hospital was drawn; *"After a patient index stay was
selected, all subsequent stays for that patient were also included in the dataset, regardless of the
admitting hospital."* Patients with only step-down/low-acuity stays were removed.

**The temporal structure — and why it ends the readmission question [DOC]:**

- All stays are centred on ICU admission; there is no `unitAdmitOffset` (it is 0 for all stays).
- Timing within a hospitalisation is fully recoverable: `hospitalAdmitOffset`, `unitDischargeOffset`,
  `hospitalDischargeOffset` are minutes relative to unit admission, and the documentation gives a
  worked example computing hospital LOS from them.
- Calendar dates were removed as PHI. What survives is `hospitalDischargeYear` (year),
  `hospitalAdmitTime24` / `unitAdmitTime24` / `hospitalDischargeTime24` / `unitDischargeTime24`
  (clock time of day only).
- **"There is no systematic method for chronologically ordering `patientHealthSystemStayID` for the
  same patient within the same year."**

⇒ **[INF, forced by the above]** For a patient with two hospitalisations, eICU cannot determine which
came first (within a year), nor the number of days between them. **30-day readmission, 90-day
readmission, time-to-event, and any post-discharge window are not constructible.** `unitVisitNumber`
and `unitStayType` ('readmit') describe *ICU readmission within one hospitalisation*
**[DOC]** — conflating that with 30-day hospital readmission would be a category error.
`apachePredVar.readmit` likewise is an APACHE severity covariate ("Indicates if the Patient was
readmitted") **[DOC]**, not a post-discharge outcome.

**Where eICU is unexpectedly strong [DOC]:**

| Table | Content of interest |
|---|---|
| `carePlanGeneral` | `cplGroup` values documented to include *Activity*, *Critical Care Discharge/Transfer Planning*, *Daily Goals/Safety Risks/Discharge Requirements*, *Safety/Restraints*, *Acuity*. Carries **`activeUponDischarge` (True/False)** — an explicit at-discharge flag. Documented care-plan content includes Code Status, Care Limitation, and a Patient-Family group covering *Baseline Status, Family/Health Care Proxy/Contact Info, End of Life Discussion, Psychosocial Status*, and whether the *Care Plan [was] Reviewed with Patient/Family*. |
| `nurseCare` | Documented categories: Nutrition, Activity, **Hygiene/ADLs**, Respiratory, Incision/Wound Care, Line Care, Drain/Tube Care, Safety, Alarms, Isolation Precautions, Equipment, Restraints. |
| `nurseAssessment` | Pain, psychosocial status, patient/family education, organ-system assessments; documented example path `…|Nursing Assessment|Scores|Braden Scale|Activity`. |
| `physicalExam` | Structured exam picklists. **Free-text sections are not included** **[DOC]**. |
| `pastHistory` | Comorbid history; documented as unreliably completed except for severity-scoring items (AIDS, cirrhosis, hepatic failure, chronic renal failure, transplant, cancer, immunosuppression). |
| `lab`, `vitalPeriodic`, `vitalAperiodic`, `respiratoryCharting`, `intakeOutput`, `treatment`, `diagnosis`, `microLab`, `medication`, `infusionDrug`, `allergy`, `apacheApsVar`, `apachePatientResult` | Physiology, therapy and severity. |

**Where eICU is weak [DOC]:**

- **No free text.** *"Any notes or section of notes which are primarily narrative text format have
  been removed."* Free-text instructions and comments in `medication` are also removed.
- **Hospital-level heterogeneity is documented, not hypothetical:** *"the reliability and completion
  of data elements varies on a hospital and/or ICU level"*; `infusionDrug` is populated for 152/208
  hospitals; `microLab` *"is not populated for a significant number of hospitals"*; `customLab`
  covers <1% of patients; 12.5% of hospitals have unknown region and 20.1% unknown bed capacity.
- **No post-discharge vital status.** `hospitalDischargeStatus` is Alive/Expired at hospital
  discharge only. There is no date of death and no out-of-hospital mortality.
- **Hospital identity removed**, so no linkage to external hospital characteristics beyond the
  three-column `hospital` table (bed-count category, teaching status, region).

---

## 6. Variable Availability Matrix (Domains A–AF)

Classification is per dataset. "Timing" states availability relative to T0 = discharge decision.

| # | Domain | MIMIC-IV | Table / field | Timing | Class | Notes |
|---|---|---|---|---|---|---|
| A | Admissions / encounters | ✔ | `hosp.admissions`, `hosp.transfers` | pre-T0 | **DIRECT** | Full ADT record **[DOC]**. |
| B | Discharge information | ✔ | `admissions.dischtime`, `.discharge_location` | **at T0** | **DIRECT** | UB-04-mapped value set **[DOC]**. |
| C | Diagnoses | ✔ | `diagnoses_icd`, `ed.diagnosis` | **post-T0 for billing codes** | **DIRECT but mistimed** | Coded after review of signed notes **[DOC]** ⇒ leakage if used as a T0 feature. |
| D | Procedures | ✔ | `procedures_icd` (`chartdate`), `icu.procedureevents` | dated | **DIRECT** | |
| E | Medications | ✔ | `prescriptions`, `pharmacy`, `emar`, `ed.medrecon` | pre-T0 | **DIRECT** | eMAR incomplete before 2016 **[DOC]**. |
| F | Laboratory results | ✔ | `labevents` (+ reference ranges) | pre-T0 and post-T0 | **DIRECT** | Outpatient labs present with NULL `hadm_id` **[DOC]**. |
| G | Vital signs | ⚠ | `icu.chartevents` (**ICU only**), `ed.triage`, `ed.vitalsign`, `omr` (BP) | pre-T0 | **PARTIAL / NOT AVAILABLE on wards** | **No ward vital signs exist in MIMIC-IV** **[INF from DOC]**. |
| H | Prior utilisation | ✔ | prior `admissions` rows, prior `edstays` | pre-T0 | **DIRECT (within BIDMC)** | Left truncation at cohort start and at first BIDMC contact **[INF]**. |
| I | ED encounters | ✔ | `ed.edstays` (incl. non-admitted) | pre- and post-T0 | **DIRECT, 2011–2019 only** | ED module covers 2011–2019 vs MIMIC-IV's 2008–2019 **[DOC]**; outcome undefined for 2008–2010 index stays. |
| J | Mortality | ⚠ | `patients.dod`, `admissions.deathtime`, `hospital_expire_flag` | post-T0 | **PARTIAL** | Censored at 1 year post-discharge; MA registry linkage only **[DOC]**. |
| K | Discharge destination | ✔ | `discharge_location` | at T0 | **DIRECT** | |
| L | Length of stay | ✔ | `dischtime − admittime`; `icustays.los` | at T0 | **DIRECT** | |
| M | Readmission measurement | ⚠ | subsequent `admissions.admittime` | post-T0 | **PARTIAL (observed only)** | Intervals valid because shifting is per-patient **[DOC]**. |
| N | Clinical notes | ⚠ | `note.discharge`, `note.radiology` | at/after T0 | **PARTIAL** | Sections deleted (§4). |
| O | Nursing documentation | ✘ | — | — | **NOT AVAILABLE** | No nursing notes in MIMIC-IV-Note **[DOC]**. ICU bedside flowsheet rows exist in `chartevents` **[DOC]** but are not nursing assessment documents. |
| P | Functional status | ✘ | — | — | **NOT AVAILABLE** (hospital-wide); **UNCERTAIN** for ICU `d_items` **[VERIFY]** | Corroborating: the official MIMIC Code Repository concept library contains no functional, mobility, Braden, ADL or delirium/CAM-ICU concept for MIMIC-IV — only `measurement/gcs.sql` and `firstday/first_day_gcs.sql` **[DOC]**. |
| Q | Cognition | ⚠ | `chartevents` GCS / RASS (ICU only) **[DOC]** | pre-T0 | **PROXY (ICU only)** | Sedation confounds GCS as a cognition measure **[INF]**. |
| R | Mobility | ✘ | — | — | **NOT AVAILABLE / UNCERTAIN** **[VERIFY]** | |
| S | ADL information | ✘ | — | — | **NOT AVAILABLE** | |
| T | Oxygen requirements | ⚠ | `chartevents` / `procedureevents` (ICU), `ed.vitalsign.o2sat` | pre-T0 | **PARTIAL (ICU/ED only)** | Ward oxygen delivery is not recorded **[INF]**. |
| U | Unresolved clinical issues | ⚠ | `chartevents` problem list (`itemid` 220001, ICU, mostly shift-change) **[DOC]**; discharge-summary narrative | pre-T0 | **PROXY** | Never a direct measure. |
| V | Medication reconciliation | ⚠ | `ed.medrecon` (**admission-side only**) | pre-T0 | **PROXY (admission), NOT AVAILABLE (discharge)** | No discharge reconciliation artefact **[INF]**. |
| W | Discharge instructions | ✘ | — | — | **NOT AVAILABLE** | Section removed in deidentification **[DOC]**. |
| X | Follow-up planning | ⚠ | `poe_detail.field_name = 'Discharge Planning'` / `'Discharge When'` **[DOC]** | pre-T0 | **PROXY, semantics unvalidated** **[VERIFY]** | Values such as "Finalized" indicate an administrative state, not the content of a plan. |
| Y | Referrals | ⚠ | `poe.order_type = 'Consults'` **[DOC]** | pre-T0 | **PROXY (inpatient consults only)** | Outpatient referrals not represented **[INF]**. |
| Z | Care coordination | ✘ | — | — | **NOT AVAILABLE** | |
| AA | Post-discharge encounters | ⚠ | subsequent `admissions`, `edstays`; `omr.chartdate`; `labevents` with NULL `hadm_id` | post-T0 | **PARTIAL** | Acute encounters only; OMR/outpatient-lab traces are an **unvalidated** proxy for ambulatory contact **[INF/VERIFY]**. |
| AB | Outpatient visits | ✘ | — | — | **NOT AVAILABLE** | No encounter table exists. |
| AC | Home-health encounters | ✘ | — | — | **NOT AVAILABLE** | `discharge_location = 'HOME HEALTH CARE'` records a *disposition*, not an encounter **[DOC]**. |
| AD | Telephone encounters | ✘ | — | — | **NOT AVAILABLE** | |
| AE | Post-discharge monitoring | ✘ | — | — | **NOT AVAILABLE** | |
| AF | Escalation pathways | ✘ | — | — | **NOT AVAILABLE** | |

### eICU deltas (only where the verdict differs from MIMIC-IV)

| # | Domain | eICU | Class |
|---|---|---|---|
| B/K | Discharge info / destination | `patient.hospitalDischargeLocation`, `.hospitalDischargeStatus`, `.unitDischargeLocation` | **DIRECT** (value set to verify) |
| G | Vital signs | `vitalPeriodic` (5-min medians), `vitalAperiodic`, `nurseCharting` | **DIRECT (ICU only)** — richer than MIMIC-IV |
| H, I, M, AA, AB | Prior/subsequent utilisation, readmission, post-discharge encounters | — | **NOT AVAILABLE** — no chronological ordering of hospitalisations **[DOC]** |
| J | Mortality | `hospitalDischargeStatus` only | **PARTIAL (in-hospital only)** |
| N, O | Notes / nursing documentation | `note` (structured picklists only; narrative removed) **[DOC]**; `nurseAssessment`, `nurseCare`, `nurseCharting` | **PROXY (structured)** — richer than MIMIC-IV for nursing |
| P, R, S | Function / mobility / ADL | `nurseCare` Activity + Hygiene/ADLs; `nurseAssessment` Braden incl. Activity | **PROXY AVAILABLE (ICU, variable completeness)** |
| Social/caregiver | — | `carePlanGeneral` Family/Health Care Proxy, Psychosocial Status, Baseline Status | **PROXY AVAILABLE** |
| V | Medication reconciliation | `admissionDrug` — documented *"Extremely infrequently used"* **[DOC]** | **PROXY, unusable in practice** |
| W, X, Y, Z, AC, AD, AE, AF | Instructions, follow-up, referrals, coordination, home health, telephone, monitoring, escalation | — | **NOT AVAILABLE** |

---

## 7. Temporal Availability / T0 Audit

**T0 ≡ the discharge decision point.** Operationally, `admissions.dischtime` for the index
hospitalisation. (Strictly, the *decision* precedes the *event*; `poe_detail.field_name = 'Discharge
When'` with value *"Discharge Now"* **[DOC]** is the closest documented marker of the decision itself
and is worth evaluating as the T0 anchor **[PROP, VERIFY]**.)

```
                        ┌──────────────────────────────────────────────┐
   PRE-T0 DATA          │ admissions (admittime, admission_type,       │
   (feature-eligible)   │   admission_location, insurance, marital,    │
                        │   language, race, edregtime/edouttime)       │
                        │ transfers · services · icustays              │
                        │ labevents  charttime  ≤ T0   (+ ref ranges)  │
                        │ microbiologyevents  charttime ≤ T0           │
                        │ prescriptions / pharmacy / emar  ≤ T0        │
                        │ poe / poe_detail  ordertime ≤ T0             │
                        │ chartevents / procedureevents  ≤ T0  [ICU]   │
                        │ ed.triage / ed.vitalsign / ed.medrecon       │
                        │ omr  chartdate ≤ T0  (incl. pre-admission)   │
                        │ prior admissions & prior edstays  (< index)  │
                        │ patients.anchor_age / gender                 │
                        └───────────────────────┬──────────────────────┘
                                                │
                        ╔═══════════════════════▼══════════════════════╗
   T0                   ║  DISCHARGE DECISION  =  admissions.dischtime ║
                        ║  Decision variables observable at T0:        ║
                        ║    discharge_location  (the decision itself) ║
                        ║    LOS = dischtime − admittime               ║
                        ╚═══════════════════════╤══════════════════════╝
                                                │
   ── FORBIDDEN AS FEATURES ─────────────────────────────────────────────
     diagnoses_icd · drgcodes · hcpcsevents      (coded after discharge)
     deathtime · hospital_expire_flag · dod      (outcome)
     discharge_location = 'DIED' / 'HOSPICE'     (encodes the outcome)
     note.discharge (storetime > T0)             (narrates whole stay)
     any labevents / emar / omr row  charttime > T0
   ──────────────────────────────────────────────────────────────────────
                                                │
                        ┌───────────────────────▼──────────────────────┐
   30-DAY OUTCOME       │ admissions.admittime ∈ (T0, T0+30d]          │
   (T0, T0+30d]         │ edstays.intime      ∈ (T0, T0+30d]           │
                        │ patients.dod        ∈ (T0, T0+30d]           │
                        │  → ALL BIDMC-OBSERVED ONLY                   │
                        └───────────────────────┬──────────────────────┘
                                                │
                        ┌───────────────────────▼──────────────────────┐
   90-DAY OUTCOME       │ same constructions, window (T0, T0+90d]      │
   (T0, T0+90d]         │ mortality valid: dod censored at 1 y  [DOC]  │
                        │ readmission/ED: same institutional bound     │
                        └──────────────────────────────────────────────┘
```

**Why the interval arithmetic is valid.** Deidentification shifted dates using a **patient-level
offset**, and *"the shift ensures that the interval between two time points for a patient is
preserved"* **[DOC]**. Therefore `admittime(next) − dischtime(index)` is a true elapsed interval.
Cross-patient calendar comparisons are invalid; use `anchor_year_group` for era adjustment **[DOC]**.

**Why the same arithmetic is impossible in eICU.** Offsets are anchored to *each unit stay's own*
admission, and hospitalisations for one patient cannot be ordered within a year **[DOC]**. There is
no common origin.

---

## 8. M1–M8 Feasibility Matrix

### M1 — Structured Reassessment

| Required concept | MIMIC-IV | eICU |
|---|---|---|
| Clinical stability | **PROXY** — trajectory of labs/vitals in the pre-T0 window; no stability instrument exists | **PROXY** — dense `vitalPeriodic`, ICU only |
| Functional status | **NOT AVAILABLE** | **PROXY** — `nurseCare` Activity |
| Cognition | **PROXY (ICU only)** — GCS/RASS **[DOC]** | **PROXY** — GCS components in `apachePredVar` **[DOC]** |
| Mobility | **NOT AVAILABLE** (`d_items` **[VERIFY]**) | **PROXY** — Braden Activity subscale **[DOC]** |
| ADL | **NOT AVAILABLE** | **PROXY** — `nurseCare` Hygiene/ADLs **[DOC]** |
| Nursing assessment | **NOT AVAILABLE** as documents | **PROXY** — `nurseAssessment` **[DOC]** |
| Vital signs near discharge | **NOT AVAILABLE for ward patients**; DIRECT for ICU-resident patients only | **DIRECT (ICU)** but ICU discharge ≠ hospital discharge |
| Abnormal labs near discharge | **DIRECT** — `labevents` + `ref_range_lower/upper` + `flag` **[DOC]** | **DIRECT** — `lab` |
| Oxygen requirement | **PARTIAL (ICU/ED)** | **PARTIAL** — `respiratoryCare`/`respiratoryCharting` (ICU) |
| Unresolved issues | **PROXY** — ICU problem list `itemid` 220001 **[DOC]**; narrative | **PROXY** — `diagnosis` active problems; `carePlanGeneral.activeUponDischarge` |
| Discharge readiness | **NOT AVAILABLE** | **NOT AVAILABLE** |

**Verdict: LEVEL C — DO NOT TEST YET.** The mechanism's defining constructs (function, mobility, ADL,
readiness) are absent in MIMIC-IV; in eICU they exist as ICU-scoped proxies but there is no
post-discharge outcome to test them against. A narrowly bounded LEVEL B variant exists — patients
resident in an ICU at hospital discharge, using labs + ICU vitals + GCS — but that subcohort is
unrepresentative of the transition-of-care population and should not be presented as a test of M1.

### M2 — Patient Selection

Can T0 data support testing of:

| Target | MIMIC-IV |
|---|---|
| High-risk patients | **YES (proxy definition)** — risk defined by observed outcome, not by an external label |
| Readmission risk | **YES, bounded** — observed BIDMC readmission within 30 d |
| ED utilisation | **YES, bounded** — `edstays.intime` post-T0; **[VERIFY]** ED coverage window |
| Mortality risk | **PARTIAL** — `dod`, incomplete linkage, 1-year censoring **[DOC]** |
| Unsuitable home transition | **NOT AVAILABLE** — no construct exists for suitability; discharge destination is a decision, not a suitability measure **[INF]** |

Comparison of approaches (all **[PROP]**, none executed):

- **A. Simple clinical rule** — feasible (e.g. age, prior admissions in 6 months, LOS, admission type,
  discharge destination, count of abnormal labs at T0). All inputs are T0-legal.
- **B. Risk-score approach** — feasible for scores computable from available fields (e.g.
  LACE-style: Length of stay, Acuity via `admission_type`, Comorbidity, ED visits). **Caveat:** the
  comorbidity component normally uses ICD codes, which are assigned *after* discharge **[DOC]**. Using
  index-admission ICD codes as a T0 feature is leakage; comorbidity must be built from *prior*
  admissions' codes only. This constraint materially weakens any published score's reproduction and
  must be stated in the protocol.
- **C. Multivariable statistical model** — feasible (logistic regression / Cox), with explicit
  variable list and pre-specified handling of missingness.

No machine learning at this stage, per protocol.

**Verdict: LEVEL B.** Testable using justified proxies. The outcome is an *observed* event, the
comorbidity feature set is constrained by coding timing, and "unsuitable home transition" is not
testable at all.

### M3 — Level-of-Care Selection

**Destination identification: DIRECTLY AVAILABLE.** `discharge_location` distinguishes HOME, HOME
HEALTH CARE, SKILLED NURSING FACILITY, REHAB, CHRONIC/LONG TERM ACUTE CARE, ASSISTED LIVING, HOSPICE,
ACUTE HOSPITAL, PSYCH FACILITY, HEALTHCARE FACILITY, OTHER FACILITY, AGAINST ADVICE, DIED, with
documented UB-04 mappings **[DOC]**. eICU's `hospitalDischargeLocation` is a structured list but its
value set is not published **[VERIFY]**.

**Baseline confounders available at T0:** age, sex, race, insurance, marital status, language,
admission type/location, service, LOS, ICU exposure, lab trajectory, medication burden, prior
utilisation, `poe_detail` code status. **[DOC]**

**Baseline confounders NOT available:** functional status, mobility, ADL dependence, cognition
outside the ICU, caregiver availability, home environment, patient/family preference. **[DOC, by
absence]**

**[INF] These missing variables are precisely the variables clinicians use to choose between home and
SNF.** Propensity scores, IPW and doubly robust estimation are all *computable*, but computability is
not identification. With the dominant confounder unmeasured, a doubly robust estimate is doubly
robust to model misspecification and not at all robust to this confounding. **Do not claim causal
inference merely because these methods are available.**

**Verdict: LEVEL B** for *association* between destination and observed outcomes with transparent
confounding limitations; **LEVEL C** for any causal claim about level-of-care selection. A negative
control outcome and a quantitative bias analysis (E-value or equivalent) are mandatory if this is
pursued **[PROP]**.

### M4 — Coordinated Transition

| Component | MIMIC-IV | Classification |
|---|---|---|
| Medication reconciliation | `ed.medrecon` at ED arrival **[DOC]** | **PROXY — admission-side only.** Discharge reconciliation: *Component not directly measurable in this dataset.* |
| Discharge instructions | Section removed **[DOC]** | **NOT AVAILABLE.** *Component not directly measurable in this dataset.* |
| Follow-up planning | `poe_detail 'Discharge Planning'` (475,428 rows) **[DOC]** | **PROXY — administrative state only, semantics unvalidated [VERIFY]** |
| Communication (to patient / to next provider) | — | **NOT AVAILABLE.** *Component not directly measurable in this dataset.* |
| Discharge summary | `note.discharge` with `charttime`/`storetime` **[DOC]** | **DIRECT for existence and timing; PARTIAL for content** |
| Medication changes | `prescriptions` vs `ed.medrecon` **[PROP]** | **PROXY — requires drug-name normalisation across GSN/NDC/ETC; unvalidated [VERIFY]** |
| Care coordination | — | **NOT AVAILABLE** |
| Referrals | `poe.order_type='Consults'` **[DOC]** | **PROXY — inpatient consults only, not outpatient referrals** |
| Primary-care follow-up | — | **NOT AVAILABLE** |

**Component-level vs bundle-level.** Component level: two components have a defensible measure
(discharge-summary existence/timing; admission medication reconciliation) and three have weak
unvalidated proxies. **Bundle level: not measurable.** A transitional-care bundle is defined by the
co-occurrence of components that are individually unobservable here; constructing a "bundle score"
from these proxies would manufacture a variable.

**Verdict: LEVEL C — DO NOT TEST YET.**

### M5 — Structured Post-Discharge Follow-up

| Item | Availability |
|---|---|
| Outpatient visits | **NOT AVAILABLE** — no encounter table **[DOC, by absence]** |
| Primary-care visits | **NOT AVAILABLE** |
| Specialty visits | **NOT AVAILABLE** |
| Home-health encounters | **NOT AVAILABLE** (`discharge_location = 'HOME HEALTH CARE'` is a disposition, not an encounter) |
| Telephone encounters | **NOT AVAILABLE** |
| First follow-up timing | **NOT CONSTRUCTIBLE** — the 0–3 / 4–7 / 8–14 / 15–30 day bands cannot be populated |

The only post-T0 ambulatory *traces* are `omr` rows with `chartdate > T0` and `labevents` rows with
NULL `hadm_id` after T0 **[DOC that these rows exist; INF that they imply ambulatory contact]**. These
are traces of a measurement being taken somewhere in the BIDMC-affiliated system — not encounters,
not visit types, not attributable to a follow-up plan. **Using them as "follow-up visits" would be
exactly the kind of manufactured proxy this audit exists to prevent.**

**Bias analysis, stated for completeness even though the mechanism is untestable:**

- **Immortal-time bias — severe and structural.** Exposure ("received follow-up within 7 days") can
  only be assigned to patients who survived and remained un-readmitted long enough to receive it.
  Naïve classification of the pre-exposure period as exposed guarantees a spurious protective effect.
  Any future design would require landmark analysis or time-varying exposure — but neither can rescue
  a dataset in which the exposure itself does not exist.
- **Selection bias.** Patients who obtain follow-up at BIDMC differ systematically from those who
  follow up elsewhere; only the former would leave any trace, so exposure ascertainment is
  differential by care-network affiliation.

**Verdict: LEVEL C — DO NOT TEST YET.**

### M6 — Remote Monitoring

**Strict separation applied.**

- **In-hospital monitoring:** MIMIC-IV `icu.chartevents` (ICU bedside) **[DOC]**; eICU
  `vitalPeriodic` (5-minute medians from bedside monitors, no human validation) and `vitalAperiodic`
  **[DOC]**. These are inpatient data collected while the patient is physically in an ICU bed.
- **Post-discharge remote monitoring:** none. No table, no field, no device stream, in either
  dataset.

eICU is a *tele-ICU* programme — remote clinicians monitoring **inpatients**. It is not remote
monitoring of discharged patients, and the tele-ICU alert/response record is not part of the released
schema **[INF]**. Labelling eICU "remote monitoring data" for this mechanism would be a
misclassification of the care setting.

**"Not directly testable in this dataset."**

**Verdict: LEVEL C — DO NOT TEST YET.**

### M7 — Escalation Pathway

| Element | Availability |
|---|---|
| Abnormal signals (pre-discharge) | **DIRECT** — `labevents` with reference ranges and `flag` **[DOC]**; ICU vitals **[DOC]** |
| Subsequent ED visit | **DIRECT, bounded** — `edstays.intime` post-T0 **[DOC]** |
| Subsequent hospitalisation | **DIRECT, bounded** — `admissions.admittime` post-T0 **[DOC]** |
| ICU escalation | **DIRECT, bounded** — `icustays.intime` within the readmission **[DOC]** |
| Timing between signal and event | **COMPUTABLE** for signals observed pre-discharge or in acute re-presentation; intervals are valid **[DOC]** |
| Documented escalation pathway | **NOT AVAILABLE** — no alert, no trigger, no response record, no rapid-response table **[DOC, by absence]** |

Because no escalation intervention exists in the data, the only honest framing is
**RETROSPECTIVE DETECTABILITY**: *were signals present before T0 that statistically preceded a later
acute event?* This is **NOT** escalation effectiveness, and results must never be worded as though a
pathway had been evaluated. There is also a hard gap: between discharge and re-presentation, the
patient is unobserved, so "delayed recognition" has no measurable clock.

**Verdict: LEVEL C for the mechanism as specified. LEVEL B for retrospective detectability only,
under a renamed research question.**

### M8 — Safety / Failure Modes

| Failure domain | Element | MIMIC-IV verdict |
|---|---|---|
| Clinical | Deterioration | **PROXY** — lab/vital trajectory pre-T0 (ICU) and severity at re-presentation |
| Clinical | Unresolved instability | **PROXY** — abnormal labs at T0 via reference ranges **[DOC]** |
| Clinical | Complications | **NOT RELIABLY MEASURABLE** — `diagnoses_icd` has **no present-on-admission flag** **[DOC, by absence]**, so a complication cannot be distinguished from a comorbidity |
| Medication | Discrepancies | **PROXY, unvalidated** — `ed.medrecon` vs `prescriptions` **[VERIFY]** |
| Medication | High-risk medication issues | **PROXY** — identify high-risk classes via GSN/NDC/ETC **[DOC]**; harm events not directly coded |
| Communication | Missing information / results / unclear plans | **NOT AVAILABLE** |
| Utilisation | ED / readmission / repeat acute care | **DIRECT, bounded** **[DOC]** |
| Functional | Mobility limitation / self-management | **NOT AVAILABLE** |
| Social | Inadequate support | **NOT AVAILABLE** (Social History removed **[DOC]**) |
| Monitoring | Missed signals | **NOT AVAILABLE** (no post-discharge signals exist) |
| Escalation | Delayed recognition | **NOT AVAILABLE** (no observation between T0 and re-presentation) |

**Verdict: LEVEL C for M8 as specified. LEVEL B for the utilisation sub-domain alone**, which is
already covered by M2's outcomes and adds nothing new. **DO NOT TEST YET.**

---

## 9. Outcome Feasibility

| Outcome | Class | Construction (if measurable) |
|---|---|---|
| **30-day readmission (PRIMARY)** | **PARTIALLY MEASURABLE** | Index = `admissions` row with `hospital_expire_flag = 0` and `discharge_location NOT IN ('DIED','HOSPICE')`. T0 = `dischtime`. Outcome = 1 if ∃ another `admissions` row, same `subject_id`, with `admittime > T0` and `admittime ≤ T0 + 30 days`. Exclude organ-donor admissions (documented short/negative LOS artefacts **[DOC]**). Exclude index stays whose `discharge_location = 'ACUTE HOSPITAL'` (transfer out, follow-up not observable) **[PROP]**. Planned-readmission exclusion is *partially* implementable from `procedures_icd` **[PROP]**; the full CMS planned-readmission algorithm cannot be reproduced exactly **[VERIFY]**. **Must be reported as "readmission observed at BIDMC".** |
| **ED visit (post-discharge)** | **PARTIALLY MEASURABLE, 2011–2019 index stays only** | `edstays.intime ∈ (T0, T0+30d]`, including visits with NULL `hadm_id` (not admitted) **[DOC]**. **Mandatory restriction:** MIMIC-IV-ED covers 2011–2019 while MIMIC-IV covers 2008–2019 **[DOC]**, so index discharges in 2008–2010 have an *undefined*, not negative, ED outcome and must be excluded. |
| **Mortality (30 / 90-day)** | **PARTIALLY MEASURABLE** | `patients.dod ∈ (T0, T0+30d]` or `(T0, T0+90d]`. **Documented limits:** deaths beyond one year post-discharge are censored **[DOC]**; ascertainment relies on Massachusetts state records plus hospital records **[DOC]**, so out-of-state deaths are systematically missed **[INF]**. Report ascertainment as incomplete; do not report crude mortality as if complete. |
| **Acute-care utilisation (composite)** | **PARTIALLY MEASURABLE** | Union of readmission and ED visit within the window. Inherits both bounds. |
| **Complications** | **NOT MEASURABLE** | No present-on-admission flag **[DOC, by absence]**; ICD codes are assigned post-discharge **[DOC]**. |
| **Length of stay** | **DIRECTLY MEASURABLE** | `dischtime − admittime`. **Note this is a T0/pre-T0 variable, not a post-discharge outcome**; using index LOS as an "outcome" of a discharge-time decision is circular. |
| **Repeat hospitalisation (90-day)** | **PARTIALLY MEASURABLE** | As for 30-day, window (T0, T0+90d]. Same institutional bound. |

**No outcome in this table is defined using information unavailable at T0** — each is constructed
strictly from events occurring after `dischtime`. Conversely, none of the T0 feature sets may include
`diagnoses_icd`, `drgcodes`, `hcpcsevents`, `deathtime`, `hospital_expire_flag`, or any row with a
timestamp after `dischtime` (§13).

**eICU: every outcome above is NOT MEASURABLE**, except in-hospital mortality
(`hospitalDischargeStatus`) and hospital LOS (derivable from offsets **[DOC]**), neither of which is a
post-discharge outcome.

---

## 10. Post-Discharge Observability Audit

**This section is mandatory and its distinction must be carried into every table, figure and
sentence of any downstream analysis.**

### MIMIC-IV

- **Single institution.** MIMIC-IV is sourced from the EHR of one academic medical centre **[DOC]**.
- **No health-information-exchange linkage.** There is no documented linkage to claims, to other
  hospitals, or to a regional exchange **[DOC, by absence]**.
- **Therefore:** a patient readmitted to any other hospital is recorded in MIMIC-IV as *no
  readmission*.

| Statement | Status |
|---|---|
| "No readmission occurred" | **NOT SUPPORTABLE** |
| "No readmission was observed in MIMIC-IV within 30 days of discharge" | **SUPPORTABLE** |

**[INF] The direction of the resulting bias is not random.** Patients discharged to HOME are more
likely to re-present to the same hospital; patients discharged to a SNF, rehabilitation facility or
another region may re-present elsewhere. Under-ascertainment is therefore plausibly *differential by
discharge destination* — the exact exposure of interest in M3. This is a threat to the M3 analysis
specifically, not merely a loss of power.

Partial mitigations **[PROP]**, none sufficient: restrict to patients with documented prior BIDMC
utilisation (a crude marker of network affiliation); report a sensitivity analysis in which
non-observed patients are assumed to have events at plausible external rates; report results as
event *detection* rates rather than incidence.

### eICU

Beyond the same non-linkage problem, eICU adds two further barriers:

1. Hospitalisations for the same patient cannot be ordered in time **[DOC]** ⇒ no window can be
   defined.
2. Only ICU/step-down stays were sampled, and stays consisting solely of step-down/low-acuity care
   were removed **[DOC]** ⇒ a subsequent *ward-level* hospitalisation would not appear even if it
   occurred within the same network.

**Any "readmission rate" computed from eICU would be an artefact. Do not compute one.**

---

## 11. Access & Reproducibility Audit

### Access

| Item | MIMIC-IV / MIMIC-IV-ED / MIMIC-IV-Note | eICU-CRD |
|---|---|---|
| Official source | PhysioNet — `physionet.org/content/mimiciv/`, `/mimic-iv-ed/`, `/mimic-iv-note/` **[DOC]** | PhysioNet — `physionet.org/content/eicu-crd/` **[DOC]** |
| Documentation | `mimic.mit.edu/docs/iv/` (source: `github.com/MIT-LCP/mimic-website`) | `eicu-crd.mit.edu` (source: `github.com/MIT-LCP/eicu-code`) |
| Version audited | Documentation anchored to **v2.2**; PhysioNet distributes a later v3.x release **[VERIFY]** | **v2.0** (2014–2015 admissions) **[DOC]** |
| Dataset DOI | **UNCERTAIN — REQUIRES VERIFICATION.** Must be copied verbatim from the PhysioNet landing page of the exact version used. Do not cite a DOI from memory or from a search snippet. | **UNCERTAIN — REQUIRES VERIFICATION.** Same instruction. |
| Peer-reviewed citation | Johnson et al., *Sci Data* (2023), [10.1038/s41597-022-01899-x](https://doi.org/10.1038/s41597-022-01899-x) | Pollard et al., *Sci Data* (2018), [10.1038/sdata.2018.178](https://doi.org/10.1038/sdata.2018.178) |
| Access requirements | Completion of a human-subjects research training course **and** a signed DUA **[DOC]** | CITI *"Data or Specimens Only Research"* course + PhysioNet credentialed application + DUA **[DOC]** |
| DUA obligations | Safeguard the data; do not attempt re-identification; do not share the data; report deidentification issues **[DOC]** | Do not share the data; do not attempt to re-identify patients or institutions; release code associated with any publication **[DOC]** |
| **Legally/technically accessible in this environment?** | **NO** | **NO** |
| Download / API available here? | **NO** | **NO** |
| Patient-level data accessible here? | **NO** | **NO** |

**Environment finding [DOC — observed this session]:** `physionet.org`, `mimic.mit.edu` and
`eicu-crd.mit.edu` are all blocked by this environment's network egress proxy. This audit was
therefore conducted against (a) the peer-reviewed dataset papers retrieved from PubMed Central and
(b) the **official documentation source repositories** `MIT-LCP/mimic-website` and `MIT-LCP/eicu-code`,
which are the upstream source of the documentation websites. No credentials were used, none were
requested, and no patient-level data were accessed or attempted. **No secrets or API keys are stored
in this repository.**

**[INF] Consequence for the project plan:** the next phase cannot be executed in this environment.
It requires (1) an individual to complete CITI training and hold approved PhysioNet credentialed
access under a signed DUA, and (2) a compute environment permitted by that DUA. This is a hard gate,
not a configuration problem.

### Reproducibility

| Requirement | Reproducible today? | Blocker |
|---|---|---|
| Exact cohort definition | **YES** | — (given a pinned version) |
| Exact tables | **YES** | — |
| Exact fields | **PARTIAL** | `itemid` in `chartevents`/`d_items` cannot be enumerated without data access; `itemid` assignments have changed between releases **[VERIFY]** |
| Exact temporal windows | **YES** | Interval preservation is documented **[DOC]** |
| Exact exclusions | **PARTIAL** | Organ-donor and planned-readmission exclusions need empirical rules **[VERIFY]** |
| Exact outcome definitions | **YES for readmission/ED/mortality**; **NO for complications** | No present-on-admission flag |
| Exact statistical methods | **YES** | Pre-specification only; nothing has been run |
| Exact SQL / query logic | **PARTIAL** | Cannot be executed or validated without credentialed access |
| Exact assumptions | **YES** | Documented in §10, §13, §15 |

**Not currently reproducible at all:** any construct requiring functional status, mobility, ADL,
cognition outside the ICU, caregiver support, discharge instructions, follow-up encounters, or
post-discharge monitoring. These are not blocked by tooling; the variables do not exist.

---

## 12. Dataset Comparison

Qualitative classification only. **No numerical scores are assigned**, because no defensible,
pre-specified weighting framework exists for these criteria; inventing weights would give the
comparison a false precision.

| # | Criterion | MIMIC-IV (+ED, +Note) | eICU-CRD v2.0 |
|---|---|---|---|
| 1 | Temporal completeness | **STRONG** — full timestamps, patient-level shift preserving intervals **[DOC]** | **NOT SUITABLE** — offsets only; hospitalisations unorderable **[DOC]** |
| 2 | Discharge information | **STRONG** — UB-04-mapped destination value set **[DOC]** | **MODERATE** — structured list, value set unpublished **[VERIFY]** |
| 3 | 30-day outcome availability | **MODERATE** — computable but institution-bounded | **NOT SUITABLE** |
| 4 | 90-day outcome availability | **MODERATE** — same bound; mortality valid to 1 y **[DOC]** | **NOT SUITABLE** |
| 5 | Medication information | **STRONG** — prescription + pharmacy + barcode administration **[DOC]** | **MODERATE** — orders only; infusions in 73% of hospitals **[DOC]** |
| 6 | Follow-up information | **NOT SUITABLE** — no encounter data | **NOT SUITABLE** |
| 7 | Safety information | **WEAK** — utilisation only; no POA flag | **WEAK** |
| 8 | Functional information | **NOT SUITABLE** | **MODERATE** — `nurseCare` Activity/ADLs, Braden **[DOC]**, ICU-scoped |
| 9 | Cognitive information | **WEAK** — GCS/RASS, ICU only **[DOC]** | **WEAK** — worst-set GCS **[DOC]** |
| 10 | Social information | **NOT SUITABLE** — Social History removed **[DOC]** | **WEAK-to-MODERATE** — care-plan proxy/psychosocial fields **[DOC]** |
| 11 | Monitoring information | **MODERATE (in-hospital ICU)**; **NOT SUITABLE (post-discharge)** | **STRONG (in-hospital ICU)**; **NOT SUITABLE (post-discharge)** |
| 12 | Escalation information | **NOT SUITABLE** | **NOT SUITABLE** |
| 13 | Sample size | **STRONG** — 431,231 admissions / 299,712 patients at v2.2; larger in v3.x **[DOC for v2.2; VERIFY for v3.x]** | **STRONG** — 200,859 unit stays / 139,367 patients **[DOC]** |
| 14 | External reproducibility | **WEAK** — single centre **[DOC]** | **STRONG in principle** (208 hospitals) but unusable for this design **[DOC]** |
| 15 | Documentation quality | **STRONG** — per-table docs, changelog, peer-reviewed paper | **STRONG** — per-table docs with explicit completeness warnings |

**The decisive asymmetry:** eICU has the multi-centre breadth and the nursing/functional
documentation that MIMIC-IV lacks, and MIMIC-IV has the only usable post-discharge clock. Neither has
both. **No combination of the two datasets produces a testable transition-of-care design**, because
the constructs and the outcomes live in different, unlinkable datasets.

---

## 13. Leakage Risks

Every item below is a concrete, documented mechanism by which post-T0 information can enter a
pre-T0 feature set.

| # | Leakage source | Evidence | Mitigation |
|---|---|---|---|
| L1 | **`diagnoses_icd`, `drgcodes`, `hcpcsevents`** — billing codes are assigned by coders after reviewing signed notes | **[DOC]** | Never use index-admission codes as T0 features. Build comorbidity only from *prior* admissions. |
| L2 | **`discharge_location = 'DIED'` / `'HOSPICE'`** encodes the outcome | **[DOC]** value set | Exclude from the index cohort before modelling. |
| L3 | **`deathtime`, `hospital_expire_flag`, `dod`** | **[DOC]** | Outcome variables only. |
| L4 | **`emar` rows outside the admit/discharge window** — 713,117 rows (~2.5%) occur outside administratively documented admit/discharge times | **[DOC]** (v2.2 changelog) | Filter by `charttime ≤ dischtime`, not by `hadm_id`. |
| L5 | **`labevents` `hadm_id` assignment by proximity** — `hadm_id` is assigned via `transfers`, imperfectly capturing stay boundaries | **[DOC]** | Filter by `charttime ≤ dischtime` explicitly; do not rely on `hadm_id` alone. |
| L6 | **`labevents.storetime` ≫ `charttime`** — results become available significantly later than collection | **[DOC]** | For a decision-time model, require `storetime ≤ T0`, not merely `charttime ≤ T0`. |
| L7 | **Discharge summary text** — authored at/after discharge, narrates the entire stay and the disposition | **[DOC]** (`storetime` = when completed and signed) | Exclude, or justify explicitly with a `storetime ≤ T0` filter and acknowledge residual narrative leakage. |
| L8 | **Note addenda (`note_type = 'AD'`)** written after discharge | **[DOC]** | Exclude. |
| L9 | **`omr` rows with `chartdate > T0`** — OMR mixes inpatient and outpatient measurements | **[DOC]** | Filter on `chartdate ≤ T0`. Note `chartdate` is date-granular, so same-day rows are ambiguous. |
| L10 | **Outpatient `labevents` (NULL `hadm_id`) after T0** | **[DOC]** | Same-day ambiguity; treat T0-day post-discharge results as post-T0 by default. |
| L11 | **`transfers` rows after discharge** and `icustays` from a *subsequent* admission | **[DOC]** | Key all pre-T0 features to the index `hadm_id` **and** a timestamp filter. |
| L12 | **`prescriptions.stoptime` in the future** relative to T0 | **[DOC]** — prescriptions carry `starttime`/`stoptime` | Use `starttime ≤ T0`; never use `stoptime` as a feature. |
| L13 | **`anchor_year_group` era leakage** — using calendar era as a predictor can proxy outcome-period practice changes | **[DOC]** | Use only as a pre-specified adjustment/stratification variable. |
| L14 | **Target leakage via the index-stay LOS in a discharge-timing question** | **[INF]** | If the estimand concerns *when* to discharge, LOS is part of the decision, not a covariate. |

---

## 14. Missing Variables

Variables required by the CareLink mechanism model that **do not exist** in either dataset. This list
is the actual result of the audit and should be treated as the project's binding constraint.

**Absent from both MIMIC-IV and eICU:**

- Discharge instructions (content) — deleted from MIMIC-IV-Note **[DOC]**; no equivalent in eICU.
- Written care plan given to the patient; teach-back or comprehension documentation.
- Communication to the next provider; discharge-summary transmission or receipt.
- Scheduled follow-up appointment (date, specialty, attended/not).
- Primary-care visits, specialty visits, home-health visits, telephone encounters.
- Post-discharge vital signs, weights, symptoms, or any patient-reported data.
- Any remote monitoring stream after discharge.
- Escalation triggers, alerts, and the response to them.
- Caregiver identity, availability or capacity; home environment; social support adequacy.
- Patient/family preference regarding discharge destination.
- Health literacy; transportation access; medication affordability.
- Present-on-admission indicator (so complications are not identifiable) **[DOC, by absence]**.

**Absent from MIMIC-IV specifically (present in some form in eICU):**

- ADL/hygiene documentation, activity documentation, Braden-type mobility subscales.
- Nursing assessment documents.
- Healthcare-proxy / psychosocial-status structured fields.
- **Ward (non-ICU) vital signs** — absent from MIMIC-IV; eICU has ICU vitals but no ward data either.

**Absent from eICU specifically (present in MIMIC-IV):**

- Calendar-ordered hospitalisations; any post-discharge time window.
- Out-of-hospital mortality.
- Free-text clinical notes.
- Non-ICU hospitalisations and ED visits.

---

## 15. Bias Risks

| Bias | Mechanism | Severity |
|---|---|---|
| **Ascertainment / observability bias** | Events at other institutions are invisible; plausibly differential by discharge destination **[INF from DOC single-centre design]** | **Critical** — threatens M3 directly |
| **Selection bias (cohort universe)** | MIMIC-IV includes only patients admitted to the ED or an ICU during 2008–2019 **[DOC]**; purely elective non-ICU admissions are under-represented | High |
| **Selection bias (eICU sampling)** | Stratified sample of *index* stays, then all subsequent stays for selected patients; step-down-only patients removed **[DOC]** | High (eICU) |
| **Left truncation** | Prior-utilisation features are only observable back to the patient's first BIDMC contact and to 2008 **[INF]** | High |
| **Immortal-time bias** | Any post-discharge exposure (follow-up, monitoring) is conditioned on surviving un-readmitted to receive it | Critical for M5/M6 — which is why they are LEVEL C |
| **Competing risks** | Death precludes readmission; naïve cumulative incidence overstates readmission-free survival | High |
| **Informative censoring** | Loss to observation correlates with care-network affiliation and destination | High |
| **Confounding by indication / unmeasured confounding** | Function, cognition and caregiver support drive destination and outcome; all unmeasured **[DOC, by absence]** | Critical for M3 |
| **Measurement/deidentification-induced missingness** | ED `triage`/`vitalsign` numeric fields: deidentified values are indistinguishable from missing values **[DOC]**, with documented counts | Moderate |
| **Differential data capture over time** | eMAR deployed 2014–2016; full coverage only from 2016 **[DOC]**; OMR added in v2.0 **[DOC]** | Moderate–High |
| **Site heterogeneity (eICU)** | Documented variation in table completion by hospital **[DOC]** | High (eICU) |
| **Coding-practice drift** | ICD-9 → ICD-10 transition within the study period **[DOC]** | Moderate |
| **Version instability** | `itemid` and value sets have changed across releases **[VERIFY]** | Moderate |
| **Post-discharge era effects** | Practice change over a decade; `anchor_year_group` is the only era handle **[DOC]** | Moderate |

---

## 16. Evidence-Level Classification

**DOCUMENTED FACTS** (each traceable to a cited source, listed in §18):

MIMIC-IV covers 2008–2019 admissions at a single centre; the cohort universe is ED-or-ICU patients
aged ≥18; date shifting is per-patient and preserves intervals; `discharge_location` has a defined
UB-04-mapped value set; `dod` provides out-of-hospital mortality up to one year post-discharge and is
censored thereafter; `chartevents` is ICU-sourced; the Social History and Discharge Instructions
sections were removed from discharge summaries; MIMIC-IV-Note contains only discharge summaries and
radiology reports; `edstays` includes ED visits without admission; `poe_detail` contains
`Discharge Planning` and `Discharge When` fields; `omr` contains inpatient and outpatient BP, height,
weight, BMI and eGFR; eMAR coverage is incomplete before 2016; `labevents` includes outpatient rows
with NULL `hadm_id`; ~713k eMAR rows fall outside the administrative stay window. eICU-CRD v2.0
contains 200,859 unit stays for 139,367 patients across 208 hospitals in 2014–2015; all offsets are
relative to unit admission; calendar dates were removed; there is no systematic method for
chronologically ordering hospitalisations for the same patient within a year; narrative note text was
removed; `nurseCare`, `nurseAssessment` and `carePlanGeneral` contain structured activity/ADL,
Braden, and family/psychosocial documentation; table completion varies by hospital. Both datasets
require training plus a signed DUA for credentialed access.

**RESEARCHER INFERENCES** (logically derived, explicitly flagged in-line):

That eICU cannot support any post-discharge time window; that MIMIC-IV under-ascertainment is
plausibly differential by discharge destination; that ward vital signs are unavailable in MIMIC-IV;
that outpatient `labevents`/`omr` rows imply ambulatory contact but not encounters; that the missing
confounders are the ones clinicians actually use for destination decisions; that the DUA/credentialing
gate blocks execution in this environment.

**PROPOSED ANALYTIC APPROACHES** (design suggestions only, none executed):

The candidate index-cohort and outcome constructions in §9; the three-way A/B/C comparison in M2; the
landmark/time-varying framing noted (and rejected as insufficient) in M5; quantitative bias analysis
for M3; `poe_detail 'Discharge When'` as a candidate T0 anchor; medication-change detection by
normalising `ed.medrecon` against `prescriptions`.

---

## 17. Dataset Decision Gate

### DATASET DECISION

**MIMIC-IV: PRIMARY DATASET** — restricted to T0-side risk prediction (M2) and discharge-destination
association (M3), with post-discharge outcomes reported as *observed at BIDMC*.

**eICU: NOT SUITABLE** as an external replication dataset for this design. Retained as a **SECONDARY
DATASET** only for auditing pre-T0 construct availability (functional/ADL/care-plan documentation) and
in-hospital outcomes. It must not be used to compute any readmission or post-discharge measure.

*Note on the required options: "EXTERNAL REPLICATION DATASET" is not selectable for eICU, because the
primary outcome cannot be constructed there at all. Choosing "FEASIBILITY UNCERTAIN" would misstate
the evidence — the limitation is documented, not uncertain.*

### MECHANISM DECISION

| | Level | Testable now? |
|---|---|---|
| **M1** | **LEVEL C** | **DO NOT TEST YET** |
| **M2** | **LEVEL B** | Yes, with the bounds in §9–§10 and §13 |
| **M3** | **LEVEL B** (association) / **LEVEL C** (causal) | Association only; no causal claims |
| **M4** | **LEVEL C** | **DO NOT TEST YET** |
| **M5** | **LEVEL C** | **DO NOT TEST YET** |
| **M6** | **LEVEL C** | **DO NOT TEST YET** — "Not directly testable in this dataset." |
| **M7** | **LEVEL C** (escalation effectiveness) / **LEVEL B** (retrospective detectability, renamed) | Effectiveness: **DO NOT TEST YET** |
| **M8** | **LEVEL C** | **DO NOT TEST YET** |

**Six of eight mechanisms are not testable in these datasets.** That is the finding. It should not be
worked around by substituting proxies for the missing constructs.

---

## 18. Exact Next Step

**Do not proceed to statistical analysis.** The following steps are ordered and gated.

**Step 1 — Resolve the credentialing gate (blocking; nothing else can proceed without it).**
A named investigator completes the CITI "Data or Specimens Only Research" course, applies for
PhysioNet credentialed access to MIMIC-IV, MIMIC-IV-ED and MIMIC-IV-Note, and signs the DUA. Record
the exact version, DOI and citation of each dataset **from the PhysioNet landing page** — the DOIs in
this document are deliberately left as *requires verification*.

**Step 2 — Close the remaining six `[VERIFY]` items** (schema-only queries; no modelling). Item 2 was
resolved during this audit and is retained below with its cohort consequence:

1. Exact MIMIC-IV version obtained, and its documented differences from v2.2 (row counts, `itemid`
   stability, `omr`/`poe_detail` value sets).
2. ~~MIMIC-IV-ED coverage window~~ — **RESOLVED**: MIMIC-IV-ED covers **2011–2019**, MIMIC-IV covers
   2008–2019 **[DOC]**. Carry the resulting cohort restriction (index discharges from 2011 onward
   whenever an ED-based outcome is used) into the pre-registration.
3. Whether a discharge-medication section survives deidentification in `note.discharge` (sample and
   count sections present).
4. Enumerate `d_items` for any functional, mobility, ADL, delirium or nursing-assessment concept;
   quantify coverage among ICU stays. **Expectation from this audit: little or nothing usable** — the
   official MIMIC concept library contains only GCS concepts and nothing for function, mobility,
   Braden, ADL or delirium **[DOC]**. (Absence from the concept library is strong corroboration but
   is not proof of absence from `d_items`; the enumeration still has to be run.)
5. `poe_detail` `Discharge Planning` / `Discharge When` — full value distributions and their timing
   relative to `dischtime`; determine whether either is a usable T0 anchor.
6. Empirical rule for excluding organ-donor admissions; feasibility of a partial planned-readmission
   exclusion from `procedures_icd`.
7. eICU `hospitalDischargeLocation` full value set (for the secondary construct-availability audit
   only).

**Step 3 — Pre-register the only two defensible questions** before touching outcome data:

- **Q1 (M2):** Among adults discharged alive from an index hospitalisation, how well do (A) a simple
  clinical rule, (B) a risk score, and (C) a multivariable regression, each built **only** from
  T0-legal variables, discriminate 30-day *observed* readmission or ED re-presentation?
- **Q2 (M3):** Is discharge destination associated with 30-day observed acute-care utilisation after
  adjustment for available baseline confounders — reported explicitly as an association, with a
  quantitative bias analysis for the unmeasured functional-status confounder?

The pre-registration must fix: cohort, exclusions, T0 definition, the T0-legal variable list
(explicitly excluding every item in §13), outcome definitions, windows, missing-data handling, model
specifications, and the reporting convention **"observed at BIDMC"**.

**Step 4 — Write the "cannot be tested" register.** M1, M4, M5, M6, M7 and M8 are recorded as
untestable with the specific missing variables from §14, so that the project's future data-acquisition
requirements are explicit. **Testing these mechanisms requires data that does not exist in MIMIC-IV or
eICU** — realistically claims data, a health-information exchange, or a registry with post-discharge
encounters. That is a data-acquisition problem, not an analysis problem.

**Step 5 — Do not substitute proxies for the missing constructs.** If a mechanism is not testable, the
finding of this project for that mechanism is: *not testable with available data*.

---

## Sources

Documentation consulted (retrieved 2026-09-01):

- **Official MIMIC-IV documentation**, source repository `github.com/MIT-LCP/mimic-website`
  (`docs/iv/`) — the upstream source of `mimic.mit.edu/docs/iv/`. Files used: `index.md`,
  `about/changelog.md`, `about/whatsnew.md`, `modules/hosp/{admissions,patients,transfers,services,
  omr,labevents,poe,poe_detail,prescriptions,pharmacy,emar,diagnoses_icd,procedures_icd,drgcodes,
  hcpcsevents,index}.md`, `modules/icu/{icustays,chartevents,procedureevents}.md`,
  `modules/ed/{index,edstays,triage,vitalsign,diagnosis,pyxis,medrecon}.md`,
  `modules/note/{index,discharge,discharge_detail}.md`.
- **Official MIMIC Code Repository**, `github.com/MIT-LCP/mimic-code` (checked out at its 2026-09-01
  head) — used for the dataset coverage windows in `README.md` and for the derived-concept inventory
  under `mimic-iv/concepts/`.
- **Official eICU-CRD documentation**, source repository `github.com/MIT-LCP/eicu-code`
  (`website/content/`) — the upstream source of `eicu-crd.mit.edu`. Files used:
  `eicutables/{patient,carePlanGeneral,nurseAssessment,nurseCare,note,hospital,apachePredVar,
  admissiondrug}.md`, `gettingstarted/access.md`.
- Peer-reviewed dataset papers, retrieved as full text from PubMed Central. **According to PubMed:**
  - Johnson AEW, et al. *MIMIC-IV, a freely accessible electronic health record dataset.* Scientific
    Data, 2023. [10.1038/s41597-022-01899-x](https://doi.org/10.1038/s41597-022-01899-x) (PMC9810617).
  - Pollard TJ, et al. *The eICU Collaborative Research Database, a freely available multi-center
    database for critical care research.* Scientific Data, 2018.
    [10.1038/sdata.2018.178](https://doi.org/10.1038/sdata.2018.178) (PMC6132188).

**Access limitation of this audit.** `physionet.org`, `mimic.mit.edu` and `eicu-crd.mit.edu` were
unreachable from the audit environment (blocked by the network egress proxy). The official
documentation was therefore read from its upstream source repositories, which are authoritative but
may lag the currently distributed dataset version. **Every version-specific number, value set and
`itemid` in this document must be re-verified against the PhysioNet release actually used.** No
patient-level data were accessed, and no credentials were used, requested or stored.
