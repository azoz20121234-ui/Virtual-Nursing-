# Implementation Readiness Report
**Date:** 2026-09-07 · **Prepared before build, gating the implementation.**

## 1. Direct Evidence (what the repo actually contains — verified by inspection)
`git` + filesystem scan of the repository on branch `claude/healthcare-research-innovation-lab-l6edy0`:
- Only two tracked files: **`index.html`** (552-line static "Virtual Nursing Command Center" dashboard demo) and **`.gitkeep`**.
- **No OpenClaw** present. No `agents/`, no `skills/`, no MCP configuration files, no
  `CLAUDE.md`, no workflows or prompt library — confirmed by `find` for `*openclaw*`,
  `CLAUDE.md`, `*.mcp*`, `.claude*` (all empty).
- Conclusion: there is nothing called "OpenClaw" to build *inside*; the premise "build a
  layer on top of OpenClaw" refers to the runtime, not an artifact in this repo.

## 2. Verified Capabilities (tested live this session — NOT assumed from config)
Method: one minimal, read-only call per tool.

| Tool | Result | Proof |
|------|--------|-------|
| PubMed `search_articles` / `get_article_metadata` | ✅ WORKING | real PMIDs + DOIs returned (e.g. 24862840 → 10.7326/M14-0083) |
| ClinicalTrials.gov `search_trials` | ✅ WORKING | 242 HF trials, real NCT IDs |
| WebSearch | ✅ WORKING | Seha Virtual Hospital + PMID 41081638 |
| WebFetch | ✅ assumed-OK (built-in) | not independently failed |
| Elicit `search_papers` | ❌ UNAVAILABLE | `api_access_denied` — account plan lacks API |
| Consensus `search` | ❌ EXHAUSTED | "used all 30 searches this month; resets Oct 1" |
| Scite `search_literature` | ❌ EXHAUSTED | "reached monthly MCP usage limit (25 calls)" |

**3 of 7 named research tools are non-functional right now.** This is exactly why
capability was tested rather than trusted — and why the architecture must degrade gracefully.

## 3. Environment Interpretation
The real runtime is **Claude Code** (the user's "OpenClaw"), with a verified
primary-source research core of **PubMed + ClinicalTrials.gov + WebSearch/WebFetch**.
This core is sufficient for Tier 0–4 evidence (registries, appraised syntheses, primary
studies, guidelines, Saudi official sources). The triangulation aids are down until Oct 1.

## 4. Architecture Decision
Build the **Autonomous Healthcare Research & Innovation Agent** as a **governance +
skill layer on top of Claude Code**, not a reconstruction of OpenClaw and not invented
components. Layered separation of concerns:
```
Agent Logic (SOUL, AGENTS) → Research Protocol → Tool Adapters (capability map + fallback)
→ Evidence Layer (Ledger) → Report Layer (Decision Brief)
```
Rationale: highest reliability + evidence traceability + maintainability + extensibility
at least complexity. A single agent with explicit reasoning stages (not 4 sub-agents)
preserves one Evidence Ledger and one confidence model. Routing by *capability* (not
tool name) makes it tool-agnostic and survivable when a tool dies.

## 5. Reusable Components
- The runtime's MCP research tools (PubMed, ClinicalTrials.gov, WebSearch/WebFetch).
- Claude Code's native **skill** mechanism (auto-discovery) and **CLAUDE.md** auto-load.
- `index.html` — kept as-is (thematic only; not wired into the agent).

## 6. Missing Components (built in this task)
- All agent logic, protocol, evidence discipline, Saudi layer, innovation & validation
  frameworks, report template, tool-adapter/capability registry, and the invokable skill.

## 7. Files to Create
`CLAUDE.md`; `.claude/skills/healthcare-research-lab/SKILL.md`; and under `healthcare-lab/`:
`SOUL.md, AGENTS.md, RESEARCH_PROTOCOL.md, EVIDENCE_RUBRIC.md, SOURCE_HIERARCHY.md,
TOOL_ADAPTERS.md, EVIDENCE_LEDGER.md, RED_TEAM.md, SAUDI_APPLICABILITY.md,
INNOVATION_ENGINE.md, VALIDATION_FRAMEWORK.md, RESEARCH_LEARNING.md, REPORT_TEMPLATE.md`;
plus `ledgers/`, `briefs/`, `reports/`.

## 8. Files to Modify
**None.** `index.html` is left untouched. No existing agent/skill exists to modify or break.

## 9. Risks
- **Tool volatility** (quotas/plans) → mitigated by TOOL_ADAPTERS capability routing +
  confidence downgrade + per-session re-verification.
- **Hallucinated citations** → mitigated by the Evidence Ledger "retrieved-not-remembered"
  law and abstract-only access flags.
- **Saudi over-claiming** → mitigated by the three-layer separation (Evidence/Inference/Hypothesis).
- **Scope creep breaking the demo** → mitigated by not touching `index.html` + backup.

## 10. Backup Plan
- Git tag `backup/pre-healthcare-lab-2026-09-07` at pre-build HEAD.
- Snapshot copy `.backup/index.html.bak`.
- All work on the feature branch; `index.html` untouched; revert = checkout the tag.

## 11. Implementation Plan (phased)
P1 Core agent (SOUL/AGENTS/PROTOCOL/SKILL/CLAUDE) → P2 Evidence Ledger → P3 Appraisal
(RUBRIC/SOURCE_HIERARCHY/TOOL_ADAPTERS) → P4 Red Team → P5 Saudi layer → P6 Innovation
engine → P7 Validation engine → P8 End-to-end live test. Verify after each.

## 12. Test Plan
Run one **real** health problem end-to-end (not synthetic): HF virtual-nursing/readmission.
Prove: Search → Retrieve → Extract → Appraise → Synthesize → Contradict → Red-Team →
Saudi context → Gap → Opportunity → MVP → Validation, with every claim traced to a real
retrieved identifier. Manually review for hallucination; correct; document limitations.

**Readiness verdict: GO.** No blocking issue. Verified core tools are sufficient; the
degraded tools are handled by design.
