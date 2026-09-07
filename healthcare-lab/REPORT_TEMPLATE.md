# REPORT_TEMPLATE.md — Healthcare Research & Innovation Decision Brief

The single output format. Fill every section; where a section has no content, say why
(e.g. "Evidence not found", "Insufficient evidence", "Not applicable"). Never leave a
section silently empty. Every load-bearing claim carries an identifier traceable to
the Evidence Ledger.

Traceability contract for the whole brief:
- Every **finding**: `Evidence → Source → Identifier → Finding → Confidence`.
- Every **recommendation**: `Evidence + Finding → Recommendation`.

---

```
# Healthcare Research & Innovation Decision Brief
**Problem:** …    **Date:** …    **Analyst:** Healthcare Evidence→Innovation Agent
**Verified tools this session:** …    **Degraded capabilities:** …

## 1. Executive Verdict
The one-paragraph answer + overall confidence + the single most important caveat.

## 2. Problem Definition
Restated problem, decision to be made, question class.

## 3. Research Question
The precise, answerable question (and sub-questions).

## 4. PICO / PICOT
P / I / C / O (/ T) — outcome flagged patient-important vs surrogate.

## 5. Search Strategy
Sources queried, actual query strings, date window, inclusion/exclusion, counts.
(Reproducible.)

## 6. Evidence Landscape
What kinds of evidence exist and how much; where it clusters; where it's thin.

## 7. Evidence Matrix
The ledger, summarized: one row per key claim (source, id, design, effect, confidence).

## 8. Key Findings
Synthesized by outcome, each: Evidence → Source → Identifier → Finding → Confidence.

## 9. Evidence Quality
Appraisal summary: risk of bias, consistency, directness, precision, publication bias.

## 10. Conflicting Evidence
Where studies disagree and the likely reason. Do not average away real conflict.

## 11. Limitations
Of the evidence base and of this investigation (incl. tool degradation).

## 12. Confidence Assessment
Per key claim, reasoned (GRADE-style). Overall certainty statement.

## 13. Saudi Applicability
Global Evidence / Saudi-specific Inference / Hypothesis — clearly separated & tagged.

## 14. Current Solutions
What exists today (named), and which are evidence-backed.

## 15. Unmet Needs
What remains unsolved for patient / clinician / system.

## 16. Evidence Gaps
What we don't know (missing/weak studies).

## 17. Research Gaps
The specific studies that should be run.

## 18. Innovation Opportunities
Gap-anchored opportunities (each traced to a gap + evidence).

## 19. Ranked Opportunities
The scoring matrix (INNOVATION_ENGINE) with the ranking.

## 20. Recommended Concept
The top opportunity, with the full Problem→…→Go/No-Go chain.

## 21. MVP
Smallest build that tests the riskiest assumption.

## 22. Validation Experiment
From VALIDATION_FRAMEWORK: level, design, metric, pre-committed thresholds.

## 23. Success Metrics
Primary + guardrail metrics.

## 24. Risks
Clinical, operational, regulatory, commercial.

## 25. Red-Team Findings
The adversarial pass and what it changed (downgrades / conclusion changes).

## 26. Research Learning
The teaching block(s) — raise the user's own capability.

## 27. Primary Sources
Full list with identifiers (PMID/DOI/NCT/official URL). PubMed items cited with DOI
links per attribution requirement.
```

---

## Style
Executive, critical, direct. No flattery, no padding. Lead with the verdict.
State confidence honestly. Absence of evidence is stated plainly, not disguised.
