import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from healthcare_lab.runtime.capability_resolver import CapabilityRegistry, ToolAdapter
from healthcare_lab.runtime.state_machine import ResearchStateMachine, ResearchState
from healthcare_lab.runtime.evidence_ledger import EvidenceLedger, Claim, now_utc
from healthcare_lab.runtime.provenance import ProvenanceGraph
from healthcare_lab.runtime.confidence import ConfidenceEngine
from healthcare_lab.runtime.human_gates import HumanGatePolicy, GateDecision

def test_unavailable_and_fallback():
    r=CapabilityRegistry(); r.register(ToolAdapter('primary','search',1,lambda p: (_ for _ in ()).throw(RuntimeError('down')),lambda: True)); r.register(ToolAdapter('fallback','search',2,lambda p:['ok'],lambda: True))
    x=r.execute('search',{}); assert x.ok and x.tool_id=='fallback' and x.degraded

def test_unavailable_tool():
    r=CapabilityRegistry(); x=r.execute('search',{}); assert not x.ok and x.confidence_penalty=='source_degradation'

def test_protocol_not_results():
    ledger=EvidenceLedger(); c=Claim('C1','PMID:protocol','protocol','RCT protocol','HF','remote','usual care','CV admission','NOT_AVAILABLE','n/a','abstract',now_utc(),{'retrieval':'live'},[]); ledger.add(c); assert c.effect=='NOT_AVAILABLE'

def test_conflict_penalty():
    a=ConfidenceEngine().assess(quality='HIGH',consistency='HIGH',directness='HIGH',precision='MODERATE',replication='LOW',contradiction=True)
    assert 'contradiction' in a.penalties

def test_circular_loop():
    m=ResearchStateMachine(); m.transition(ResearchState.QUESTION); m.transition(ResearchState.PICO); m.transition(ResearchState.SEARCH); assert m.transition(ResearchState.QUESTION)==ResearchState.FAILED

def test_missing_provenance():
    ledger=EvidenceLedger();
    try: ledger.add(Claim('C1','x','journal','RCT','p','i','c','o','e','LOW','abstract',now_utc(),{},[])); assert False
    except ValueError as e: assert 'provenance' in str(e)

def test_human_gate():
    p=HumanGatePolicy(); g=p.require('go_no_go',['C1']); assert g['decision']==GateDecision.PENDING.value and g['requires_human']; assert p.enforce(g,False)['decision']==GateDecision.REJECTED.value

def test_provenance_edges():
    g=ProvenanceGraph(); g.add('C1','S1','Claim->Source'); g.add('C1','I1','Claim->Inference'); g.add('I1','H1','Inference->Hypothesis'); assert not g.validate()

def test_unsupported_relation():
    try: ProvenanceGraph().add('a','b','unsupported'); assert False
    except ValueError: pass

# Fabricated PMID/DOI and unsupported recommendations are blocked by contract validation:
# identifiers must be returned by a live source adapter; recommendations require linked claims.
