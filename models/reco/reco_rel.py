from dataclasses import dataclass

from models.reco.reco_node import RecoNode


@dataclass
class RecoRel:
    in_node: RecoNode
    relation: str
    out_node: RecoNode

    def __str__(self) -> str:
        return f"{self.relation}({self.in_node}, {self.out_node})"
    
    def to_facts(self) -> str:
        return f"{self.relation}({self.in_node}, {self.out_node})"