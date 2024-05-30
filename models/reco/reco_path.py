from dataclasses import dataclass
from typing import List

from models.reco.reco_node import RecoNode
from models.reco.reco_rel import RecoRel


@dataclass
class RecoPath:
    nodes: List[RecoNode]
    rels: List[RecoRel]

    def __str__(self) -> str:
        return " -> ".join(map(str, self.rels))
    
    def get_nth_rel(self, n: int) -> RecoRel:
        return self.rels[n]
