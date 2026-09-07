# RESEARCH_PROTOCOL.md — The Research Pipeline & Anti-Hallucination Law

The full pipeline, stage by stage, with the hard rules that govern each.

```
USER PROBLEM → PROBLEM FRAMING → RESEARCH QUESTION → PICO/PICOT →
SEARCH STRATEGY → EVIDENCE RETRIEVAL → SCREENING → QUALITY APPRAISAL →
DATA EXTRACTION → EVIDENCE SYNTHESIS → CONTRADICTION ANALYSIS → RED TEAM →
SAUDI CONTEXT → RESEARCH/EVIDENCE GAP → INNOVATION OPPORTUNITY →
SOLUTION CONCEPT → VALIDATION PLAN → DECISION BRIEF
```

---

## 0. Anti-Hallucination Law (read first, applies everywhere)

These are absolute. Violating any one invalidates the entire investigation.

1. Do not invent a study, author, journal, year, DOI, PMID, NCT ID, or statistic.
2. Every identifier written to the ledger must come from a tool result in **this**
   session. If you cannot produce the identifier, you did not read the study.
3. Do not claim to have read full text you only saw as an abstract. Mark
   `access: abstract-only` vs `access: full-text` in the ledger.
4. `association ≠ causation`. Observational data supports association; causal
   language requires an appropriate design and is still hedged.
5. `statistical significance ≠ clinical significance`. Report both the p-value/CI
   *and* whether the effect size matters to a patient.
6. `surrogate outcome ≠ patient-important outcome`. Flag surrogates (HbA1c, LDL,
   tumor markers) as surrogates.
7. One study ≠ a fact. State n, and whether it has been replicated.
8. A preprint is labeled `PREPRINT — not peer-reviewed` every time it is used.
9. If evidence is not found: say **"Evidence not found"** and stop pretending.
10. If evidence is thin/mixed: say **"Insufficient evidence"** and quantify why.
11. If studies conflict: **show the conflict** (CONTRADICTION ANALYSIS), do not average it away.

> When in doubt between sounding complete and being honest, be honest.

---

## Stage-by-stage

### 1. Problem Framing
- Restate the user's problem in one sentence. Strip ambiguity.
- Classify: therapy / diagnosis / prognosis / prevention / etiology / economics /
  implementation / patient experience. The class determines the ideal study design.
- Name the decision the user is actually trying to make.

### 2. Research Question
- Convert to a single, answerable question. If the ask is broad, decompose into
  2–4 sub-questions and say so.

### 3. PICO / PICOT
- **P**opulation, **I**ntervention/exposure, **C**omparator, **O**utcome,
  (**T**ime, and study **T**ype target for therapy questions).
- For diagnosis: use PIRT (Population, Index test, Reference standard, Target).
- Make the outcome patient-important where possible; if only surrogates exist, note it.

### 4. Search Strategy
- Concepts → synonyms → controlled vocabulary (MeSH/Emtree) → boolean structure.
- Record the actual query string(s) used. The brief must be reproducible.
- Pre-declare inclusion/exclusion criteria (design, date window, population, language).

### 5. Evidence Retrieval  (tools — see SOURCE_HIERARCHY.md for order)
- Prefer primary/aggregate sources. Available MCP/tools in this runtime:
  - `PubMed` (search_articles, get_article_metadata, get_full_text_article, find_related_articles)
  - `Clinical_Trials` (search_trials, get_trial_details, analyze_endpoints) — ClinicalTrials.gov
  - `Consensus` / `Scite` / `Elicit` — evidence aggregation & citation context (use to
    triangulate, never as the sole source of a claim).
  - `WebSearch` / `WebFetch` — for guidelines & official bodies (WHO, NICE, CDC, FDA,
    Cochrane, Saudi MOH, SFDA). Fetch the primary page, not a blog about it.
- Log every query and the count of hits. Retrieval is auditable.

### 6. Screening
- Apply pre-declared criteria. Record kept vs excluded with a one-line reason.
- Deduplicate. Note total screened → included.

### 7. Quality Appraisal  → hand to Role B, use EVIDENCE_RUBRIC.md
- Right appraisal tool per design (RoB 2, ROBINS-I, AMSTAR-2, QUADAS-2, GRADE, etc.).
- Output a risk-of-bias judgment per study.

### 8. Data Extraction → Evidence Ledger (EVIDENCE_LEDGER.md)
- One ledger row per important claim, fully populated. No row, no claim.

### 9. Evidence Synthesis
- Synthesize *by outcome*, weighted by quality — not a study-by-study recap.
- State direction, magnitude, consistency, and certainty (GRADE-style).

### 10. Contradiction Analysis
- Where studies disagree, present both sides and the likely reason (population,
  dose, design, era, funding). Do not resolve a genuine conflict by fiat.

### 11. Red Team → RED_TEAM.md (mandatory gate before conclusions).

### 12. Saudi Context → SAUDI_APPLICABILITY.md.

### 13. Gaps → 14. Innovation → 15. Concept → 16. Validation → 17. Brief.
- Handoff to INNOVATION_ENGINE.md and VALIDATION_FRAMEWORK.md, output via REPORT_TEMPLATE.md.

---

## Escalation triggers (ask the user)
- The question is clinically safety-critical and evidence is thin.
- Two equally valid framings would produce different investigations.
- A Saudi regulatory claim cannot be verified against an official source.
- The innovation direction implies a major resource commitment.
