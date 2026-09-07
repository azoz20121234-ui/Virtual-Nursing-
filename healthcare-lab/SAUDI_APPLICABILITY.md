# SAUDI_APPLICABILITY.md — From global evidence to Saudi reality

Global evidence does not transfer to Saudi Arabia by default. This layer forces the
translation to be explicit and sourced, and to separate three things that are
constantly confused:

```
EVIDENCE (what the studies show, globally)
   ≠
SAUDI-SPECIFIC INFERENCE (what an official Saudi source establishes)
   ≠
HYPOTHESIS (what we suspect about Saudi Arabia but have not verified)
```

Every Saudi statement in a brief must be tagged as one of these three.

## The applicability funnel (run in order)

```
Global Evidence
   ↓  is the effect real and clinically meaningful? (from appraisal)
Clinical Applicability
   ↓  does the studied population match Saudi patients? (age, comorbidity, disease mix)
Healthcare Workflow
   ↓  where does this sit in the actual Saudi care pathway? (PHC → hospital → virtual)
Saudi Context
   ↓  system realities: MOH clusters, Seha Virtual Hospital, workforce, Saudization, language, geography
Regulatory Context
   ↓  SFDA (devices / software-as-medical-device), SDAIA (AI & data), NPHIES/data residency, CBAHI accreditation
Operational Feasibility
   ↓  cost, staffing, connectivity, reimbursement, change management
Innovation Opportunity
```

## Saudi factors to check every time
- **Demographics/disease burden:** younger population, high prevalence of T2D,
  obesity, road-traffic trauma; verify specifics against MOH data, never assume.
- **System structure:** MOH health clusters, model of care under Vision 2030,
  Health Sector Transformation Program; **Seha Virtual Hospital** as the national
  virtual-care backbone.
- **Workforce:** reliance on expatriate nurses/physicians, Saudization targets,
  nurse-to-patient ratios — a nurse-led intervention's feasibility hinges on this.
- **Regulatory:** SFDA for medical devices and SaMD; SDAIA/PDPL for data protection
  and AI governance; data residency; CBAHI accreditation standards.
- **Language/culture:** Arabic-first design, gender considerations in care delivery,
  family-centered decision-making, health literacy.
- **Access/geography:** urban–rural divide, connectivity outside metros.

## Rules
1. Any claim about Saudi regulation, system, or statistics needs a **Tier-4 official
   source** (SOURCE_HIERARCHY) retrieved this session, or the tag `HYPOTHESIS`.
2. Never write "this works in Saudi Arabia" from a global trial. Write "global
   evidence shows X (EVIDENCE); applicability to Saudi patients is plausible because
   Y (INFERENCE, sourced); whether it holds locally is untested (HYPOTHESIS → needs
   local validation)."
3. Absence of Saudi-specific evidence is itself a finding — often the research gap.
4. Descriptive Saudi data (e.g. utilization/satisfaction) is **not** comparative
   effectiveness data. Do not upgrade it into an outcome claim.
