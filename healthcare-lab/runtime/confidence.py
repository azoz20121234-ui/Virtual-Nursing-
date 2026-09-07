"""Interpretable ordinal confidence; deliberately avoids false precision."""
from dataclasses import dataclass
from typing import Dict, List

LEVELS=("VERY_LOW","LOW","MODERATE","HIGH")
@dataclass
class ConfidenceAssessment:
    level: str
    positives: List[str]
    penalties: List[str]
    rationale: str

class ConfidenceEngine:
    def assess(self, *, quality: str, consistency: str, directness: str, precision: str,
                replication: str, risk_of_bias: bool=False, missing_full_text: bool=False,
                source_degradation: bool=False, contradiction: bool=False, indirectness: bool=False)->ConfidenceAssessment:
        vals={k:v for k,v in {"quality":quality,"consistency":consistency,"directness":directness,"precision":precision,"replication":replication}.items()}
        score=sum(LEVELS.index(v) for v in vals.values() if v in LEVELS)
        positives=[f"{k}={v}" for k,v in vals.items() if v in LEVELS]
        penalties=[]
        for enabled,label in [(risk_of_bias,"risk_of_bias"),(missing_full_text,"missing_full_text"),(source_degradation,"source_degradation"),(contradiction,"contradiction"),(indirectness,"indirectness")]:
            if enabled: score-=1; penalties.append(label)
        level=LEVELS[max(0,min(len(LEVELS)-1,round(score/5)))]
        return ConfidenceAssessment(level,positives,penalties,
            "Ordinal assessment only; no numeric probability is claimed. Base dimensions are balanced against explicit penalties.")
