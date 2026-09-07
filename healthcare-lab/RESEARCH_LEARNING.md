# RESEARCH_LEARNING.md — Raise the user's own capability

The agent's job is not only to research *for* the user, but to make the user a
sharper researcher, appraiser, and innovator over time. Every investigation that
touches a non-trivial method or concept must surface a **Research Learning** block.

## When to emit
- A methodological concept was load-bearing in the analysis (e.g. network
  meta-analysis, NNT, risk of bias, surrogate outcomes, publication bias, GRADE,
  stepped-wedge design, competing risks, ITT vs per-protocol).
- The user's decision hinges on interpreting a statistic correctly.
- A common misreading would have led to the wrong conclusion.

## Format (keep it tight — Apple-style, no padding)
```
### Research Learning: <Concept>
- **Concept:** one-line definition.
- **Why it matters:** what it changes about the conclusion / decision.
- **How researchers use it:** the normal, correct application.
- **How to interpret it:** what a given value/result actually means.
- **Common mistake:** the trap most people fall into.
- **How you can apply it:** a concrete move the user can make next time.
```

## Rules
1. Teach the concept that actually mattered *in this investigation*, not a random fact.
2. Prefer concepts that transfer — ones the user will meet again.
3. Be honest about limits of the method too (every method has failure modes).
4. One or two per brief is enough; depth over breadth. A wall of concepts teaches
   nothing.

## Running index
Maintain `healthcare-lab/RESEARCH_LEARNING.md` as a growing personal curriculum:
append each new concept below with the date and the investigation it came from, so
the user accumulates a compounding methods library.

---

### Learning log
<!-- Append entries here. Example seeded from the first end-to-end test: -->

- **2026-09-07 — "Telemonitoring" is not one intervention (composite-intervention trap).**
  Trials labeled "telemonitoring" range from passive vitals transmission to nurse-led
  collaborative management with consultation. Pooling them hides the fact that the
  *active ingredient* may be the human follow-up, not the device. When evidence
  "conflicts," first check whether the interventions are even the same thing. (From
  the HF virtual-nursing brief.)
