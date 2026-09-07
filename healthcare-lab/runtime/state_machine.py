"""Bounded research state machine with explicit retries, stopping rules and gates."""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

class ResearchState(str, Enum):
    FRAME="FRAME"; QUESTION="QUESTION"; PICO="PICO/PICOT"; SEARCH="SEARCH"; SCREEN="SCREEN"
    APPRAISE="APPRAISE"; EXTRACT="EXTRACT"; SYNTHESIZE="SYNTHESIZE"; CONTRADICTION="CONTRADICTION"
    RED_TEAM="RED_TEAM"; SAUDI="SAUDI"; GAP="GAP"; INNOVATION="INNOVATION"; VALIDATION="VALIDATION"; DECISION="DECISION"
    RETRY="RETRY"; FAILED="FAILED"; HUMAN_GATE="HUMAN_GATE"

ORDER=[ResearchState.FRAME,ResearchState.QUESTION,ResearchState.PICO,ResearchState.SEARCH,ResearchState.SCREEN,
       ResearchState.APPRAISE,ResearchState.EXTRACT,ResearchState.SYNTHESIZE,ResearchState.CONTRADICTION,
       ResearchState.RED_TEAM,ResearchState.SAUDI,ResearchState.GAP,ResearchState.INNOVATION,
       ResearchState.VALIDATION,ResearchState.DECISION]

@dataclass
class ResearchStateMachine:
    max_iterations: int = 3
    max_retries_per_state: int = 2
    state: ResearchState = ResearchState.FRAME
    iterations: int = 0
    retries: Dict[str,int] = field(default_factory=dict)
    history: List[str] = field(default_factory=list)
    stopped: bool = False
    stop_reason: Optional[str] = None

    def transition(self, target: ResearchState, *, success: bool=True, reason: str="") -> ResearchState:
        if self.stopped: return self.state
        if self.iterations >= self.max_iterations * len(ORDER):
            return self.fail("max_iterations_exceeded")
        if not success:
            key=target.value; self.retries[key]=self.retries.get(key,0)+1
            if self.retries[key] > self.max_retries_per_state: return self.fail(f"retry_limit:{key}")
            self.history.append(f"RETRY:{key}:{reason}"); return ResearchState.RETRY
        if target not in ORDER: return self.fail("invalid_state")
        current_index=ORDER.index(self.state) if self.state in ORDER else -1
        target_index=ORDER.index(target)
        if target_index <= current_index and target != ResearchState.SEARCH:
            return self.fail("circular_transition")
        self.state=target; self.iterations+=1; self.history.append(target.value); return self.state

    def require_human_gate(self, gate: str) -> ResearchState:
        self.state=ResearchState.HUMAN_GATE; self.history.append(f"HUMAN_GATE:{gate}"); return self.state

    def approve_gate(self, approved: bool, gate: str) -> ResearchState:
        if not approved: return self.fail(f"human_gate_rejected:{gate}")
        if self.history and self.history[-1] == f"HUMAN_GATE:{gate}": self.history.pop()
        self.state=ResearchState.DECISION if gate in {"clinical","regulatory","go_no_go"} else self.state
        return self.state

    def stop_if_complete(self, evidence_sufficient: bool=False) -> bool:
        if self.state == ResearchState.DECISION and evidence_sufficient:
            self.stopped=True; self.stop_reason="decision_reached"; return True
        return False

    def fail(self, reason: str) -> ResearchState:
        self.state=ResearchState.FAILED; self.stopped=True; self.stop_reason=reason; self.history.append(f"FAILED:{reason}"); return self.state
