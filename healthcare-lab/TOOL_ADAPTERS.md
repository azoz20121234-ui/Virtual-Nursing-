# TOOL_ADAPTERS.md — Capability layer (verified, not assumed)

The agent is **not** hard-wired to one search tool. This file is the adapter layer
that sits between the Research Protocol and the actual tools, so a dead tool degrades
the investigation gracefully instead of breaking it — and always *declares* the
degradation and lowers confidence.

## Architecture (separation of concerns)

```
Agent Logic (SOUL, AGENTS)
      ↓
Research Protocol (RESEARCH_PROTOCOL)
      ↓
Tool Adapters  ← THIS FILE (capability registry + fallback routing)
      ↓
Evidence Layer (EVIDENCE_LEDGER)
      ↓
Report Layer (REPORT_TEMPLATE)
```

The protocol asks for a *capability* ("find appraised evidence"), not a *tool*
("call PubMed"). The adapter maps capability → best available verified tool, with a
fallback chain. If it falls back, it stamps the ledger row `source_tier_degraded: true`.

## Capability → tool map

| Capability | Primary | Fallback 1 | Fallback 2 | On total failure |
|------------|---------|-----------|-----------|------------------|
| Biomedical literature search | `PubMed.search_articles` | `WebSearch` (site:pubmed / cochrane) | — | State "search capability degraded", cap confidence at Low |
| Article metadata / DOI | `PubMed.get_article_metadata` | `WebFetch` (doi.org) | — | Mark `access: unverified`, do not assert findings |
| Full text | `PubMed.get_full_text_article` | `WebFetch` (OA URL) | publisher link | Mark `access: abstract-only` |
| Clinical trials | `Clinical_Trials.search_trials` + `get_trial_details` | `WebSearch` (clinicaltrials.gov) | — | State trials landscape unverified |
| Evidence triangulation | `Consensus.search` | `Scite.search_literature` | `Elicit.search_papers` | Skip; note "triangulation unavailable" |
| Citation context / retraction | `Scite.search_literature` | `WebFetch` | — | Note retraction status unchecked |
| Guidelines & official bodies | `WebSearch` + `WebFetch` | — | — | State guideline layer incomplete |
| Saudi official sources | `WebSearch`+`WebFetch` (moh/sfda/sdaia .gov.sa) | — | — | Saudi layer = hypothesis only |

## VERIFIED capability status — 2026-09-07 (this session, tested live)

> This is a *measurement*, not an assumption. Re-verify at the start of each session;
> tool quotas and plans change. Method: one minimal read-only call each.

| Tool | Status | Evidence of test | Limits found |
|------|--------|------------------|--------------|
| `PubMed.search_articles` / `get_article_metadata` | ✅ WORKING | returned real PMIDs + DOIs (e.g. 24862840 → 10.7326/M14-0083) | none hit; requires PubMed attribution + DOI links |
| `Clinical_Trials.search_trials` | ✅ WORKING | 242 HF-telemonitoring trials, real NCT IDs | — |
| `WebSearch` | ✅ WORKING | returned Seha Virtual Hospital + PMID 41081638 | US-only index |
| `WebFetch` | ✅ ASSUMED-OK | built-in; not independently failed | 15-min cache; no auth URLs |
| `Elicit.search_papers` | ❌ UNAVAILABLE | `api_access_denied` — account plan lacks API | needs paid plan |
| `Consensus.search` | ❌ EXHAUSTED | "used all 30 searches this month; resets Oct 1" | 30/mo free cap |
| `Scite.search_literature` | ❌ EXHAUSTED | "reached monthly MCP usage limit (25 calls); resets Oct 1" | 25/mo free cap |

**Operating consequence for this period:** the verified primary-source core is
**PubMed + ClinicalTrials.gov + WebSearch/WebFetch**. This is sufficient for Tier 0–4
evidence. The triangulation aids (Consensus/Scite/Elicit) are **down**, so
cross-database triangulation is degraded — where a claim would normally be
triangulated across engines, cap incremental confidence and say so.

## Rule
Never report a tool as available because its name appears in configuration.
"Available" = a real, non-destructive call succeeded this session.
