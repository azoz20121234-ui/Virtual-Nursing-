"""Canonical structured evidence ledger; Markdown is a presentation layer."""
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import json

REQUIRED=("claim_id","source_id","source_type","study_design","population","intervention",
          "comparator","outcome","effect","certainty","access_level","retrieval_timestamp",
          "provenance","contradictions")

@dataclass
class Claim:
    claim_id: str
    source_id: str
    source_type: str
    study_design: str
    population: Any
    intervention: Any
    comparator: Any
    outcome: Any
    effect: Any
    certainty: str
    access_level: str
    retrieval_timestamp: str
    provenance: Dict[str,Any]
    contradictions: List[str]

class EvidenceLedger:
    def __init__(self): self.claims: Dict[str,Claim]={}
    def add(self, claim: Claim):
        missing=[k for k in REQUIRED if not hasattr(claim,k)]
        if missing: raise ValueError(f"missing_fields:{','.join(missing)}")
        if not claim.provenance: raise ValueError("missing_provenance")
        if claim.claim_id in self.claims: raise ValueError("duplicate_claim_id")
        self.claims[claim.claim_id]=claim
    def validate(self)->List[str]:
        errors=[]
        for cid,c in self.claims.items():
            for field in REQUIRED:
                if getattr(c,field,None) is None: errors.append(f"{cid}:{field}")
        return errors
    def to_json(self)->str:
        return json.dumps([asdict(c) for c in self.claims.values()],ensure_ascii=False,indent=2)
    def markdown(self)->str:
        rows=["| claim_id | source_id | design | outcome | effect | certainty | access | contradictions |","|---|---|---|---|---|---|---|---|"]
        for c in self.claims.values(): rows.append(f"| {c.claim_id} | {c.source_id} | {c.study_design} | {c.outcome} | {c.effect} | {c.certainty} | {c.access_level} | {', '.join(c.contradictions) or '—'} |")
        return "\n".join(rows)

def now_utc(): return datetime.now(timezone.utc).isoformat()
