# EVIDENCE_RUBRIC.md — Evidence Hierarchy & Confidence Model

Two separate things live here: (1) the **hierarchy** of study designs, and (2) the
**confidence model** that decides how much to trust a claim. They are not the same,
and that distinction is the whole point.

---

## 1. Evidence hierarchy (design → default ceiling on certainty)

Ranked roughly by ability to support a causal therapeutic claim. Design sets a
**ceiling**, never the final score.

| Tier | Design | Best answers | Default ceiling |
|------|--------|--------------|-----------------|
| 1 | Clinical practice guidelines (evidence-based, graded) | what to do now | High* |
| 1 | Systematic review + meta-analysis of RCTs | therapy effect | High |
| 2 | Individual RCT | therapy effect (single) | Moderate–High |
| 3 | Cohort study | prognosis, harm, exposure | Moderate |
| 4 | Case-control | rare outcomes, etiology | Low–Moderate |
| 5 | Cross-sectional | prevalence, association | Low |
| 5 | Diagnostic accuracy study | test performance | design-specific |
| 5 | Economic evaluation | cost-effectiveness | design-specific |
| 6 | Qualitative research | experience, barriers, why | high for *its* question |
| 7 | Case series / case report | signal, novelty | Very low |
| 7 | Protocol (registered, no results) | what is coming | none (no result) |
| 8 | Preprint | provisional | none until appraised |
| 9 | Expert opinion / narrative review | context, framing | Very low |

*A guideline's strength depends on its evidence base and rigor of development
(appraise with AGREE II), not on its authority.

**Rule:** never emit the phrase "strong evidence" mechanically from tier alone.
Qualitative research is *high* evidence for a lived-experience question and *not
applicable* for an effect-size question. Match design to question class first.

---

## 2. Risk-of-bias / appraisal tool per design

| Design | Appraisal instrument |
|--------|----------------------|
| RCT | Cochrane RoB 2 |
| Non-randomized intervention | ROBINS-I |
| Systematic review | AMSTAR-2 |
| Diagnostic accuracy | QUADAS-2 |
| Cohort/case-control | Newcastle–Ottawa Scale |
| Guideline | AGREE II |
| Overall certainty across body of evidence | GRADE |
| Prognosis | QUIPS |

Name the instrument used per study in the ledger's `Limitations` reasoning.

---

## 3. Confidence model (GRADE-inspired, applied per claim)

Start at the design ceiling, then move the score:

**Downgrade** for:
- Risk of bias (poor randomization, no blinding, high attrition, selective reporting)
- Inconsistency (heterogeneous results across studies, high I²)
- Indirectness (population/intervention/outcome differs from the question; surrogate outcomes)
- Imprecision (wide CI, small n, few events)
- Publication bias (asymmetric funnel, industry-only positive trials, unregistered)

**Upgrade** (observational only) for:
- Large effect size
- Dose–response gradient
- Plausible confounding would reduce, not create, the observed effect

**Final confidence labels:**
- **High** — further research very unlikely to change the estimate.
- **Moderate** — further research may change the estimate.
- **Low** — further research likely to change the estimate.
- **Very Low** — estimate is very uncertain.
- **Evidence not found / Insufficient evidence** — valid outputs; use them.

Every confidence label in the brief must trace to a one-line reason
("Moderate: single well-conducted RCT, but surrogate outcome and n=140").

---

## 4. Distinctions that must never collapse
- Association vs causation.
- Statistical significance (p, CI) vs clinical significance (does it matter to a patient?).
- Surrogate outcome vs patient-important outcome.
- Efficacy (ideal trial conditions) vs effectiveness (real world).
- Relative effect (RR, HR) vs absolute effect (ARR, NNT) — always give absolute too.
- Internal validity (is it true here?) vs external validity (does it transfer?).
