import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from capability_resolver import CapabilityRegistry, ToolAdapter
from state_machine import ResearchStateMachine, ResearchState
from evidence_ledger import EvidenceLedger, Claim, now_utc
from provenance import ProvenanceGraph
from confidence import ConfidenceEngine
from human_gates import HumanGatePolicy, GateDecision
from validation import validate_identifier, validate_effect_for_source, validate_recommendation

def test_unavailable_and_fallback():
    r=CapabilityRegistry(); r.register(ToolAdapter('primary','search',1,lambda p: (_ for _ in ()).throw(RuntimeError('down')),lambda: True)); r.register(ToolAdapter('fallback','search',2,lambda p:['ok'],lambda: True))
    x=r.execute('search',{}); assert x.ok and x.tool_id=='fallback' and x.degraded

def test_unavailable_tool():
    r=CapabilityRegistry(); x=r.execute('search',{}); assert not x.ok and x.confidence_penalty=='source_degradation'

def test_protocol_not_results():
    try: validate_effect_for_source('protocol','RR 0.80') ; assert False
    except ValueError as e: assert 'protocol' in str(e)

def test_fabricated_identifier():
    try: validate_identifier('999999999', {'verified_identifiers':['12345']}); assert False
    except ValueError as e: assert 'fabricated' in str(e)

def test_conflict_penalty():
    a=ConfidenceEngine().assess(quality='HIGH',consistency='HIGH',directness='HIGH',precision='MODERATE',replication='LOW',contradiction=True)
    assert 'contradiction' in a.penalties

def test_circular_loop():
    m=ResearchStateMachine(); m.transition(ResearchState.QUESTION); m.transition(ResearchState.PICO); m.transition(ResearchState.SEARCH); assert m.transition(ResearchState.QUESTION)==ResearchState.FAILED

def test_missing_provenance():
    ledger=EvidenceLedger()
    try: ledger.add(Claim('C1','x','journal','RCT','p','i','c','o','e','LOW','abstract',now_utc(),{},[])); assert False
    except ValueError as e: assert 'provenance' in str(e)

def test_human_gate():
    p=HumanGatePolicy(); g=p.require('go_no_go',['C1']); assert g['decision']==GateDecision.PENDING.value and g['requires_human']; assert p.enforce(g,False)['decision']==GateDecision.REJECTED.value

def test_human_gate_violation():
    try: validate_recommendation({'supporting_claim_ids':['C1'],'requires_human_gate':True}); assert False
    except ValueError as e: assert 'human_gate' in str(e)

def test_unsupported_recommendation():
    try: validate_recommendation({}); assert False
    except ValueError as e: assert 'unsupported' in str(e)

def test_provenance_edges():
    g=ProvenanceGraph(); g.add('C1','S1','Claim->Source'); g.add('C1','I1','Claim->Inference'); g.add('I1','H1','Inference->Hypothesis'); assert not g.validate()

def test_unsupported_relation():
    try: ProvenanceGraph().add('a','b','unsupported'); assert False
    except ValueError: pass
