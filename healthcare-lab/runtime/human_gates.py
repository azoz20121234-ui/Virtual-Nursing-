"""Human-gate enforcement for clinical, regulatory and Go/No-Go decisions."""
from dataclasses import dataclass
from enum import Enum
class GateDecision(str,Enum): PENDING="PENDING"; APPROVED="APPROVED"; REJECTED="REJECTED"
@dataclass
class HumanGatePolicy:
    decision_support_only: bool=True
    def require(self, gate:str, evidence_ids:list)->dict:
        if gate not in {"clinical","regulatory","go_no_go"}: raise ValueError("unknown_gate")
        if not evidence_ids: return {"gate":gate,"decision":GateDecision.PENDING.value,"reason":"evidence_required"}
        return {"gate":gate,"decision":GateDecision.PENDING.value,"requires_human":True,"evidence_ids":evidence_ids}
    def enforce(self, gate_record:dict, human_approved:bool)->dict:
        if not human_approved: return {**gate_record,"decision":GateDecision.REJECTED.value}
        return {**gate_record,"decision":GateDecision.APPROVED.value,"human_approved":True}
