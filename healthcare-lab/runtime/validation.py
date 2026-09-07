"""Safety validators for identifiers, protocol/results separation and recommendation provenance."""
import re

def validate_identifier(identifier: str, source_payload: dict) -> None:
    if not identifier or not source_payload.get('verified_identifiers') or identifier not in source_payload['verified_identifiers']:
        raise ValueError('fabricated_or_unverified_identifier')

def validate_effect_for_source(source_type: str, effect: str) -> None:
    if source_type.lower() in {'protocol','trial_protocol','design_paper'} and effect not in {'NOT_AVAILABLE','n/a',None}:
        raise ValueError('protocol_mistaken_for_results')

def validate_recommendation(recommendation: dict) -> None:
    if not recommendation.get('supporting_claim_ids'):
        raise ValueError('unsupported_recommendation')
    if recommendation.get('requires_human_gate') and not recommendation.get('human_gate'):
        raise ValueError('human_gate_violation')

def validate_pmid(pmid: str) -> bool:
    return bool(re.fullmatch(r'\d{1,9}', str(pmid)))
