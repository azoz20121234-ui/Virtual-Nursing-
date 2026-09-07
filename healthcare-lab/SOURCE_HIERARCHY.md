# SOURCE_HIERARCHY.md — Where to look, and in what order

Priority is **primary and authoritative over secondary and derivative**. When the
original is reachable, never rest a claim on an article that summarizes it.

## Tier 0 — Registries & primary data (ground truth for "what exists / what was tested")
- **ClinicalTrials.gov** (`Clinical_Trials` MCP) — trial existence, design, status,
  enrollment, endpoints, sponsor. Real NCT IDs only.
- **PROSPERO** — systematic review protocols (via WebFetch).

## Tier 1 — Aggregate appraised evidence (best first stop for "what do we know")
- **Cochrane Library** — systematic reviews (WebSearch/WebFetch to cochranelibrary.com).
- **PubMed / MEDLINE** (`PubMed` MCP) — filter to `Systematic Review[Publication Type]`,
  `Meta-Analysis[Publication Type]`, `Guideline[Publication Type]`.

## Tier 2 — Guidelines & official health bodies (for "what to do" and regulation)
- **WHO**, **NICE**, **CDC**, **USPSTF**, **FDA** (device/drug status), **EMA**.
- Fetch the primary guideline page (WebFetch), not a news summary of it.

## Tier 3 — Primary studies
- Individual RCTs, cohort, case-control, diagnostic accuracy, economic evaluations,
  qualitative studies — via PubMed. Pull full text where OA
  (`PubMed.get_full_text_article`) or the publisher link.

## Tier 4 — Saudi-specific official sources (mandatory for the Saudi layer)
- **Saudi MOH** (moh.gov.sa) — programs, statistics, Seha Virtual Hospital.
- **Saudi FDA (SFDA)** (sfda.gov.sa) — device/drug/software-as-medical-device regulation.
- **SDAIA / NHIC / SHC / CBAHI** — data, AI governance, accreditation.
- **Saudi Health Council, MoH statistical yearbook**, local peer-reviewed studies
  (Saudi Med J, Ann Saudi Med) via PubMed with `Saudi Arabia` filter.

## Tier 5 — Triangulation aids (never the sole basis of a claim)
- **Consensus**, **Scite** (Smart Citations, retraction checks), **Elicit** — use to
  find and stress-test, then confirm against the primary record before citing.

## Tier 6 — Lowest trust
- Preprints (label as such), narrative reviews, expert blogs, vendor material.

---

## Retrieval rules
1. Start at the tier that matches the question class (see RESEARCH_PROTOCOL.md §1).
2. For any therapy/prevention question, reach Tier 1 before concluding.
3. Every Saudi regulatory or system claim needs a Tier-4 source or an explicit
   `hypothesis / needs local verification` label.
4. Log every source's tier in the ledger — it feeds the confidence model.
5. If a higher tier is unreachable (tool down / paywall), drop to a lower tier,
   **say so**, and **downgrade confidence** (see TOOL_ADAPTERS.md).
