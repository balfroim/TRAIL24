from dataclasses import dataclass
from typing import List, Tuple

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
    
    @property
    def recommendation(self) -> Tuple[RecoNode, RecoNode]:
        return self.rels[0].in_node, self.rels[-1].out_node
