"""Small typed provenance graph with explicit edge vocabulary."""
from dataclasses import dataclass
from typing import Dict, List

ALLOWED={"Claim->Source","Claim->Supporting Evidence","Claim->Contradicting Evidence","Claim->Inference",
         "Inference->Hypothesis","Hypothesis->Innovation","Innovation->Validation","Innovation->Decision"}
@dataclass(frozen=True)
class Edge:
    source: str; target: str; relation: str
class ProvenanceGraph:
    def __init__(self): self.edges: List[Edge]=[]
    def add(self, source:str,target:str,relation:str):
        if relation not in ALLOWED: raise ValueError(f"unsupported_relation:{relation}")
        self.edges.append(Edge(source,target,relation))
    def validate(self)->List[str]:
        return [] if self.edges else ["empty_provenance_graph"]
    def as_dict(self)->Dict[str,List[str]]:
        return {r:[f"{e.source}->{e.target}" for e in self.edges if e.relation==r] for r in sorted(ALLOWED)}
