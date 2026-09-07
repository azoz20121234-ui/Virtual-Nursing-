# EVIDENCE_LEDGER.md — The traceability spine

No important claim exists outside this ledger. The model's memory is not a source.
One row per important claim. If a row cannot be filled from a retrieved source, the
claim does not go in the brief — it becomes an open question or a labeled hypothesis.

## Why this exists
A fluent paragraph can hide a fabricated fact. The ledger makes every load-bearing
statement **traceable to a real, retrieved artifact** with an identifier. It is the
single mechanism that most reduces hallucination in this system.

## Row schema (every field required, or explicitly `n/a` / `not reported`)

| Field | Meaning |
|-------|---------|
| `claim_id` | short handle, e.g. `C1` |
| `claim` | the assertion, one sentence |
| `source` | authors + year + journal |
| `identifier` | PMID / DOI / NCT / official URL — **must come from a tool result this session** |
| `tier` | SOURCE_HIERARCHY tier (0–6) |
| `study_type` | design (SR, MA, network MA, RCT, cohort, protocol, retrospective, …) |
| `population` | who (n, age, setting, country) |
| `intervention` | intervention / exposure |
| `comparator` | control / comparison |
| `outcome` | outcome measured (flag surrogate vs patient-important) |
| `effect` | direction + magnitude + CI/p (absolute where possible) |
| `confidence` | High / Moderate / Low / Very Low — with one-line reason |
| `limitations` | key threats to validity; appraisal instrument used |
| `contradicts` | claim_ids or sources that disagree |
| `applicability` | direct / indirect; transfer notes |
| `access` | full-text / abstract-only / metadata-only |
| `evidence_date` | publication date; and whether newer evidence likely exists |
| `retrieved` | tool + query that produced it (audit trail) |

## Rules
1. `identifier` is sacred. If you did not get it from a tool result in this session,
   the row is invalid. Never reconstruct a DOI/PMID from memory.
2. `access: abstract-only` forbids any claim that requires reading the full text
   (e.g. detailed subgroup effects). Say what the abstract supports, no more.
3. A **protocol/design paper** (registered, no results) can populate `intervention`
   and `outcome` but **must not** populate `effect` — it has no results. Mark it and
   say the result requires the results publication.
4. `confidence` is set by the Critical Appraiser via EVIDENCE_RUBRIC.md, never by
   study type alone.
5. Contradictions are recorded, never silently dropped.
6. Ledgers are written to `healthcare-lab/ledgers/<date>_<slug>.md` per investigation.

## Blank template (copy per row)
```
- claim_id:
  claim:
  source:
  identifier:
  tier:
  study_type:
  population:
  intervention:
  comparator:
  outcome:
  effect:
  confidence:        # + reason
  limitations:       # + appraisal tool
  contradicts:
  applicability:
  access:
  evidence_date:
  retrieved:         # tool + query
```

A worked, real example lives in `ledgers/2026-09-07_HF-virtual-nursing.md`.
