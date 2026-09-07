# VALIDATION_FRAMEWORK.md — Test the riskiest assumption first

A concept is a hypothesis until an experiment survives contact with reality. This
framework turns a Solution Concept into a cheap, decisive test with a pre-committed
Go/No-Go line.

## 1. Name the riskiest assumption
Every concept rests on assumptions. Rank them by (impact if wrong) × (uncertainty).
The top one is what you test first. Common risk classes:
- **Desirability:** will the user actually use it? (adoption, trust, behavior change)
- **Feasibility:** can it be built and integrated into the workflow?
- **Clinical validity:** does it change a patient-important outcome?
- **Viability:** does the economics/reimbursement work?
- **Regulatory:** is the approval path survivable (SFDA/SDAIA)?

## 2. Choose the smallest sufficient test (evidence ladder — climb only as far as needed)
| Level | Test | Answers | Cost/time |
|-------|------|---------|-----------|
| 0 | Desk validation vs literature + official data | is this already known/solved? | hours |
| 1 | Problem interviews (clinicians, patients, ops) | is the problem real & painful? | days |
| 2 | Wizard-of-Oz / concierge MVP | will they use it if it exists? | weeks |
| 3 | Prospective pilot / single-arm feasibility | does it run in the real workflow? | months |
| 4 | Controlled study (cluster/stepped-wedge/RCT) | does it change the outcome? | months–years |
| 5 | Economic evaluation | is it worth paying for? | alongside 3–4 |

Do not run a Level-4 trial to answer a Level-1 question.

## 3. Define the metric and the line — before running
- **Primary metric:** one patient-important or decision-relevant number.
- **Guardrail metrics:** safety / equity / workflow burden (what must NOT get worse).
- **Go / Pivot / No-Go thresholds:** committed in advance, in writing.
- **Sample & duration:** enough to see the effect you'd act on (not p-hacked).

## 4. Validity discipline
- Prefer patient-important outcomes; if using a surrogate, justify and label it.
- Name the confounders and how the design handles them.
- Pre-register where it matters (PROSPERO/ClinicalTrials.gov) — and practice what the
  research protocol preaches.
- State external validity: will a positive pilot generalize to the Saudi system?

## 5. Output: Validation Plan
```
Riskiest assumption:
Test level & design:
Population / setting:
Primary metric:
Guardrail metrics:
Go / Pivot / No-Go thresholds:   (pre-committed)
Duration & sample:
Cost order-of-magnitude:
What a Go unlocks next:
```

## Principle
The goal of validation is not to prove you are right. It is to find out cheaply
whether you are wrong, before it gets expensive.
