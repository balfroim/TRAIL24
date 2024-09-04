from dataclasses import dataclass
from models.nodes.fact import Fact
from models.reco.reco_node import RecoNode


@dataclass
class RecoRel:
    in_node: RecoNode
    relation: str
    out_node: RecoNode

    def __str__(self) -> str:
        return f"{self.relation}({self.in_node}, {self.out_node})"
    
    def facts(self):
        return [
            Fact(self.relation, (str(self.in_node), str(self.out_node)))
        ]